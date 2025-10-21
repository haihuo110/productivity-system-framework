#!/usr/bin/env python3
"""
Notion Sync Script

This script demonstrates how to integrate your productivity system with Notion's API.
It can sync tasks, create recurring items, update progress, and more.

Required:
- notion-client library: pip install notion-client
- Notion API key (get from notion.so/my-integrations)
- Database IDs from your Notion workspace

Usage:
    python notion-sync.py
"""

import os
from datetime import datetime, timedelta
from notion_client import Client

# Configuration
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")  # Set this environment variable
TASKS_DATABASE_ID = os.environ.get("TASKS_DB_ID")
PROJECTS_DATABASE_ID = os.environ.get("PROJECTS_DB_ID")
HABITS_DATABASE_ID = os.environ.get("HABITS_DB_ID")


class NotionProductivitySync:
    """Sync and automate your Notion productivity system."""
    
    def __init__(self, token):
        """Initialize Notion client."""
        self.notion = Client(auth=token)
        
    def create_daily_plan(self, date=None):
        """
        Create a new daily plan page.
        
        Args:
            date: Date for the plan (default: today)
        """
        if date is None:
            date = datetime.now()
            
        title = f"Daily Plan - {date.strftime('%Y-%m-%d')}"
        
        # Create page in your Daily Plans database
        new_page = self.notion.pages.create(
            parent={"database_id": "YOUR_DAILY_PLANS_DB_ID"},
            properties={
                "Name": {"title": [{"text": {"content": title}}]},
                "Date": {"date": {"start": date.isoformat()}},
                "Status": {"select": {"name": "Not Started"}}
            },
            children=[
                {
                    "object": "block",
                    "heading_2": {"rich_text": [{"text": {"content": "Top 3 Priorities"}}]}
                },
                {
                    "object": "block",
                    "to_do": {"rich_text": [{"text": {"content": "Priority 1"}}], "checked": False}
                },
                {
                    "object": "block",
                    "to_do": {"rich_text": [{"text": {"content": "Priority 2"}}], "checked": False}
                },
                {
                    "object": "block",
                    "to_do": {"rich_text": [{"text": {"content": "Priority 3"}}], "checked": False}
                },
            ]
        )
        
        print(f"✅ Created daily plan: {title}")
        return new_page
        
    def get_tasks_due_today(self):
        """
        Retrieve all tasks due today.
        
        Returns:
            List of task pages
        """
        today = datetime.now().date().isoformat()
        
        response = self.notion.databases.query(
            database_id=TASKS_DATABASE_ID,
            filter={
                "and": [
                    {"property": "Due Date", "date": {"equals": today}},
                    {"property": "Status", "select": {"does_not_equal": "Done"}}
                ]
            }
        )
        
        tasks = response.get("results", [])
        print(f"📋 Found {len(tasks)} tasks due today")
        return tasks
        
    def create_recurring_task(self, task_name, recurrence="daily", start_date=None):
        """
        Create recurring tasks.
        
        Args:
            task_name: Name of the task
            recurrence: daily, weekly, monthly
            start_date: When to start creating tasks
        """
        if start_date is None:
            start_date = datetime.now().date()
            
        # Calculate next occurrence dates
        occurrences = []
        
        if recurrence == "daily":
            occurrences = [start_date + timedelta(days=i) for i in range(30)]  # Next 30 days
        elif recurrence == "weekly":
            occurrences = [start_date + timedelta(weeks=i) for i in range(12)]  # Next 12 weeks
        elif recurrence == "monthly":
            occurrences = [start_date.replace(month=start_date.month + i) for i in range(12)]  # Next 12 months
            
        # Create tasks for each occurrence
        for date in occurrences:
            self.notion.pages.create(
                parent={"database_id": TASKS_DATABASE_ID},
                properties={
                    "Task": {"title": [{"text": {"content": task_name}}]},
                    "Due Date": {"date": {"start": date.isoformat()}},
                    "Status": {"select": {"name": "Todo"}},
                    "Recurring": {"checkbox": True}
                }
            )
            
        print(f"✅ Created {len(occurrences)} recurring tasks for '{task_name}'")
        
    def update_project_progress(self, project_id):
        """
        Calculate and update project completion percentage.
        
        Args:
            project_id: Notion page ID of the project
        """
        # Query all tasks related to this project
        response = self.notion.databases.query(
            database_id=TASKS_DATABASE_ID,
            filter={
                "property": "Project",
                "relation": {"contains": project_id}
            }
        )
        
        tasks = response.get("results", [])
        if not tasks:
            return
            
        completed = sum(1 for task in tasks if self._is_task_complete(task))
        total = len(tasks)
        progress = (completed / total * 100) if total > 0 else 0
        
        # Update project page
        self.notion.pages.update(
            page_id=project_id,
            properties={
                "Progress": {"number": progress},
                "Tasks Completed": {"number": completed},
                "Total Tasks": {"number": total}
            }
        )
        
        print(f"📊 Updated project progress: {progress:.1f}% ({completed}/{total} tasks)")
        
    def _is_task_complete(self, task):
        """Check if a task is marked as complete."""
        status = task["properties"].get("Status", {})
        if "select" in status and status["select"]:
            return status["select"]["name"] in ["Done", "Complete", "Completed"]
        return False
        
    def generate_weekly_report(self):
        """
        Generate a weekly productivity report.
        
        Returns:
            Dictionary with weekly stats
        """
        # Calculate date range for this week
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        # Query tasks completed this week
        response = self.notion.databases.query(
            database_id=TASKS_DATABASE_ID,
            filter={
                "and": [
                    {"property": "Status", "select": {"equals": "Done"}},
                    {"property": "Completed", "date": {"on_or_after": week_start.isoformat()}},
                    {"property": "Completed", "date": {"on_or_before": week_end.isoformat()}}
                ]
            }
        )
        
        completed_tasks = response.get("results", [])
        
        # Query habits for this week
        habit_response = self.notion.databases.query(
            database_id=HABITS_DATABASE_ID,
            filter={
                "and": [
                    {"property": "Date", "date": {"on_or_after": week_start.isoformat()}},
                    {"property": "Date", "date": {"on_or_before": week_end.isoformat()}}
                ]
            }
        )
        
        habit_entries = habit_response.get("results", [])
        
        report = {
            "week_start": week_start.isoformat(),
            "week_end": week_end.isoformat(),
            "tasks_completed": len(completed_tasks),
            "habit_entries": len(habit_entries),
            "habit_consistency": self._calculate_habit_consistency(habit_entries)
        }
        
        print("\n📊 Weekly Report")
        print(f"Week: {week_start} to {week_end}")
        print(f"Tasks completed: {report['tasks_completed']}")
        print(f"Habit consistency: {report['habit_consistency']:.1f}%")
        
        return report
        
    def _calculate_habit_consistency(self, habit_entries):
        """Calculate average habit consistency."""
        if not habit_entries:
            return 0
            
        # This is a simplified calculation
        # Customize based on your Notion database structure
        total_expected = len(habit_entries) * 7  # Assuming 7 habits tracked
        total_completed = sum(1 for entry in habit_entries if entry["properties"].get("Completed", {}).get("checkbox", False))
        
        return (total_completed / total_expected * 100) if total_expected > 0 else 0
        
    def cleanup_old_tasks(self, days=90):
        """
        Archive or delete tasks older than specified days.
        
        Args:
            days: Number of days to keep tasks
        """
        cutoff_date = (datetime.now().date() - timedelta(days=days)).isoformat()
        
        response = self.notion.databases.query(
            database_id=TASKS_DATABASE_ID,
            filter={
                "and": [
                    {"property": "Status", "select": {"equals": "Done"}},
                    {"property": "Completed", "date": {"before": cutoff_date}}
                ]
            }
        )
        
        old_tasks = response.get("results", [])
        
        for task in old_tasks:
            # Archive the task
            self.notion.pages.update(
                page_id=task["id"],
                archived=True
            )
            
        print(f"🗑️ Archived {len(old_tasks)} old tasks")


def main():
    """Main execution function."""
    
    if not NOTION_TOKEN:
        print("❌ Error: NOTION_TOKEN environment variable not set")
        print("   Get your token from: https://www.notion.so/my-integrations")
        return
        
    # Initialize sync
    sync = NotionProductivitySync(NOTION_TOKEN)
    
    print("🚀 Notion Productivity System Sync\n")
    
    try:
        # Example operations
        print("1. Creating today's daily plan...")
        # sync.create_daily_plan()
        
        print("\n2. Fetching tasks due today...")
        # tasks = sync.get_tasks_due_today()
        
        print("\n3. Generating weekly report...")
        # report = sync.generate_weekly_report()
        
        print("\n4. Cleaning up old tasks...")
        # sync.cleanup_old_tasks(days=90)
        
        print("\n✅ Sync completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during sync: {str(e)}")
        raise


if __name__ == "__main__":
    main()


# Setup Instructions:
# 
# 1. Install the Notion Python client:
#    pip install notion-client
#
# 2. Create a Notion integration:
#    - Go to https://www.notion.so/my-integrations
#    - Click "+ New integration"
#    - Give it a name and select your workspace
#    - Copy the "Internal Integration Token"
#
# 3. Share your databases with the integration:
#    - Open each database in Notion
#    - Click "..." menu → "Add connections"
#    - Select your integration
#
# 4. Get your database IDs:
#    - Open database in Notion
#    - Copy the URL (looks like: notion.so/workspace/DATABASE_ID?v=...)
#    - Extract the DATABASE_ID part
#
# 5. Set environment variables:
#    export NOTION_TOKEN="your_token_here"
#    export TASKS_DB_ID="your_tasks_database_id"
#    export PROJECTS_DB_ID="your_projects_database_id"
#    export HABITS_DB_ID="your_habits_database_id"
#
# 6. Run the script:
#    python notion-sync.py
