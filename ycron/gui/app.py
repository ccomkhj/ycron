
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.orm import joinedload
from ycron.storage.models import get_session, Job, Execution
from ycron.visualization.heatmap import generate_heatmap_data
from ycron.core.scheduler import run_job

app = Flask(__name__)

@app.route('/')
def index():
    session = get_session()
    try:
        jobs = session.query(Job).all()
        for job in jobs:
            job.last_execution = session.query(Execution).filter_by(job_id=job.id).order_by(Execution.start_time.desc()).first()

        job_name_filter = request.args.get('job_name')
        executions_query = session.query(Execution).options(joinedload(Execution.job)).order_by(Execution.start_time.desc())
        if job_name_filter:
            executions_query = executions_query.join(Job).filter(Job.name == job_name_filter)
        executions = executions_query.all()

        heatmap_data = generate_heatmap_data()
        return render_template('index.html', jobs=jobs, executions=executions, heatmap_data=heatmap_data, job_name_filter=job_name_filter)
    finally:
        session.close()

@app.route('/trigger_job', methods=['POST'])
def trigger_job():
    job_name = request.form['job_name']
    session = get_session()
    try:
        job = session.query(Job).filter_by(name=job_name).first()
        if job:
            run_job(job.id)
    finally:
        session.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
