from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column, Table, MetaData, ForeignKey, UniqueConstraint
from sqlalchemy.types import Integer, Date, String, Time, Float, DateTime, Binary, SmallInteger, BLOB, JSON

from datetime import datetime

BaseSQL = declarative_base()
metadata = MetaData()


def _rename_dict_keys(d, map={}):

    if map:
        new_dict = dict((map.get(key, key), value) for (key, value) in d.items())
        return new_dict
    else:
        return d


class TaskType(BaseSQL):

    __tablename__ = 'task_type'

    task_type_id = Column(String(16), primary_key=True)
    description = Column(String(255))
    create_date = Column(DateTime, default=datetime.utcnow)
    last_modified_date = Column(DateTime, default=datetime.utcnow)
    state_id = Column(String(16), ForeignKey('state.state_id'), nullable=False)
    state = relationship('State')


class State(BaseSQL):

    __tablename__ = 'state'
    state_id = Column(String(8), primary_key=True)
    description = Column(String(255))
    create_date = Column(DateTime, default=datetime.utcnow)
    last_modified_date = Column(DateTime, default=datetime.utcnow)


class DataStoreType(BaseSQL):

    __tablename__ = 'datastore_type'

    datastore_type_id = Column(String(20), primary_key=True)
    create_date = Column(DateTime, default=datetime.utcnow)
    last_modified_date = Column(DateTime, default=datetime.utcnow)
    state_id = Column(String(16), ForeignKey('state.state_id'), nullable=False)
    state = relationship('State')


class ModelCatalog(BaseSQL):

    __tablename__ = 'model_catalog'

    model_catalog_id = Column(Integer, primary_key=True)
    model_id = Column(String(64), unique=True)
    usecase = Column(String(16))
    technique = Column(String(16))
    version = Column(String(16))
    code_version = Column(String(16))
    modifier = Column(String(16))
    create_date = Column(DateTime, default=datetime.utcnow)
    last_modified_date = Column(DateTime, default=datetime.utcnow)
    state_id = Column(String(16), ForeignKey('state.state_id'), nullable=False)
    state = relationship('State')


class Job(BaseSQL):

    __tablename__ = 'job'

    job_id = Column(Integer, primary_key=True)
    model_catalog_id = Column(Integer, ForeignKey('model_catalog.model_catalog_id'), nullable=False)
    model_catalog = relationship("ModelCatalog")
    task_type_id = Column(String(16), ForeignKey('task_type.task_type_id'), nullable=False)
    task_type = relationship("TaskType")
    create_date = Column(DateTime, default=datetime.utcnow)
    last_modified_date = Column(DateTime, default=datetime.utcnow)
    state_id = Column(String(16), ForeignKey('state.state_id'), nullable=False)
    state = relationship('State')

    def __repr__(self):
        return "<job> %s %s " % (self.job_id, self.model_catalog_id )

    def row2dict(row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = getattr(row, column.name)

        return d


class ModelOutput(BaseSQL):

    __tablename__ = 'model_output'

    model_output_id = Column(Integer, primary_key=True)
    model_catalog_id = Column(Integer, ForeignKey('model_catalog.model_catalog_id'))
    model_catalog = relationship("ModelCatalog")
    job_id = Column(Integer, ForeignKey('job.job_id'))
    job = relationship('Job')
    datastore_type_id = Column(String(20), ForeignKey('datastore_type.datastore_type_id'))
    datastore_type = relationship("DataStoreType")
    location = Column(String(255))
    create_date = Column(DateTime, default=datetime.utcnow)
    last_modified_date = Column(DateTime, default=datetime.utcnow)


class DataMetrics(BaseSQL):

    __tablename__ = 'data_metrics'

    data_metrics_id = Column(Integer, primary_key=True)
    model_catalog_id = Column(Integer, ForeignKey('model_catalog.model_catalog_id'))
    model_catalog = relationship("ModelCatalog")
    job_id = Column(Integer, ForeignKey('job.job_id'))
    job = relationship('Job')
    key = Column(String(32))
    value = Column(JSON)
    create_date = Column(DateTime, default=datetime.utcnow)
    reference_time = Column(DateTime, default=datetime.utcnow)


