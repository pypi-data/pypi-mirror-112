import logging.config

from modeltracker.accesslayer.dao import *
from modeltracker.dblayer.enumtypes import StateEnum

logging.getLogger(__name__)


class ModelTracker(object):

    def __init__(self, model_id: str, name: str, technique: str, version: str, code_version: str,
                 task_mode: str, modifier: str, output: dict = None):
        """
        write model details to a database by
        1) adding the model to the catalog if it is does not exist,
        2) registering the run in the model_log table
        3) adding the model output if provided
        :param model_id: a model id (e.g. 'usecaseA-H2OGBM-20180911.114c0')
        :param name: a model name ('usecaseA')
        :param technique: a technique ('h2ogbm')
        :param version: a model version (20180911)
        :param code_version: (1.1.4) --- the removal of '.' is inadequate and non unique in model_id determination - to fix
        :param state: see dblayer.enumtypes (but one of ACITVE, SUCCESS, ...)
        :param run_mode: in {PROD, DEV, PREPROD}
        :param task_mode: in {FS_TRAIN, FS_SCORE, SCORE, TRAIN)
        :param modifier: e.g. c0, for challenger 0
        :param output: a dictionary (e.g. {'HIVE': 'db/myhive/tbl1', 'UNIXFS': '/home/myhome/stores/store1.csv'}))
        :return:
        """
        self.model_id = model_id
        self.model_catalog_id = None
        self.name = name
        self.technique = technique
        self.version = version
        self.code_version = code_version
        self.task_mode = task_mode
        self.modifier = modifier
        self.output = output
        # the transactional entry for this model run
        self.job_id = -1

    def job_start(self):
        """
        start the model metrics logging process
        :return:
        """
        try:
            # get model from catalog if exists
            state = StateEnum.ACTIVE
            db_model = ModelCatalogDao.read(model_id=self.model_id, state=StateEnum.ACTIVE)

            # insert model if not exists
            if not db_model:
                print('no db_model')
                log.debug('inserting model {}'.format(self.model_id))

                self.model_catalog_id = ModelCatalogDao.write(model_id=self.model_id,
                                                      name=self.name,
                                                      model=self.technique,
                                                      version=self.version,
                                                      code_version=self.code_version,
                                                      modifier=self.modifier, state=state)
            else:
                print('found a model')
                self.model_catalog_id = db_model.model_catalog_id
                log.debug('model found for {}'.format(self.model_id))
        except Exception as e:
            log.error('failed to query state {} and insert model {}'.format(state.name, self.model_id))
            log.error(e)
            raise e

        job = None
        try:
            # insert job
            log.debug('inserting the model log entry')
            self.job_id = JobDao.write(model_catalog_id=self.model_catalog_id,
                                       task_type_id=self.task_mode,
                                       state=state)

        except Exception as e:
            log.error('state in func: {}'.format(locals()))
            log.error('failed to insert model log entry{}'.format(e))
            raise e

    def job_complete(self, state: StateEnum = StateEnum.SUCCESS):
        """
        finalise the run using the job_id derived from log_start
        :param state: default is success (successful run - else, mark as another state)
        :return:
        """
        if self.job_id < 0:
            log.error('log_start needs to be called before log_complete')
            raise Exception('programming error - please call log_start before log_complete - no log_model_id available')
        log.debug('updating {} to state {}'.format(self.job_id, state.name))
        JobDao().update(self.job_id, state)
