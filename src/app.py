import streamlit as st
import pandas as pd
from datetime import datetime
from tasks import load_tasks, save_tasks, filter_tasks_by_priority, filter_tasks_by_category
import subprocess

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tests.test_advanced import test_cov, test_hmtl_report

def main():
    st.title("To-Do Application")
    
    # Load existing tasks
    tasks = load_tasks()
    
    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")
    
    # Task creation form
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"])
        task_due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")
        
        if submit_button and task_title:
            new_task = {
                "id": len(tasks) + 1,
                "title": task_title,
                "description": task_description,
                "priority": task_priority,
                "category": task_category,
                "due_date": task_due_date.strftime("%Y-%m-%d"),
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            tasks.append(new_task)
            save_tasks(tasks)
            st.sidebar.success("Task added successfully!")
    
    # Main area to display tasks
    st.header("Your Tasks")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(set([task["category"] for task in tasks])))
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    
    show_completed = st.checkbox("Show Completed Tasks")
    
    # Apply filters
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]
    
    # Display tasks
    for task in filtered_tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            if task["completed"]:
                st.markdown(f"~~**{task['title']}**~~")
            else:
                st.markdown(f"**{task['title']}**")
            if "description" in task and task["description"]:
                st.write(task["description"])
            if "due_date" in task and task["due_date"]:
                st.caption(f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}")
            else:
                st.caption(f"Due: None | Priority: {task['priority']} | Category: {task['category']}")
        with col2:
            if st.button("Complete" if not task["completed"] else "Undo", key=f"complete_{task['id']}"):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["completed"] = not t["completed"]
                        save_tasks(tasks)
                        st.rerun()
            if st.button("Delete", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                for i, task in enumerate(tasks):
                    task["id"] = i + 1
                save_tasks(tasks)
                st.rerun()

    st.subheader("Run Tests")

    if st.button("Run Unit Tests"):
        result = subprocess.run(["pytest", "../tests/test_basic.py"], capture_output=True, text=True)
        st.sidebar.text_area("Test Output", result.stdout)
        if result.stderr:
            st.sidebar.text_area("Errors", result.stderr)

    if st.button("Pytest Cov"):
        stdout, stderr = test_cov()
        st.sidebar.text_area("Test Output", stdout)
        if stderr:
            st.sidebar.text_area("Errors", stderr)

    if st.button("Run Parameterized Test"):
        result = subprocess.run(["pytest", "-v", "../tests/test_advanced.py::test_parametrize"], capture_output=True, text=True)
        st.sidebar.text_area("Test Output", result.stdout)
        if result.stderr:
            st.sidebar.text_area("Errors", result.stderr)

    if st.button("Run Mock Test"):
        result = subprocess.run(["pytest", "../tests/test_advanced.py::test_mock"], capture_output=True, text=True)
        st.sidebar.text_area("Test Output", result.stdout)
        if result.stderr:
            st.sidebar.text_area("Errors", result.stderr)

    if st.button("HTML Report"):
        stdout, stderr = test_hmtl_report()
        st.sidebar.text_area("Test Output", stdout)
        if stderr:
            st.sidebar.text_area("Errors", stderr)

    if st.button("Run BDD Tests"):
        result = subprocess.run(["pytest", "../tests/feature/steps/test_add_steps.py"], capture_output=True, text=True)
        st.sidebar.text_area("Test Output", result.stdout)
        if result.stderr:
            st.sidebar.text_area("Errors", result.stderr)

if __name__ == "__main__":
    main()