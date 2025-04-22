import pytest
import pytest_bdd

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from src.tasks import load_tasks, save_tasks, filter_tasks_by_priority, filter_tasks_by_category, filter_tasks_by_completion


@pytest_bdd.given("Tasks are saved")
@pytest.fixture
def create_tasks():
    tasks = [{"id": 1, "title": "aaaaaaa", "priority": "Low", "category": "Personal", "completed": True}]
    return tasks

@pytest_bdd.when("User wants to load tasks")
@pytest.fixture
def load_list():
    return load_tasks()

@pytest_bdd.then("Saved tasks should be retrived")
def test_loaded(load_list):
    assert len(load_list) == 1
    assert load_list[0]["title"] == "aaaaaaa"



@pytest_bdd.given("User wants to save a task")
@pytest.fixture
def user_tasks():
    return []

@pytest_bdd.when("User gives a title, date_due, priority, category")
@pytest.fixture
def add_task(user_tasks):
    task = {"id": 1, "title": "aaaaaaa", "priority": "Low", "category": "Personal", "completed": True}
    user_tasks.append(task)
    save_tasks(user_tasks)
    return user_tasks

@pytest_bdd.then("Result should be task was added")
def test_added(add_task):
    assert len(add_task) == 1



@pytest_bdd.given("Tasks have different priorities")
@pytest.fixture
def task_set():
    return [{"id": 1, "title": "aaaaaaa", "priority": "Low", "category": "Personal", "completed": True},
    {"id": 2, "title": "bbbbbbb", "priority": "High", "category": "School", "completed": True}, 
    {"id": 3, "title": "ccccccc", "priority": "Medium", "category": "School", "completed": False}]

@pytest_bdd.when("User wants to see only low priority tasks")
@pytest.fixture
def filter_priority(task_set):
    task_set[:] = filter_tasks_by_priority(task_set, "Low")
    return task_set

@pytest_bdd.then("Only low priority tasks shown")
def test_priority_filtered(filter_priority):
    assert len(filter_priority) == 1



@pytest_bdd.given("Tasks have different categories")
@pytest.fixture
def tasks_for_user():
    return [{"id": 1, "title": "aaaaaaa", "priority": "Low", "category": "Personal", "completed": True},
    {"id": 2, "title": "bbbbbbb", "priority": "High", "category": "School", "completed": True}, 
    {"id": 3, "title": "ccccccc", "priority": "Medium", "category": "School", "completed": False}]

@pytest_bdd.when("User wants to see their 'School'work")
@pytest.fixture
def filter_category(tasks_for_user):
    tasks_for_user[:] = filter_tasks_by_category(tasks_for_user, "School")
    return tasks_for_user

@pytest_bdd.then("Only 'School'work displayed")
def test_category_filtered(filter_category):
    assert len(filter_category) == 2



@pytest_bdd.given("Tasks can be marked complete or not")
@pytest.fixture
def task_list():
    return [{"id": 1, "title": "aaaaaaa", "priority": "Low", "category": "Personal", "completed": True},
    {"id": 2, "title": "bbbbbbb", "priority": "High", "category": "School", "completed": True}, 
    {"id": 3, "title": "ccccccc", "priority": "Medium", "category": "School", "completed": False}]

@pytest_bdd.when("the user marks it as completed")
@pytest.fixture
def completed(task_list):
    task_list[:] = filter_tasks_by_completion(task_list, completed = True)
    return task_list

@pytest_bdd.then("the task should be marked as completed")
def test_tasks_completed(completed):
    assert len(completed) == 2


