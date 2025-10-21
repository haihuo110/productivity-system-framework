#!/usr/bin/env python3
"""
Habit Reminder Script

Send automated reminders for your daily habits via email, Slack, or console.
Can be scheduled to run at specific times using cron or Task Scheduler.

Usage:
    python habit-reminder.py --method email
    python habit-reminder.py --method slack
    python habit-reminder.py --method console
"""

import os
import smtplib
import argparse
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    from notion_client import Client
    NOTION_AVAILABLE = True
except ImportError:
    NOTION_AVAILABLE = False
    
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# Configuration
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
HABITS_DATABASE_ID = os.environ.get("HABITS_DB_ID")

# Email configuration
EMAIL_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("SMTP_PORT", "587"))
EMAIL_USER = os.environ.get("SMTP_USER")
EMAIL_PASSWORD = os.environ.get("SMTP_PASSWORD")
EMAIL_TO = os.environ.get("REMINDER_EMAIL")

# Slack configuration
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

# Default habits (if not using Notion)
DEFAULT_HABITS = [
    {"name": "Morning Meditation", "time": "07:00", "emoji": "🧘"},
    {"name": "Exercise", "time": "17:00", "emoji": "🏋️"},
    {"name": "Evening Journal", "time": "21:00", "emoji": "📓"},
    {"name": "Read", "time": "21:30", "emoji": "📚"},
]


class HabitReminder:
    """Send habit reminders via various channels."""
    
    def __init__(self, use_notion=False):
        self.use_notion = use_notion and NOTION_AVAILABLE
        if self.use_notion and NOTION_TOKEN:
            self.notion = Client(auth=NOTION_TOKEN)
        else:
            self.notion = None
            
    def get_habits(self):
        """
        Get list of habits to remind about.
        
        Returns:
            List of habit dictionaries
        """
        if self.use_notion and self.notion:
            return self._get_habits_from_notion()
        else:
            return DEFAULT_HABITS
            
    def _get_habits_from_notion(self):
        """
        Fetch habits from Notion database.
        
        Returns:
            List of habit dictionaries
        """
        try:
            response = self.notion.databases.query(
                database_id=HABITS_DATABASE_ID,
                filter={
                    "property": "Active",
                    "checkbox": {"equals": True}
                }
            )
            
            habits = []
            for page in response.get("results", []):
                props = page["properties"]
                
                # Extract habit name
                name_prop = props.get("Name", props.get("Habit", {}))
                name = ""
                if name_prop.get("title"):
                    name = " ".join([t["plain_text"] for t in name_prop["title"]])
                    
                # Extract other properties
                time = props.get("Time", {}).get("rich_text", [{}])[0].get("plain_text", "")
                emoji = props.get("Emoji", {}).get("rich_text", [{}])[0].get("plain_text", "✅")
                
                habits.append({
                    "name": name,
                    "time": time,
                    "emoji": emoji
                })
                
            return habits
            
        except Exception as e:
            print(f"⚠️  Error fetching habits from Notion: {e}")
            return DEFAULT_HABITS
            
    def get_current_habits(self):
        """
        Get habits that should be reminded about right now.
        
        Returns:
            List of habit dictionaries for current time
        """
        current_hour = datetime.now().hour
        current_minute = datetime.now().minute
        current_time = f"{current_hour:02d}:{current_minute:02d}"
        
        habits = self.get_habits()
        
        # Find habits within 15 minutes of current time
        current_habits = []
        for habit in habits:
            if not habit.get("time"):
                continue
                
            habit_time = habit["time"]
            habit_hour, habit_minute = map(int, habit_time.split(":"))
            
            time_diff = (current_hour * 60 + current_minute) - (habit_hour * 60 + habit_minute)
            
            # Remind if it's time or up to 15 minutes past
            if 0 <= time_diff <= 15:
                current_habits.append(habit)
                
        return current_habits
        
    def send_email_reminder(self, habits):
        """
        Send email reminder.
        
        Args:
            habits: List of habit dictionaries
        """
        if not EMAIL_USER or not EMAIL_PASSWORD or not EMAIL_TO:
            print("❌ Email not configured. Set SMTP_USER, SMTP_PASSWORD, and REMINDER_EMAIL")
            return
            
        subject = f"✅ Habit Reminder - {datetime.now().strftime('%H:%M')}"
        
        # Build email body
        body = "<html><body>"
        body += f"<h2>🔔 Time for Your Habits!</h2>"
        body += f"<p><strong>{datetime.now().strftime('%A, %B %d, %Y - %I:%M %p')}</strong></p>"
        body += "<hr>"
        body += "<ul>"
        
        for habit in habits:
            emoji = habit.get("emoji", "✅")
            body += f"<li><h3>{emoji} {habit['name']}</h3></li>"
            
        body += "</ul>"
        body += "<hr>"
        body += "<p>You've got this! 💪</p>"
        body += "<p><em>Track your completion in Notion or your habit tracker.</em></p>"
        body += "</body></html>"
        
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = EMAIL_USER
        msg["To"] = EMAIL_TO
        
        html_part = MIMEText(body, "html")
        msg.attach(html_part)
        
        # Send email
        try:
            with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
                server.starttls()
                server.login(EMAIL_USER, EMAIL_PASSWORD)
                server.send_message(msg)
                
            print(f"✅ Email reminder sent to {EMAIL_TO}")
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            
    def send_slack_reminder(self, habits):
        """
        Send Slack reminder.
        
        Args:
            habits: List of habit dictionaries
        """
        if not REQUESTS_AVAILABLE:
            print("❌ requests library not installed. Run: pip install requests")
            return
            
        if not SLACK_WEBHOOK_URL:
            print("❌ Slack webhook not configured. Set SLACK_WEBHOOK_URL")
            return
            
        # Build Slack message
        text = f":bell: *Habit Reminder - {datetime.now().strftime('%H:%M')}*\n\n"
        text += "Time for your habits!\n\n"
        
        for habit in habits:
            emoji = habit.get("emoji", ":white_check_mark:")
            text += f"• {emoji} *{habit['name']}*\n"
            
        text += "\nYou've got this! :muscle:"
        
        payload = {
            "text": text,
            "username": "Habit Reminder Bot",
            "icon_emoji": ":alarm_clock:"
        }
        
        try:
            response = requests.post(SLACK_WEBHOOK_URL, json=payload)
            
            if response.status_code == 200:
                print("✅ Slack reminder sent")
            else:
                print(f"❌ Error sending Slack message: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error sending Slack message: {e}")
            
    def print_console_reminder(self, habits):
        """
        Print reminder to console.
        
        Args:
            habits: List of habit dictionaries
        """
        print("\n" + "="*50)
        print(f"🔔 HABIT REMINDER - {datetime.now().strftime('%H:%M')}")
        print("="*50 + "\n")
        print(f"{datetime.now().strftime('%A, %B %d, %Y - %I:%M %p')}\n")
        print("Time for your habits!\n")
        
        for habit in habits:
            emoji = habit.get("emoji", "✅")
            print(f"  {emoji} {habit['name']}")
            
        print("\nYou've got this! 💪\n")
        print("="*50 + "\n")
        
    def send_daily_summary(self, method="console"):
        """
        Send a summary of all daily habits.
        
        Args:
            method: Reminder method (email, slack, console)
        """
        habits = self.get_habits()
        
        if not habits:
            print("⚠️  No habits configured")
            return
            
        if method == "email":
            self.send_email_reminder(habits)
        elif method == "slack":
            self.send_slack_reminder(habits)
        else:
            self.print_console_reminder(habits)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Send habit reminders")
    parser.add_argument(
        "--method",
        choices=["email", "slack", "console"],
        default="console",
        help="Reminder method (default: console)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Send reminder for all habits (not just current time)"
    )
    parser.add_argument(
        "--notion",
        action="store_true",
        help="Fetch habits from Notion (requires NOTION_TOKEN)"
    )
    
    args = parser.parse_args()
    
    print("🚀 Habit Reminder System\n")
    
    # Initialize reminder
    reminder = HabitReminder(use_notion=args.notion)
    
    # Get habits to remind about
    if args.all:
        habits = reminder.get_habits()
        print(f"Sending reminder for all {len(habits)} habits...\n")
    else:
        habits = reminder.get_current_habits()
        if not habits:
            print("✅ No habits due right now.")
            return
        print(f"Found {len(habits)} habit(s) to remind about...\n")
        
    # Send reminder
    if args.method == "email":
        reminder.send_email_reminder(habits)
    elif args.method == "slack":
        reminder.send_slack_reminder(habits)
    else:
        reminder.print_console_reminder(habits)


if __name__ == "__main__":
    main()


# Setup Instructions:
#
# 1. Install dependencies (optional):
#    pip install notion-client requests
#
# 2. For Email reminders:
#    export SMTP_HOST="smtp.gmail.com"  # Or your email provider
#    export SMTP_PORT="587"
#    export SMTP_USER="your_email@gmail.com"
#    export SMTP_PASSWORD="your_app_password"  # Use app-specific password for Gmail
#    export REMINDER_EMAIL="your_email@gmail.com"
#
# 3. For Slack reminders:
#    - Create incoming webhook: https://api.slack.com/messaging/webhooks
#    export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
#
# 4. For Notion integration:
#    export NOTION_TOKEN="your_token_here"
#    export HABITS_DB_ID="your_habits_database_id"
#
# 5. Schedule with cron (Linux/Mac):
#    crontab -e
#    # Add lines for each reminder time:
#    0 7 * * * /usr/bin/python3 /path/to/habit-reminder.py --method email
#    0 17 * * * /usr/bin/python3 /path/to/habit-reminder.py --method slack
#    0 21 * * * /usr/bin/python3 /path/to/habit-reminder.py --method email
#
# 6. Or use Task Scheduler (Windows):
#    - Create a new task
#    - Set trigger times
#    - Action: Start program python.exe with arguments habit-reminder.py --method email
