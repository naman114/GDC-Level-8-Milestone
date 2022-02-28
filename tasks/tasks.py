import time

from django.contrib.auth.models import User
from django.core.mail import send_mail
from tasks.models import Task
from datetime import timedelta

from celery.task import periodic_task

from task_manager.celery import app

# Scheduled / periodic tasks
@periodic_task(run_every=timedelta(seconds=10))
def send_email_reminder():
    print("Starting to process users to send emails")
    for user in User.objects.all():
        pending_tasks = Task.objects.filter(user=user, completed=False, deleted=False)
        email_content = f"You have {pending_tasks.count()} pending tasks"
        send_mail(
            "Pending tasks from Task Manager",
            email_content,
            "tasks@task_manager.org",
            [user.email],
        )
        print(f"Completed Process User {user.id}")


# Define tasks like this to start tasks dynamically
# This registers this method with celery and lets celery know that this task can be executed async in background
@app.task
def test_background_job():
    print("This is a background job!")
    for i in range(10):
        time.sleep(1)
        print(i)
