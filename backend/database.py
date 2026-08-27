from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:////job_applications.db', echo=True)

Base = declarative_base()

class JobApplications(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    applied_at = Column(DateTime, nullable=False)
    source = Column(String, nullable=False)
    active = Column(Boolean, nullable=True)
    email_id = Column(String)
    email_subject = Column(String)
    phone = Column(String)
    pdf_path = Column(String)
    created_at = Column(DateTime)

Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)




print("Database and table created successfully")