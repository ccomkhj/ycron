
import pandas as pd
from ycron.storage.models import get_session, Execution, Job
from datetime import datetime, timedelta

from sqlalchemy.orm import joinedload

def generate_heatmap_data(days=7):
    session = get_session()
    try:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        jobs = session.query(Job).all()
        all_job_names = [job.name for job in jobs]
        dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days + 1)]

        all_executions = (
            session.query(Execution)
            .options(joinedload(Execution.job))
            .filter(Execution.start_time >= start_date)
            .all()
        )

        heatmap_dict = {}
        for job_name in all_job_names:
            df = pd.DataFrame(index=[job_name], columns=dates, data=0)
            heatmap_dict[job_name] = df

        for ex in all_executions:
            date_str = ex.start_time.strftime('%Y-%m-%d')
            if ex.job.name in heatmap_dict and date_str in heatmap_dict[ex.job.name].columns:
                if ex.status == 'success':
                    heatmap_dict[ex.job.name].loc[ex.job.name, date_str] = 1
                elif ex.status == 'failed':
                    heatmap_dict[ex.job.name].loc[ex.job.name, date_str] = -1

        return heatmap_dict
    finally:
        session.close()
