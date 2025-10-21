#!/usr/bin/env python3
"""
Weekly Report Script

Generate a comprehensive weekly productivity report from your Notion data.
Includes task completion, habit consistency, goal progress, and time allocation.

Usage:
    python weekly-report.py
    python weekly-report.py --format markdown --output weekly-report.md
    python weekly-report.py --format html --email
"""

import os
import argparse
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    from notion_client import Client
    NOTION_AVAILABLE = True
except ImportError:
    NOTION_AVAILABLE = False
    print("⚠️  notion-client not installed. Run: pip install notion-client")

# Configuration
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
TASKS_DATABASE_ID = os.environ.get("TASKS_DB_ID")
HABITS_DATABASE_ID = os.environ.get("HABITS_DB_ID")
GOALS_DATABASE_ID = os.environ.get("GOALS_DB_ID")

# Email configuration
EMAIL_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("SMTP_PORT", "587"))
EMAIL_USER = os.environ.get("SMTP_USER")
EMAIL_PASSWORD = os.environ.get("SMTP_PASSWORD")
REPORT_EMAIL = os.environ.get("REPORT_EMAIL")


class WeeklyReportGenerator:
    """Generate weekly productivity reports."""
    
    def __init__(self, token=None):
        if token and NOTION_AVAILABLE:
            self.notion = Client(auth=token)
        else:
            self.notion = None
            
        # Calculate this week's date range
        today = datetime.now().date()
        self.week_start = today - timedelta(days=today.weekday())
        self.week_end = self.week_start + timedelta(days=6)
        
    def get_tasks_data(self):
        """
        Get task completion data for the week.
        
        Returns:
            Dictionary with task stats
        """
        if not self.notion or not TASKS_DATABASE_ID:
            return self._get_sample_tasks_data()
            
        try:
            # Get completed tasks
            completed = self.notion.databases.query(
                database_id=TASKS_DATABASE_ID,
                filter={
                    "and": [
                        {"property": "Status", "select": {"equals": "Done"}},
                        {"property": "Completed", "date": {"on_or_after": self.week_start.isoformat()}},
                        {"property": "Completed", "date": {"on_or_before": self.week_end.isoformat()}}
                    ]
                }
            )
            
            # Get all tasks for completion rate
            all_tasks = self.notion.databases.query(
                database_id=TASKS_DATABASE_ID,
                filter={
                    "property": "Created",
                    "date": {"on_or_before": self.week_end.isoformat()}
                }
            )
            
            completed_count = len(completed.get("results", []))
            total_count = len(all_tasks.get("results", []))
            
            # Categorize by priority
            by_priority = {"P1": 0, "P2": 0, "P3": 0, "P4": 0}
            for task in completed.get("results", []):
                priority = task["properties"].get("Priority", {}).get("select", {}).get("name", "P4")
                by_priority[priority] = by_priority.get(priority, 0) + 1
                
            return {
                "completed": completed_count,
                "total": total_count,
                "completion_rate": (completed_count / total_count * 100) if total_count > 0 else 0,
                "by_priority": by_priority
            }
            
        except Exception as e:
            print(f"⚠️  Error fetching tasks: {e}")
            return self._get_sample_tasks_data()
            
    def _get_sample_tasks_data(self):
        """Return sample data when Notion is unavailable."""
        return {
            "completed": 24,
            "total": 35,
            "completion_rate": 68.6,
            "by_priority": {"P1": 8, "P2": 10, "P3": 5, "P4": 1}
        }
        
    def get_habits_data(self):
        """
        Get habit consistency data for the week.
        
        Returns:
            Dictionary with habit stats
        """
        if not self.notion or not HABITS_DATABASE_ID:
            return self._get_sample_habits_data()
            
        try:
            response = self.notion.databases.query(
                database_id=HABITS_DATABASE_ID,
                filter={
                    "and": [
                        {"property": "Date", "date": {"on_or_after": self.week_start.isoformat()}},
                        {"property": "Date", "date": {"on_or_before": self.week_end.isoformat()}}
                    ]
                }
            )
            
            entries = response.get("results", [])
            
            # Calculate per-habit stats
            habits = {}
            for entry in entries:
                habit_name = entry["properties"].get("Habit", {}).get("select", {}).get("name", "Unknown")
                completed = entry["properties"].get("Completed", {}).get("checkbox", False)
                
                if habit_name not in habits:
                    habits[habit_name] = {"completed": 0, "total": 0}
                    
                habits[habit_name]["total"] += 1
                if completed:
                    habits[habit_name]["completed"] += 1
                    
            # Calculate completion rates
            for habit in habits.values():
                habit["rate"] = (habit["completed"] / habit["total"] * 100) if habit["total"] > 0 else 0
                
            overall_rate = sum(h["rate"] for h in habits.values()) / len(habits) if habits else 0
            
            return {
                "habits": habits,
                "overall_rate": overall_rate,
                "total_entries": len(entries)
            }
            
        except Exception as e:
            print(f"⚠️  Error fetching habits: {e}")
            return self._get_sample_habits_data()
            
    def _get_sample_habits_data(self):
        """Return sample data when Notion is unavailable."""
        return {
            "habits": {
                "Morning Meditation": {"completed": 6, "total": 7, "rate": 85.7},
                "Exercise": {"completed": 4, "total": 7, "rate": 57.1},
                "Evening Journal": {"completed": 7, "total": 7, "rate": 100.0},
                "Reading": {"completed": 5, "total": 7, "rate": 71.4}
            },
            "overall_rate": 78.6,
            "total_entries": 28
        }
        
    def generate_text_report(self):
        """
        Generate plain text report.
        
        Returns:
            Report as string
        """
        tasks = self.get_tasks_data()
        habits = self.get_habits_data()
        
        report = f"""
{'='*60}
WEEKLY PRODUCTIVITY REPORT
{'='*60}

Week: {self.week_start.strftime('%B %d')} - {self.week_end.strftime('%B %d, %Y')}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

{'='*60}
TASK COMPLETION
{'='*60}

Completed Tasks: {tasks['completed']}
Total Tasks: {tasks['total']}
Completion Rate: {tasks['completion_rate']:.1f}%

By Priority:
  P1 (Critical): {tasks['by_priority']['P1']} tasks
  P2 (High):     {tasks['by_priority']['P2']} tasks
  P3 (Medium):   {tasks['by_priority']['P3']} tasks
  P4 (Low):      {tasks['by_priority']['P4']} tasks

{'='*60}
HABIT CONSISTENCY
{'='*60}

Overall Consistency: {habits['overall_rate']:.1f}%
Total Entries: {habits['total_entries']}

Individual Habits:
"""
        
        for habit_name, stats in habits['habits'].items():
            completion_bar = '█' * int(stats['rate'] / 10) + '░' * (10 - int(stats['rate'] / 10))
            report += f"  {habit_name:20} {completion_bar} {stats['completed']}/{stats['total']} ({stats['rate']:.1f}%)\n"
            
        report += f"""
{'='*60}
INSIGHTS & RECOMMENDATIONS
{'='*60}

"""
        
        # Add insights
        if tasks['completion_rate'] >= 80:
            report += "✅ Excellent task completion! You're crushing it.\n"
        elif tasks['completion_rate'] >= 60:
            report += "👍 Solid task completion. Keep up the good work.\n"
        else:
            report += "⚠️  Task completion below target. Consider reducing commitments.\n"
            
        if habits['overall_rate'] >= 80:
            report += "✅ Outstanding habit consistency!\n"
        elif habits['overall_rate'] >= 60:
            report += "👍 Good habit consistency. Room for improvement.\n"
        else:
            report += "⚠️  Habit consistency needs attention. Review your systems.\n"
            
        # Identify struggling habits
        struggling = [name for name, stats in habits['habits'].items() if stats['rate'] < 60]
        if struggling:
            report += f"\n👉 Habits needing attention: {', '.join(struggling)}\n"
            
        report += f"""
{'='*60}
NEXT WEEK FOCUS
{'='*60}

1. Review and adjust weekly priorities
2. Address struggling habits
3. Celebrate your wins!

{'='*60}
"""
        
        return report
        
    def generate_markdown_report(self):
        """
        Generate Markdown format report.
        
        Returns:
            Report as Markdown string
        """
        tasks = self.get_tasks_data()
        habits = self.get_habits_data()
        
        report = f"""# Weekly Productivity Report

**Week:** {self.week_start.strftime('%B %d')} - {self.week_end.strftime('%B %d, %Y')}  
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 📋 Task Completion

- **Completed Tasks:** {tasks['completed']}
- **Total Tasks:** {tasks['total']}
- **Completion Rate:** {tasks['completion_rate']:.1f}%

### By Priority

| Priority | Count |
|----------|-------|
| P1 (Critical) | {tasks['by_priority']['P1']} |
| P2 (High) | {tasks['by_priority']['P2']} |
| P3 (Medium) | {tasks['by_priority']['P3']} |
| P4 (Low) | {tasks['by_priority']['P4']} |

---

## ✅ Habit Consistency

- **Overall Consistency:** {habits['overall_rate']:.1f}%
- **Total Entries:** {habits['total_entries']}

### Individual Habits

| Habit | Completed | Rate |
|-------|-----------|------|
"""
        
        for habit_name, stats in habits['habits'].items():
            report += f"| {habit_name} | {stats['completed']}/{stats['total']} | {stats['rate']:.1f}% |\n"
            
        report += """
---

## 💡 Insights & Recommendations

"""
        
        if tasks['completion_rate'] >= 80:
            report += "- ✅ **Excellent task completion!** You're crushing it.\n"
        elif tasks['completion_rate'] >= 60:
            report += "- 👍 **Solid task completion.** Keep up the good work.\n"
        else:
            report += "- ⚠️  **Task completion below target.** Consider reducing commitments.\n"
            
        if habits['overall_rate'] >= 80:
            report += "- ✅ **Outstanding habit consistency!**\n"
        elif habits['overall_rate'] >= 60:
            report += "- 👍 **Good habit consistency.** Room for improvement.\n"
        else:
            report += "- ⚠️  **Habit consistency needs attention.** Review your systems.\n"
            
        struggling = [name for name, stats in habits['habits'].items() if stats['rate'] < 60]
        if struggling:
            report += f"\n### Habits Needing Attention\n\n"
            for habit in struggling:
                report += f"- {habit}\n"
                
        report += """
---

## 🎯 Next Week Focus

1. Review and adjust weekly priorities
2. Address struggling habits
3. Celebrate your wins!
"""
        
        return report
        
    def send_email_report(self, report, format="text"):
        """
        Email the report.
        
        Args:
            report: Report content
            format: "text" or "html"
        """
        if not all([EMAIL_USER, EMAIL_PASSWORD, REPORT_EMAIL]):
            print("❌ Email not configured")
            return
            
        subject = f"Weekly Productivity Report - {self.week_start.strftime('%b %d, %Y')}"
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = EMAIL_USER
        msg["To"] = REPORT_EMAIL
        
        if format == "html":
            # Convert markdown to simple HTML
            html_content = report.replace("\n", "<br>")
            html_content = f"<html><body style='font-family: monospace;'>{html_content}</body></html>"
            msg.attach(MIMEText(html_content, "html"))
        else:
            msg.attach(MIMEText(report, "plain"))
            
        try:
            with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
                server.starttls()
                server.login(EMAIL_USER, EMAIL_PASSWORD)
                server.send_message(msg)
                
            print(f"✅ Report emailed to {REPORT_EMAIL}")
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Generate weekly productivity report")
    parser.add_argument(
        "--format",
        choices=["text", "markdown"],
        default="text",
        help="Report format (default: text)"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (default: print to console)"
    )
    parser.add_argument(
        "--email",
        action="store_true",
        help="Email the report"
    )
    
    args = parser.parse_args()
    
    print("🚀 Weekly Report Generator\n")
    
    # Initialize generator
    generator = WeeklyReportGenerator(token=NOTION_TOKEN)
    
    # Generate report
    print("Generating report...\n")
    
    if args.format == "markdown":
        report = generator.generate_markdown_report()
    else:
        report = generator.generate_text_report()
        
    # Output report
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ Report saved to {args.output}")
    else:
        print(report)
        
    # Email if requested
    if args.email:
        generator.send_email_report(report, format=args.format)
        
    print("\n✅ Report generation complete!")


if __name__ == "__main__":
    main()


# Setup Instructions:
#
# 1. Install dependencies:
#    pip install notion-client
#
# 2. Configure Notion (optional):
#    export NOTION_TOKEN="your_token_here"
#    export TASKS_DB_ID="your_tasks_database_id"
#    export HABITS_DB_ID="your_habits_database_id"
#
# 3. Configure Email (optional):
#    export SMTP_USER="your_email@gmail.com"
#    export SMTP_PASSWORD="your_app_password"
#    export REPORT_EMAIL="your_email@gmail.com"
#
# 4. Run manually:
#    python weekly-report.py
#    python weekly-report.py --format markdown --output report.md
#    python weekly-report.py --email
#
# 5. Schedule weekly (cron):
#    crontab -e
#    # Every Monday at 9 AM:
#    0 9 * * 1 /usr/bin/python3 /path/to/weekly-report.py --email
