
from sqlalchemy.orm import create_session
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
import argparse
import logging
log = logging.getLogger()
log.addHandler(logging.StreamHandler())
import modeltracker.dblayer.populate
import modeltracker.settings_local as settings


from modeltracker.dblayer.model import BaseSQL, metadata, DataStoreType
from modeltracker.dblayer.model import ModelCatalog, Job, ModelOutput


def insert_model():

    m = ModelCatalog(
                        usecase='usecase',
                        technique='GBM',
                        version='20180911',
                        code_version='1.1.4',
                        modifier='x',
                        state_id='ACTIVE')
    session.add(m)
    session.commit()
    print('model {} inserted'.format(m.model_catalog_id))
    return m.model_catalog_id


def insert_data(model_catalog_id):

    job = Job(model_catalog_id=model_catalog_id,
              task_type_id='TRAIN',
              state_id='SUCCESS')
    print('the job id is {}'.format(job.model_catalog_id))

    session.add(job)
    session.flush()

    # add the output
    d = session.query(DataStoreType).filter(DataStoreType.datastore_type_id == 'hive').first()
    # d = DataStoreType(id='hdfs')
    model_output = ModelOutput(model_catalog_id=model_catalog_id, model_log_id=job.job_id,
                               datastore_type=d,
                               location='/hdfs/some/place')
    session.add(model_output)
    model_output = ModelOutput(model_catalog_id=model_catalog_id, model_log_id=job.job_id,
                               datastore_type=d,
                               location='/hdfs/some/other/place')
    session.add(model_output)
    session.commit()

    for j in session.query(Job).all():
        print(j)


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Welcome to the model tracker cli - play nice')
    parser.add_argument('-r', '--remove', action='store_const', const=True,
                        help='truncate all tables')

    args = parser.parse_args()

    import modeltracker.dblayer.connection

    tracker_obj = modeltracker.dblayer.connection.DbSession(**settings.DATABASE)
    session = tracker_obj.session
    engine = tracker_obj.engine

    from modeltracker.dblayer.model import BaseSQL

    if args.remove:
        print('truncating database')
        import contextlib
        meta = MetaData(bind=engine)
        meta.reflect(bind=engine)
        with contextlib.closing(engine.connect()) as con:
            trans = con.begin()
            for table in reversed(meta.sorted_tables):
                print('removing {}'.format(table))
                con.execute(table.delete())
            print('done')
            trans.commit()
    else:
        BaseSQL.metadata.create_all(engine)
        modeltracker.dblayer.populate.state(session)
        modeltracker.dblayer.populate.datastore_type(session)
        modeltracker.dblayer.populate.model_task_category(session)
        # model_catalog_id = insert_model()
        # insert_data(model_catalog_id)

    print('---DONE---')
