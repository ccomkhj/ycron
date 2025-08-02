
import pytest
import os
import yaml
from ycron.core.yaml_loader import load_jobs_from_yaml

@pytest.fixture
def sample_yaml_config(tmp_path):
    config_content = """
jobs:
  test_job_1:
    script: scripts/script1.py
    schedule: "* * * * *"
    retries:
      attempts: 1
      delay: 60
    backfill: true
    max_parallel: 1
  test_job_2:
    script: scripts/script2.py
    schedule: "0 0 * * *"
    retries:
      attempts: 0
      delay: 0
    backfill: false
    max_parallel: 5
"""
    config_file = tmp_path / "jobs.yaml"
    config_file.write_text(config_content)
    return str(config_file)

def test_load_jobs_from_yaml(sample_yaml_config):
    jobs = load_jobs_from_yaml(sample_yaml_config)

    assert len(jobs) == 2

    job1 = next((j for j in jobs if j.name == 'test_job_1'), None)
    assert job1 is not None
    assert job1.script == 'scripts/script1.py'
    assert job1.schedule == '* * * * *'
    assert job1.retries == 1
    assert job1.retry_delay == 60
    assert job1.backfill is True
    assert job1.max_parallel == 1

    job2 = next((j for j in jobs if j.name == 'test_job_2'), None)
    assert job2 is not None
    assert job2.script == 'scripts/script2.py'
    assert job2.schedule == '0 0 * * *'
    assert job2.retries == 0
    assert job2.retry_delay == 0
    assert job2.backfill is False
    assert job2.max_parallel == 5
