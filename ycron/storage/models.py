
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    script = Column(String, nullable=False)
    schedule = Column(String, nullable=False)
    retries = Column(Integer, default=0)
    retry_delay = Column(Integer, default=0)
    backfill = Column(Boolean, default=False)
    max_parallel = Column(Integer, default=1)
    last_run = Column(DateTime)
    executions = relationship("Execution", back_populates="job")

class Execution(Base):
    __tablename__ = 'executions'
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'))
    job = relationship("Job", back_populates="executions")
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime)
    status = Column(String, nullable=False) # running, success, failed
    output = Column(String)

    def status_class(self):
        if self.status == 'success':
            return 'success'
        elif self.status == 'failed':
            return 'danger'
        else:
            return 'info'

def get_session(db_path='ycron.db'):
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
