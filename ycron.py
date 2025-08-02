
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
from ycron.core.yaml_loader import load_jobs_from_yaml
from ycron.core.scheduler import start_scheduler, run_job
from ycron.storage.models import get_session, Job
from ycron.gui.app import app
from croniter import croniter
from datetime import datetime

def main():
    # Load jobs from YAML
    jobs = load_jobs_from_yaml('ycron/config/jobs.yaml')

    # Store jobs in the database
    session = get_session()
    try:
        for job in jobs:
            existing_job = session.query(Job).filter_by(name=job.name).first()
            if existing_job:
                existing_job.script = job.script
                existing_job.schedule = job.schedule
                existing_job.retries = job.retries
                existing_job.retry_delay = job.retry_delay
                existing_job.backfill = job.backfill
                existing_job.max_parallel = job.max_parallel
            else:
                session.add(job)
        session.commit()
        db_jobs = session.query(Job).all()

        # Backfill logic
        for job in db_jobs:
            if job.backfill and job.last_run:
                base_time = job.last_run
                now = datetime.utcnow()
                if job.schedule:
                    cron = croniter(job.schedule, base_time)
                    for schedule_time in cron.all_next(datetime):
                        if schedule_time > now:
                            break
                        run_job(job.id)

        # Update last_run for all jobs
        for job in db_jobs:
            job.last_run = datetime.utcnow()
        session.commit()
        job_ids_for_scheduler = [job.id for job in db_jobs]
    finally:
        session.close()

    # Start the scheduler
    start_scheduler(job_ids_for_scheduler)

    # Start the Flask app
    app.run(debug=True, use_reloader=False, host='0.0.0.0') # use_reloader=False to avoid running scheduler twice

if __name__ == '__main__':
    main()
