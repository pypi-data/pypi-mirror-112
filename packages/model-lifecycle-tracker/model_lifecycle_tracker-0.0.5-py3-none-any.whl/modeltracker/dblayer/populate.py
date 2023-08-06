from modeltracker.dblayer.model import DataStoreType, State, TaskType
from modeltracker.dblayer.enumtypes import StateEnum


def datastore_type(session):
    """
    Populate data store types upfront
    :param session:
    :return:
    """
    active = session.query(State).filter(State.state_id == 'ACTIVE').first()
    session.flush()
    objects = [DataStoreType(datastore_type_id='BIGQUERY', state=active),
               DataStoreType(datastore_type_id='GCS', state=active)]

    session.add_all(objects)
    session.commit()


def state(session):
    """
    populate the state table on first run
    :param session:
    :return:
    """
    objects = [State(state_id=StateEnum.ACTIVE.name, description='object/task/process is active'),
               State(state_id=StateEnum.INACTIVE.name, description='object/task/process has been taken out of service'),
               State(state_id=StateEnum.SUCCESS.name,
                     description='object/task/process is task/process completed successfully'),
               State(state_id=StateEnum.FAIL.name, description='task/process failed')
               ]
    session.add_all(objects)
    session.commit()


def model_task_category(session):
    active = session.query(State).filter(State.state_id == 'ACTIVE').first()
    objects = [TaskType(task_type_id='TRAIN', description='perform model training', state=active),
               TaskType(task_type_id='FS_TRAIN', description='build a training feature store', state=active),
               TaskType(task_type_id='FS_SCORE', description='build a scoring feature store', state=active),
               TaskType(task_type_id='SCORE', description='build a score store', state=active),
               TaskType(task_type_id='PREPARED_LAYER', description='build a prepared layer', state=active),
               TaskType(task_type_id='FS_DECIDE', description='build a decision feature store', state=active),
               TaskType(task_type_id='DECIDE', description='build a decision store', state=active)
               ]
    session.add_all(objects)
    session.commit()
