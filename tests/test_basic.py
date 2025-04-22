import pytest
from src.tasks import load_tasks, save_tasks, filter_tasks_by_priority, filter_tasks_by_category, filter_tasks_by_completion

@pytest.fixture
def sample_tasks():
    return [{"id": 1, "title": "aaaaaaa", "priority": "Low", "category": "Personal", "completed": True},
            {"id": 2, "title": "bbbbbbb", "priority": "High", "category": "School", "completed": True}, 
            {"id": 3, "title": "ccccccc", "priority": "Medium", "category": "School", "completed": False}]

def test_load():
    tasks = load_tasks()
    assert isinstance(tasks, list)
    
def test_save(sample_tasks):
    save_tasks(sample_tasks)
    loaded = load_tasks()
    assert len(loaded) == len(sample_tasks)

def test_priority(sample_tasks):
    priority = filter_tasks_by_priority(sample_tasks, "Low")
    assert len(priority) == 1
    assert priority[0]["title"] == "aaaaaaa"

def test_category(sample_tasks):
    category = filter_tasks_by_category(sample_tasks, "School")
    assert len(category) == 2
    assert category[0]["title"] == "bbbbbbb"
    assert category[1]["title"] == "ccccccc"

def test_completed(sample_tasks):
    completed_tasks = filter_tasks_by_completion(sample_tasks)
    assert len(completed_tasks) == 2
    assert completed_tasks[0]["title"] == "aaaaaaa"
    assert completed_tasks[1]["title"] == "bbbbbbb"