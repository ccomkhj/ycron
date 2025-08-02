
from apscheduler.schedulers.background import BackgroundScheduler
from ycron.storage.models import get_session, Execution, Job
import subprocess
import datetime

import time

def run_job(job_id):
    session = get_session()
    try:
        job = session.query(Job).get(job_id)
        if not job:
            return
        
        for i in range(job.retries + 1):
            execution = Execution(job=job, status='running')
            session.add(execution)
            session.commit()

            try:
                result = subprocess.run(['python3', job.script], capture_output=True, text=True, check=True)
                execution.status = 'success'
                execution.output = result.stdout
            except subprocess.CalledProcessError as e:
                execution.status = 'failed'
                execution.output = e.stderr
            finally:
                execution.end_time = datetime.datetime.utcnow()
                session.commit()
                if execution.status == 'success':
                    break # Break the loop if successful
                elif i < job.retries:
                    time.sleep(job.retry_delay)
    finally:
        session.close()

    session.close()

def start_scheduler(job_ids):
    scheduler = BackgroundScheduler()
    session = get_session()
    try:
        for job_id in job_ids:
            job = session.query(Job).get(job_id)
            if job:
                scheduler.add_job(run_job, 'cron', **cron_to_dict(job.schedule), args=[job.id], max_instances=job.max_parallel)
    finally:
        session.close()
    scheduler.start()

def cron_to_dict(cron_str):
    parts = cron_str.split()
    return {
        'minute': parts[0],
        'hour': parts[1],
        'day': parts[2],
        'month': parts[3],
        'day_of_week': parts[4]
    }
