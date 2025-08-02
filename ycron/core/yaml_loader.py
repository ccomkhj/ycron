
import yaml
from ycron.storage.models import Job

def load_jobs_from_yaml(path):
    with open(path, 'r') as f:
        config = yaml.safe_load(f)

    jobs = []
    for job_name, job_data in config.get('jobs', {}).items():
        job = Job(
            name=job_name,
            script=job_data.get('script'),
            schedule=job_data.get('schedule'),
            retries=job_data.get('retries', {}).get('attempts', 0),
            retry_delay=job_data.get('retries', {}).get('delay', 0),
            backfill=job_data.get('backfill', False),
            max_parallel=job_data.get('max_parallel', 1)
        )
        jobs.append(job)
    return jobs
