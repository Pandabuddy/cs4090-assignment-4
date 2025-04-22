import pytest
import subprocess
from src.tasks import load_tasks, filter_tasks_by_priority

def test_cov():
    result = subprocess.run(["pytest", "--cov=../src/tasks  --cov-report=term-missing"], capture_output=True, text=True)
    return result.stdout, result.stderr

@pytest.mark.parametrize("tasks, priority, expected_count", [
    ([{"priority": "High"}, {"priority": "Medium"}, {"priority": "Low"}], "High", 1),
    ([{"priority": "High"}, {"priority": "High"}, {"priority": "Low"}], "High", 2),
    ([], "Medium", 0),
])
def test_parametrize(tasks, priority, expected_count):
    filtered = filter_tasks_by_priority(tasks, priority)
    assert len(filtered) == expected_count

def test_mock(mocker):
    mock_load = mocker.patch("src.tasks.load_tasks")
    tasks = load_tasks()
    assert len(tasks) == 3

def test_hmtl_report():
    result = subprocess.run(["pytest", "--html=report.html"], capture_output=True, text=True)
    return result.stdout, result.stderr