from modeltracker.dblayer.enumtypes import StateEnum
from modeltracker.dblayer.model import *
from modeltracker.dblayer.connection import DbSession

import pandas as pd
import logging

log = logging.getLogger(__name__)


class Dao(object):

    @staticmethod
    def write(**kwargs):
        pass

    @staticmethod
    def read(**kwargs):
        pass


class StateDao(Dao):

    @staticmethod
    def read(state: StateEnum):
        try:
            # get the state from the db
            db_state = DbSession().session.query(State).filter(State.state_id == state.name).first()
            return db_state
        except Exception as e:
            print('invalid state, does it exist in the db?')
            raise e


class JobDao(Dao):

    @staticmethod
    def write(model_catalog_id, task_type_id, state: StateEnum):
        """
        A job write inserts a model, if it is not in the catalog (this is up for debate, likely better to keep
        it simpler),
        :param model_catalog_id:
        :param task_mode:
        :param state:
        :return:
        """
        try:
            print(state)
            db_state = StateDao().read(state)

            job = Job(model_catalog_id=model_catalog_id,
                      task_type_id=task_type_id,
                      state=db_state)

            DbSession().session.add(job)
            DbSession().session.commit()
            return job.job_id
        except Exception as e:
            DbSession().session.rollback()
            log.error('failed to write to job table: {}'.format(e))
            raise e

    @staticmethod
    def update(job_id, state: StateEnum):
        """
        :param jo   b_id:
        :param state:
        :return:
        """
        try:
            db_state = StateDao().read(state)
            log.debug('updating to {}'.format(db_state.state_id))
            DbSession().session.query(Job).filter(Job.job_id == job_id).update(
                {"state_id": db_state.state_id, "last_modified_date": (datetime.utcnow())})
            DbSession().session.commit()
        except Exception as e:
            log.error('failed to update job table: {}'.format(e))
            DbSession().session.rollback()
            raise e


class ModelCatalogDao(Dao):

    @staticmethod
    def write(model_id, name, model, version, code_version, modifier, state: StateEnum):
        """
        Insert a model into the catalog
        :param usecase: use case name (e.g. usecaseA)
        :param technique:  a modelling technique
        :param model_name: a concatenation of usecase, technique version and code version to act as a self-identifier
        :param version: a model version
        :param code_version: code version
        :param modifier: a identifier modifier
        :param state: enum type in {'ACTIVE', 'DECOMMISSIONED', 'INACTIVE', ...}
        :return the model catalog id
        """
        try:
            # deal with state FK
            db_state = StateDao.read(state)
            if not db_state:
                raise Exception('State does not exist in state table')
            m = ModelCatalog(model_id=model_id,
                             usecase=name,
                             technique=model, version=version,
                             code_version=code_version, modifier=modifier, state_id=db_state.state_id)
            DbSession().session.add(m)
            DbSession().session.commit()
            return m.model_catalog_id
        except Exception as e:
            log.error('unable to add model to db: {}'.format(e))
            DbSession().session.rollback()

    @staticmethod
    def read(model_id,
             state: StateEnum = StateEnum.ACTIVE,
             name=None,
             model=None,
             version=None,
             code_version=None):
        """
        Given a model_id, or a unique combination of name, model, version, code_version,
        get the model entry
        :param model_id: the system identifier for the model
        :param name:
        :param model:
        :param version:
        :param code_version:
        :param state:
        :return:
        """
        try:
            log.debug('confirming that state exists: {}'.format(state.name))
            db_state = StateDao().read(state)
            log.debug('extracting model catalog item based on numerous keys')
            if name or model or version or code_version:
                raise NotImplementedError('We need user defined type or we unique constraint on all these values')
            else:
                db_model = DbSession().session.query(ModelCatalog).filter(ModelCatalog.model_id == model_id,
                                                                          ModelCatalog.state == db_state
                                                                          ).first()
            return db_model
        except Exception as e:
            log.error('failed to query model with local state: {}'.format(e))
            raise e

    @staticmethod
    def update_state(model_id, state: StateEnum):
        """
        :param model_id: the unique model identifier
        :param state: the enum state type
        """
        try:
            # deal with state FK
            db_state = StateDao.read(state)
            DbSession().session.query(ModelCatalog).filter(
                ModelCatalog.model_catalog.model_catalog_id == model_id).update(
                {
                    "state_id":
                        db_state.state_id,
                    "last_modified_date": (
                        datetime.utcnow())
                }
            )
            DbSession().session.commit()
        except Exception as e:
            log.error('failed to update state {}'.format(e))

    @staticmethod
    def run(model_id, state: StateEnum, model_outputs: dict):
        try:
            print('pretty sure you are never called')
            # get the state from the db
            db_state = StateDao(state)
            db_task_type = TaskType(TaskType.task_mode).read(state)

            # db_task_mode = DbSession().session.query(RunModeCategory).filter(ModelTaskCategory.id == task_mode).first()
            job = ModelCatalog(model_catalog_id=model_id,
                               model_task_category_id=db_task_type.task_type_id,
                               state_id=db_state.state_id)
            DbSession().session.add(job)
            DbSession().session.flush()
            DbSession().session.commit()

            # this would be wrapped in another api call in something that wasn't poc
            for k, v in model_outputs.items():
                db_model_output = ModelOutput(model_catalog_id=model_id,
                                              model_log_id=job.job_id,
                                              datastore_type_id=k,
                                              location=v)
            DbSession().session.add(db_model_output)
            DbSession().session.commit()

        except Exception as e:
            log.error('failed :{}'.format(e))
            DbSession().session.rollback()
            raise e


class ModelOutputDao(Dao):

    @staticmethod
    def write(model_id, job_id, datastore_dict=None):
        """
        :param model_id: a unique model identifier (e.g. 'usecaseA-H2OGBM-20180911.114c0')
        :param job_id: the model log entry integer associated with this output
        :param datastore_dict: a dictionary of datastore types and their locations (e.g.
        {'HIVE': 'db/myhive/tbl1', 'UNIXFS': '/home/myhome/stores/store1.csv'})
        """
        try:
            # is the model there?
            db_model = DbSession().session.query(ModelCatalog).filter(ModelCatalog.model_catalog_id == model_id).first()
            if not db_model:
                raise Exception('{} model id not found - consider inserting'.format(model_id))

            # is the job logged?
            db_job = DbSession().session.query(Job).filter(Job.job_id == job_id).first()
            if not db_job:
                raise Exception('{} is an invalid model job')

            # insert the output
            objects = []
            for k, v in datastore_dict.items():
                # is this a valid datastore type
                db_datastore_type = DbSession().session.query(DataStoreType).filter(
                    DataStoreType.datastore_type_id == k).first()
                if not db_datastore_type:
                    raise Exception('{} not valid datastore type - consider inserting'.format(k))
                objects.append(ModelOutput(model_catalog_id=model_id,
                                           job_id=db_job.job_id,
                                           datastore_type=db_datastore_type,
                                           location=v))
                DbSession().session.add_all(objects)
            DbSession().session.commit()

        except Exception as e:
            DbSession().session.rollback()
            log.error('failed to output for model {},  namely: {}'.format(model_id, datastore_dict))
            raise e

    @staticmethod
    def read_latest(model_id, datastore_type_id):
        return DbSession().session.query(
            ModelOutput
        ).join(DataStoreType) \
            .filter(DataStoreType.datastore_type_id == datastore_type_id) \
            .filter(ModelCatalog.model_id == model_id).order_by(ModelOutput.create_date.desc()).first()


class DataMetricsDao(Dao):

    @staticmethod
    def __formatter(data):
        """
        given a data collection, format the data as required by write
        :param data:
        :return: a generator yeilding <key, value> pairs as required by this implementation
        """
        if isinstance(data, dict):
            data_list_dict = [data]
        elif isinstance(data, list):
            data_list_dict = data
        else:
            raise NotImplementedError('unsupported data type')

        for elem in data_list_dict:
            for k, v in elem.items():
                yield k, v

    @staticmethod
    def write(model_catalog_id, job_id, data, reference_time):
        """
        given a dictionary, write it to the underlying database as key-value pairs
        where the key is the first encountered key (the values may be complex -- e.g. {'key': [{"somestuff": 1}]}
        :param model_catalog_id:
        :param job_id:
        :param data: a dictionary
        :param reference_time: your time of writing the record
        """

        insert_list = []
        for k, v in DataMetricsDao.__formatter(data):
            insert_list.append(
                DataMetrics(
                    model_catalog_id=model_catalog_id,
                    job_id=job_id,
                    key=k,
                    value=v,
                    reference_time=reference_time
                )
            )
        DbSession().session.add_all(insert_list)
        DbSession().session.commit()




