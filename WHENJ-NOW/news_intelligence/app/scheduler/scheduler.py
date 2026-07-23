from apscheduler.schedulers.background import BackgroundScheduler

from main import run_pipeline
from app.logging.logger import logger


from datetime import timezone, timedelta

ist = timezone(timedelta(hours=5, minutes=30))
scheduler = BackgroundScheduler(timezone=ist)

# Run at 7:00, 12:00, 17:00, 21:00 (system local time — IST)
scheduler.add_job(run_pipeline, "cron", hour=7,  minute=0, id="earlymorning")
scheduler.add_job(run_pipeline, "cron", hour=7,  minute=53, id="morning")
scheduler.add_job(run_pipeline, "cron", hour=12, minute=0, id="noon")
scheduler.add_job(run_pipeline, "cron", hour=15, minute=0, id="afternoon")
scheduler.add_job(run_pipeline, "cron", hour=18, minute=0, id="evening")
scheduler.add_job(run_pipeline, "cron", hour=21, minute=0, id="night")

logger.info("Scheduler configured — pipeline runs at 07:00, 12:00, 17:00, 21:00 (IST).")