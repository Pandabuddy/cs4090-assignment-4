import pytest
from src.tasks import add_recurring_task, share_task, priority_sort

def test_recurring():
    tasks = []
    new_task = {
        "title": "Feed Dog",
        "priority": "High",
        "category": "Personal",
        "due_date": "2025-04-23",
        "recurring": "daily"
    }
    add_recurring_task(tasks, new_task)
    assert len(tasks) == 1
    assert tasks[0]["recurring"] == "daily"

def test_share():
    tasks = [{"title": "Group Project", "shared_with": []}]
    share_task(tasks, "Group Project", "group@example.com")
    assert "group@example.com" in tasks[0]["shared_with"]

def test_sort():
    tasks = [
        {"title": "Task A", "priority": "Low"},
        {"title": "Task B", "priority": "High"},
        {"title": "Task C", "priority": "Medium"}
    ]
    sorted_tasks = priority_sort(tasks)
    assert sorted_tasks[0]["priority"] == "High"
    assert sorted_tasks[1]["priority"] == "Medium"
    assert sorted_tasks[2]["priority"] == "Low"