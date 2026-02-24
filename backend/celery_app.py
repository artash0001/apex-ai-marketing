from celery import Celery
from celery.schedules import crontab
import os

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
celery_app = Celery("apex_digital", broker=redis_url, backend=redis_url)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "daily-content-generation": {
            "task": "tasks.content_tasks.generate_daily_content",
            "schedule": crontab(hour=6, minute=0),
        },
        "weekly-reports": {
            "task": "tasks.reporting_tasks.generate_weekly_reports",
            "schedule": crontab(day_of_week=1, hour=8, minute=0),
        },
        "outreach-followups": {
            "task": "tasks.outreach_tasks.send_outreach_followups",
            "schedule": crontab(hour=9, minute=0, day_of_week="1-5"),
        },
        "daily-maintenance": {
            "task": "tasks.maintenance_tasks.daily_cleanup",
            "schedule": crontab(hour=2, minute=0),
        },
    },
)
