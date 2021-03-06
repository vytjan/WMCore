#!/usr/bin/env python

"""
_Step.Executor.DeleteFiles_

Implementation of an Executor for a Delete step

"""
from __future__ import print_function

import logging
import signal
import traceback

import WMCore.Storage.DeleteMgr as DeleteMgr
import WMCore.Storage.FileManager
from WMCore.WMSpec.Steps.Executor import Executor
from WMCore.WMSpec.Steps.Executors.LogArchive import Alarm, alarmHandler


class DeleteFiles(Executor):
    """
    A step run to clean up the unmerged files in a job

    """

    def pre(self, emulator=None):
        """
        _pre_

        Pre execution checks

        """

        # Are we using an emulator?
        if emulator is not None:
            return emulator.emulatePre(self.step)

        logging.info("Steps.Executors.%s.pre called", self.__class__.__name__)
        return None

    def execute(self, emulator=None):
        """
        _execute_

        """

        # Are we using emulators again?
        if emulator is not None:
            return emulator.emulate(self.step, self.job)

        logging.info("Steps.Executors.%s.execute called", self.__class__.__name__)

        # Look!  I can steal from StageOut
        # DeleteMgr uses the same manager structure as StageOutMgr

        overrides = {}
        if hasattr(self.step, 'override'):
            overrides = self.step.override.dictionary_()

        # Set wait to 15 minutes
        waitTime = overrides.get('waitTime', 900)

        # Pull out StageOutMgr Overrides
        # switch between old stageOut behavior and new, fancy stage out behavior
        useNewStageOutCode = False
        if 'newStageOut' in overrides and overrides.get('newStageOut'):
            useNewStageOutCode = True

        stageOutCall = {}
        if "command" in overrides and "option" in overrides \
                and "phedex-node" in overrides \
                and "lfn-prefix" in overrides:
            stageOutCall['command'] = overrides.get('command')
            stageOutCall['option'] = overrides.get('option')
            stageOutCall['phedex-node'] = overrides.get('phedex-node')
            stageOutCall['lfn-prefix'] = overrides.get('lfn-prefix')

        # naw man, this is real
        # iterate over all the incoming files
        manager = DeleteMgr.DeleteMgr(**stageOutCall)
        manager.numberOfRetries = self.step.retryCount
        manager.retryPauseTime = self.step.retryDelay
        # naw man, this is real
        # iterate over all the incoming files
        if not useNewStageOutCode:
            # old style
            manager = DeleteMgr.DeleteMgr(**stageOutCall)
            manager.numberOfRetries = self.step.retryCount
            manager.retryPauseTime = self.step.retryDelay
        else:
            # new style
            logging.critical("DeleteFiles IS USING NEW STAGEOUT CODE")
            print("DeleteFiles IS USING NEW STAGEOUT CODE")
            manager = WMCore.Storage.FileManager.DeleteMgr(
                    retryPauseTime=self.step.retryDelay,
                    numberOfRetries=self.step.retryCount,
                    **stageOutCall)

        # This is where the deleted files go
        filesDeleted = []

        for fileDict in self.job['input_files']:
            logging.debug("Deleting LFN: %s", fileDict.get('lfn'))
            fileForTransfer = {'LFN': fileDict.get('lfn'),
                               'PFN': None,  # PFNs are assigned in the Delete Manager
                               'PNN': None,  # PNN is assigned in the delete manager
                               'StageOutCommand': None}
            filesDeleted.append(self.deleteOneFile(fileForTransfer, manager, waitTime))

        if hasattr(self.step, 'filesToDelete'):
            # files from the configTree to be deleted
            for k, v in self.step.filesToDelete.dictionary_().iteritems():
                if k.startswith('file'):
                    logging.debug("Deleting LFN: %s", v)
                    fileForTransfer = {'LFN': v,
                                       'PFN': None,
                                       'PNN': None,
                                       'StageOutCommand': None}
                    filesDeleted.append(self.deleteOneFile(fileForTransfer, manager, waitTime))

        # Now we've got to put things in the report
        for fileDict in filesDeleted:
            self.report.addRemovedCleanupFile(**fileDict)

        return

    def deleteOneFile(self, fileForTransfer, manager, waitTime):
        signal.signal(signal.SIGALRM, alarmHandler)
        signal.alarm(waitTime)

        try:
            manager(fileToDelete=fileForTransfer)
            # Afterwards, the file should have updated info.
            return fileForTransfer

        except Alarm:
            msg = "Indefinite hang during stageOut of logArchive"
            logging.error(msg)
        except Exception as ex:
            msg = "General failure in StageOut for DeleteFiles"
            msg += str(ex)
            logging.error(msg)
            logging.error("Traceback: ")
            logging.error(traceback.format_exc())
            raise

        signal.alarm(0)

    def post(self, emulator=None):
        """
        _post_

        Post execution checkpointing

        """
        # Another emulator check
        if emulator is not None:
            return emulator.emulatePost(self.step)

        logging.info("Steps.Executors.%s.post called", self.__class__.__name__)
        return None
