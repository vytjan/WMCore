#!/usr/bin/env python

import os, logging, time, random

from WMCore.DAOFactory import DAOFactory
from WMCore.WMBS.File import File
from WMCore.WMBS.Fileset import Fileset
from WMCore.WMBS.Job import Job
from WMCore.WMBS.Subscription import Subscription
from WMCore.WMBS.JobGroup import JobGroup
from WMCore.WMBS.Workflow import Workflow
from sets import Set

class Base_t():
    """
    __Base_t__

    Base class for Performance Tests at WMBS

    This class is abstract, proceed to the DB specific testcase
    to run the test


    """

    def setUp(self, dbf):
        """
        Common setUp for all Performance tests

        """
        
        #Setting up logger
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='%s.log' % __file__.replace('.py',''),
                    filemode='w')
        self.logger = logging.getLogger('BasePerformanceTest')
        #Place common execute method arguments here        
        #TODO -Still to be implemented
        self.baseexec=''

        #possibly deprecated, need to use selist instead
        self.sename='localhost'        
        
        self.tearDown()

        self.dbf=dbf

        self.dao = DAOFactory(package='WMCore.WMBS', logger=self.logger, 
                        dbinterface=self.dbf.connect())
        
        assert self.dao(classname='CreateWMBS').execute()       

        #Creating the Locations at the Database
        self.selist = ['localhost']        
        for se in self.selist:
            self.dao(classname='Locations.New').execute(sename=se)      

        # Create a File to be used as argument for the performance test
        file_lfn = '/tmp/file/fileexample'
        file_events = 1111
        file_size = 1111
        file_run = 111
        file_lumi = 0
        
        self.testFile = File(lfn=file_lfn, size=file_size, events=file_events, run=file_run,
                    lumi=file_lumi, logger=self.logger, dbfactory=self.dbf)
        self.testFile.save()
        self.testFile.load()

        # Create a Fileset of random, parentless, childless, unlocatied file
        filelist = []

        #Generating Files        
        for x in range(random.randint(1000,3000)):
            file = File(lfn='/store/data/%s/%s/file.root' % (random.randint(1000, 9999), 
                                                  random.randint(1000, 9999)),
                        size=random.randint(1000, 2000),
                        events = 1000,
                        run = random.randint(0, 2000),
                        lumi = random.randint(0, 8), 
                        logger=self.logger, 
                        dbfactory=self.dbf)
            
            filelist.append(file)
    
        #Creating mySQL Fileset        
        self.testFileset = Fileset(name='testFileSet', 
                            files=filelist, 
                            logger=self.logger, 
                            dbfactory=self.dbf) 
        self.testFileset.create()     

        #Creating mySQL Workflow
        self.testWorkflow = Workflow(spec='Test', owner='PerformanceTestCase', name='TestWorkflow', logger=self.logger, dbfactory=self.dbf)
        self.testWorkflow.create()

        #Creating MySQL Subscription
        self.testSubscription = Subscription(fileset=self.testFileset, 
                        workflow=self.testWorkflow, logger=self.logger, 
                        dbfactory=self.dbf)
        self.testSubscription.create()

        #Instatiating mySQL Job
        self.testJob = Job(name='TestJob',files=self.testFileset, logger=self.logger, dbfactory=self.dbf)

        #Creating mySQL JobGroup
        testSet = Set()
        testSet.add(self.testJob)
        self.testJobGroup = JobGroup(subscription=self.testSubscription, jobs=testSet)

        #Creating mySQL Job for testing
        self.testJob.create(group=self.testJobGroup.id)


    def tearDown(self):
        #Base tearDown method for the DB Performance test
        pass

    
    def perfTest(self, dao, action, **input):
        """
        Method that executes a dao class operation and measures its
        execution time.
        
        """
        #Test each of the DAO classes of the specific WMBS class directory        
        action = dao(classname=action)
        string = ""
        for i in input.keys():
            if type(input[i]) == type('string'):
                string = "%s %s='%s'," % (string, i, input[i])
            else:
                string = "%s %s=%s," % (string, i, input[i])
        string = string.strip()
        string = string.rstrip(",")
        string = "action.execute(%s)" % string
        self.logger.debug('the final string: %s' % string)
        startTime = time.time()               
        #Place execute method of the specific classname here
        #string = compile(string)
        eval(string)
        endTime = time.time()
        diffTime = endTime - startTime
        
        return diffTime
