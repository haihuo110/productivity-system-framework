#!/usr/bin/env python3
"""
Task Export Script

Export your tasks to various formats (CSV, JSON, Markdown) for backup or analysis.

Usage:
    python task-export.py --format csv --output tasks.csv
    python task-export.py --format json --output tasks.json
    python task-export.py --format markdown --output tasks.md
"""

import os
import json
import csv
import argparse
from datetime import datetime
from notion_client import Client

# Configuration
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
TASKS_DATABASE_ID = os.environ.get("TASKS_DB_ID")


class TaskExporter:
    """Export tasks from Notion to various formats."""
    
    def __init__(self, token, database_id):
        self.notion = Client(auth=token)
        self.database_id = database_id
        
    def fetch_all_tasks(self, filters=None):
        """
        Fetch all tasks from the database.
        
        Args:
            filters: Optional Notion filter object
            
        Returns:
            List of task dictionaries
        """
        tasks = []
        has_more = True
        start_cursor = None
        
        query_params = {"database_id": self.database_id}
        if filters:
            query_params["filter"] = filters
            
        print("📥 Fetching tasks from Notion...")
        
        while has_more:
            if start_cursor:
                query_params["start_cursor"] = start_cursor
                
            response = self.notion.databases.query(**query_params)
            tasks.extend(response["results"])
            
            has_more = response["has_more"]
            start_cursor = response.get("next_cursor")
            
        print(f"✅ Fetched {len(tasks)} tasks")
        return tasks
        
    def parse_task(self, task):
        """
        Parse a Notion task page into a simplified dict.
        
        Args:
            task: Notion page object
            
        Returns:
            Dictionary with task data
        """
        props = task["properties"]
        
        def get_text(prop):
            """Extract text from rich text property."""
            if prop and "title" in prop:
                return " ".join([t["plain_text"] for t in prop["title"]])
            elif prop and "rich_text" in prop:
                return " ".join([t["plain_text"] for t in prop["rich_text"]])
            return ""
            
        def get_select(prop):
            """Extract value from select property."""
            return prop.get("select", {}).get("name", "") if prop.get("select") else ""
            
        def get_date(prop):
            """Extract date from date property."""
            date_obj = prop.get("date")
            return date_obj.get("start", "") if date_obj else ""
            
        def get_multi_select(prop):
            """Extract values from multi-select property."""
            return ", ".join([opt["name"] for opt in prop.get("multi_select", [])])
            
        return {
            "id": task["id"],
            "task": get_text(props.get("Task", props.get("Name", {}))),
            "status": get_select(props.get("Status", {})),
            "priority": get_select(props.get("Priority", {})),
            "due_date": get_date(props.get("Due Date", {})),
            "scheduled": get_date(props.get("Scheduled", {})),
            "context": get_multi_select(props.get("Context", {})),
            "energy": get_select(props.get("Energy", {})),
            "time_estimate": props.get("Time Estimate", {}).get("number", 0),
            "created": task["created_time"],
            "updated": task["last_edited_time"],
            "url": task["url"]
        }
        
    def export_to_csv(self, tasks, output_file):
        """
        Export tasks to CSV file.
        
        Args:
            tasks: List of task objects
            output_file: Output file path
        """
        if not tasks:
            print("⚠️  No tasks to export")
            return
            
        parsed_tasks = [self.parse_task(task) for task in tasks]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=parsed_tasks[0].keys())
            writer.writeheader()
            writer.writerows(parsed_tasks)
            
        print(f"✅ Exported {len(tasks)} tasks to {output_file}")
        
    def export_to_json(self, tasks, output_file):
        """
        Export tasks to JSON file.
        
        Args:
            tasks: List of task objects
            output_file: Output file path
        """
        parsed_tasks = [self.parse_task(task) for task in tasks]
        
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "total_tasks": len(tasks),
            "tasks": parsed_tasks
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Exported {len(tasks)} tasks to {output_file}")
        
    def export_to_markdown(self, tasks, output_file):
        """
        Export tasks to Markdown file.
        
        Args:
            tasks: List of task objects
            output_file: Output file path
        """
        parsed_tasks = [self.parse_task(task) for task in tasks]
        
        # Group tasks by status
        by_status = {}
        for task in parsed_tasks:
            status = task["status"] or "No Status"
            if status not in by_status:
                by_status[status] = []
            by_status[status].append(task)
            
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Task Export\n\n")
            f.write(f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"**Total Tasks:** {len(tasks)}\n\n")
            f.write("---\n\n")
            
            for status, status_tasks in by_status.items():
                f.write(f"## {status} ({len(status_tasks)} tasks)\n\n")
                
                for task in status_tasks:
                    f.write(f"### {task['task']}\n\n")
                    f.write(f"- **Priority:** {task['priority']}\n")
                    f.write(f"- **Due Date:** {task['due_date']}\n")
                    f.write(f"- **Context:** {task['context']}\n")
                    f.write(f"- **Energy:** {task['energy']}\n")
                    f.write(f"- **Time Estimate:** {task['time_estimate']} min\n")
                    f.write(f"- **Created:** {task['created'][:10]}\n")
                    f.write(f"- **Link:** {task['url']}\n")
                    f.write("\n")
                    
                f.write("---\n\n")
                
        print(f"✅ Exported {len(tasks)} tasks to {output_file}")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Export tasks from Notion")
    parser.add_argument(
        "--format",
        choices=["csv", "json", "markdown"],
        default="json",
        help="Output format (default: json)"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (default: tasks.{format})"
    )
    parser.add_argument(
        "--status",
        default=None,
        help="Filter by status (e.g., 'Todo', 'In Progress')"
    )
    parser.add_argument(
        "--priority",
        default=None,
        help="Filter by priority (e.g., 'P1', 'High')"
    )
    
    args = parser.parse_args()
    
    # Check for required environment variables
    if not NOTION_TOKEN:
        print("❌ Error: NOTION_TOKEN environment variable not set")
        return
        
    if not TASKS_DATABASE_ID:
        print("❌ Error: TASKS_DB_ID environment variable not set")
        return
        
    # Set default output file
    if not args.output:
        args.output = f"tasks.{args.format}"
        
    # Build filters
    filters = None
    if args.status or args.priority:
        filter_conditions = []
        
        if args.status:
            filter_conditions.append({
                "property": "Status",
                "select": {"equals": args.status}
            })
            
        if args.priority:
            filter_conditions.append({
                "property": "Priority",
                "select": {"equals": args.priority}
            })
            
        if len(filter_conditions) > 1:
            filters = {"and": filter_conditions}
        else:
            filters = filter_conditions[0]
            
    # Initialize exporter
    exporter = TaskExporter(NOTION_TOKEN, TASKS_DATABASE_ID)
    
    print("🚀 Task Export Tool\n")
    
    try:
        # Fetch tasks
        tasks = exporter.fetch_all_tasks(filters)
        
        if not tasks:
            print("⚠️  No tasks found")
            return
            
        # Export to chosen format
        if args.format == "csv":
            exporter.export_to_csv(tasks, args.output)
        elif args.format == "json":
            exporter.export_to_json(tasks, args.output)
        elif args.format == "markdown":
            exporter.export_to_markdown(tasks, args.output)
            
        print(f"\n✅ Export complete!")
        print(f"📁 File saved to: {args.output}")
        
    except Exception as e:
        print(f"\n❌ Error during export: {str(e)}")
        raise


if __name__ == "__main__":
    main()


# Setup Instructions:
#
# 1. Install dependencies:
#    pip install notion-client
#
# 2. Set environment variables:
#    export NOTION_TOKEN="your_token_here"
#    export TASKS_DB_ID="your_tasks_database_id"
#
# 3. Run the script:
#    # Export all tasks to JSON (default)
#    python task-export.py
#
#    # Export to CSV
#    python task-export.py --format csv --output my-tasks.csv
#
#    # Export only Todo tasks to Markdown
#    python task-export.py --format markdown --status Todo --output todo-tasks.md
#
#    # Export only P1 priority tasks
#    python task-export.py --status "In Progress" --priority P1
