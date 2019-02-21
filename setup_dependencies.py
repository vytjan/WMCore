#!/usr/bin/env python
"""
Manage dependancies by declaring systems here.
A system can depend on packages or other systems.
If a package ends with a + include all subpackages.
"""
dependencies = {
    'wmc-rest': {
        'bin': ['wmc-dist-patch', 'wmc-dist-unpatch', 'wmc-httpd'],
        'packages': ['WMCore.REST'],
        'modules': ['WMCore.Configuration'],
        'systems': ['wmc-base']
    },
    'wmc-wmarchive': {
        'bin': ['wmc-dist-patch', 'wmc-dist-unpatch', 'wmc-httpd'],
        'packages': ['WMCore.REST', 'WMCore.Services.StompAMQ'],
        'modules': ['WMCore.Configuration'],
        'systems': ['wmc-base']
    },
    'wmc-base': {
        'bin': ['wmc-dist-patch', 'wmc-dist-unpatch'],
        'packages': ['Utils', 'WMCore.DataStructs', 'WMCore.Cache'],
        'modules': ['WMCore.WMFactory', 'WMCore.WMException', 'WMCore.Configuration',
                    'WMCore.WMExceptions', 'WMCore.WMFactory', 'WMCore.Lexicon',
                    'WMCore.WMBase', 'WMCore.WMLogging', 'WMCore.Algorithms.Permissions'],
    },
    'wmc-component': {
        'packages': ['WMCore.MsgService', 'WMCore.WorkerThreads', 'WMCore.ThreadPool'],
        'modules': ['WMComponent.__init__'],
        'systems': ['wmc-base']
    },
    'wmc-database': {
        'packages': ['WMCore.Wrappers+', 'WMCore.GroupUser', 'WMCore.DataStructs', 'WMCore.Database',
                     'WMCore.Algorithms', 'WMCore.Services'],
        'modules': ['WMCore.WMConnectionBase', 'WMCore.DAOFactory', 'WMCore.WMInit'],
        'systems': ['wmc-base']
    },
    'wmc-runtime': {
        'packages': ['WMCore.WMRuntime+', 'WMCore.WMSpec+', 'PSetTweaks',
                     'WMCore.FwkJobReport', 'WMCore.Storage+', 'WMCore.Services.HTTPS'],
        'modules': ['WMCore.Algorithms.ParseXMLFile'],
        'systems': ['wmc-base']
    },
    'wmc-web': {
        'packages': ['WMCore.WebTools', 'WMCore.Agent+', 'WMCore.WorkerThreads'],
        'systems': ['wmc-database', 'wmc-base'],
        'statics': ['src/javascript/WMCore/WebTools',
                    'src/javascript/external/yui',
                    'src/css/WMCore/WebTools',
                    'src/css/WMCore/WebTools/Masthead',
                    'src/css/external/yui',
                    'src/templates/WMCore/WebTools',
                    'src/templates/WMCore/WebTools/Masthead', ]
    },
    'reqmgr2': {
        'packages': ['WMCore.ReqMgr+',
                     'WMCore.WMDataMining+',
                     'WMCore.Services+',
                     'WMCore.ACDC',
                     'Utils'],
        'modules': ['WMCore.WorkQueue.__init__',
                    'WMCore.WorkQueue.DataStructs.__init__',
                    'WMCore.WorkQueue.DataStructs.WorkQueueElement'],
        'systems': ['wmc-rest', 'wmc-runtime', 'wmc-database'],
        'statics': ['src/couchapps/ReqMgr+',
                    'src/couchapps/ReqMgrAux+',
                    'src/couchapps/ConfigCache+',
                    'src/couchapps/WMStats+',
                    'src/couchapps/WMDataMining+',
                    'src/html/ReqMgr+'
                    ],
    },
    'reqmgr2ms': {
        'packages': ['Utils', 'WMCore.MicroService+', 'WMCore.Services+'],
        'modules': ['WMCore.Wrappers.__init__',
                    'WMCore.Wrappers.JsonWrapper.__init__',
                    'WMCore.Wrappers.JsonWrapper.JSONThunker',
                    ],
        'systems': ['wmc-rest', 'wmc-runtime'],
        'statics': [],
    },
    'workqueue': {
        'packages': ['WMCore.GlobalWorkQueue+', 'WMCore.WorkQueue+',
                     'WMCore.Wrappers+', 'WMCore.Services+',
                     'WMCore.WMSpec', 'WMCore.WMSpec.Steps', 'WMCore.WMSpec.Steps.Templates',
                     'WMCore.ACDC', 'WMCore.GroupUser'],
        'modules': ['WMCore.Algorithms.__init__', 'WMCore.Algorithms.Permissions',
                    'WMCore.Algorithms.MiscAlgos', 'WMCore.Algorithms.ParseXMLFile',
                    'WMCore.Database.__init__', 'WMCore.Database.CMSCouch',
                    'WMCore.Database.CouchUtils',
                    'WMCore.ReqMgr.__init__', 'WMCore.ReqMgr.DataStructs.__init__',
                    'WMCore.ReqMgr.DataStructs.RequestStatus',
                    'WMCore.ReqMgr.DataStructs.RequestType'],
        'systems': ['wmc-rest', 'wmc-database'],
        'statics': ['src/couchapps/WorkQueue+'],
    },
    'wmagent': {
        'packages': ['WMCore.Agent+', 'WMCore.Algorithms+',
                     'WMCore.JobStateMachine', 'WMComponent+',
                     'WMCore.ThreadPool',
                     'WMCore.BossAir+', 'WMCore.Credential',
                     'WMCore.JobSplitting+', 'WMCore.ProcessPool',
                     'WMCore.Services+', 'WMCore.WMSpec+',
                     'WMCore.WMBS+', 'WMCore.ResourceControl+'],
        'systems': ['wmc-web', 'wmc-database', 'workqueue', 'wmc-runtime'],
        'statics': ['src/javascript/WMCore/WebTools/Agent',
                    'src/javascript/WMCore/WebTools/WMBS',
                    'src/javascript/external/graphael',
                    'src/templates/WMCore/WebTools/WMBS'],
    },
    'asyncstageout': {
        'packages': ['WMCore.Agent+', 'WMCore.Storage+',
                     'WMCore.Credential', 'WMCore.WorkerThreads',
                     'WMCore.ACDC',
                     'WMCore.Services+'],
        'modules': ['WMQuality.TestInitCouchApp', 'WMCore.Services.Service',
                    'WMCore.Services.pycurl_manager', 'WMComponent.__init__'],
        'systems': ['wmc-database'],
        'statics': ['src/couchapps/Agent+'],
    },
    'crabcache': {
        'packages': ['WMCore.Wrappers+', 'WMCore.Services.UserFileCache+'],
        'systems': ['wmc-rest'],
        'modules': ['WMCore.Services.Requests', 'WMCore.Services.Service',
                    'WMCore.Services.pycurl_manager', ],
    },
    'crabserver': {
        'packages': ['WMCore.Credential', 'WMCore.Services+',
                     'WMCore.WMSpec+', 'WMCore.ACDC'],
        'modules': ['WMCore.DataStructs.LumiList'],
        'systems': ['wmc-rest', 'wmc-database'],
    },
    'crabclient': {
        'packages': ['WMCore.Wrappers+', 'WMCore.Credential', 'PSetTweaks', 'WMCore.Services.UserFileCache+',
                     'WMCore.Services.PhEDEx+', 'WMCore.Services.DBS+'],
        'systems': ['wmc-base'],
        'modules': ['WMCore.FwkJobReport.FileInfo', 'WMCore.Services.Requests', 'WMCore.DataStructs.LumiList',
                    'WMCore.Services.Service', 'WMCore.Services.pycurl_manager', ],
    },
    'crabtaskworker': {
        'packages': ['WMCore.WorkQueue', 'WMCore.Credential', 'WMCore.Algorithms+', 'WMCore.WMSpec+',
                     'WMCore.JobSplitting', 'WMCore.Services+', 'Utils+'],
        'modules': ['WMCore.WMBS.File', 'WMCore.WMBS.WMBSBase', 'WMCore.WMBS.__init__'],
        'systems': ['wmc-database', 'wmc-runtime'],
    },
    'wmclient': {
        'systems': ['wmc-runtime', 'wmc-database']
    },
    'reqmon': {
        'packages': ['WMCore.WMStats+', 'WMCore.WMDataMining+',
                     'WMCore.Services+', 'WMCore.Wrappers+',
                     'WMCore.ReqMgr.DataStructs+'
                     ],
        'modules': ['WMCore.Database.__init__', 'WMCore.Database.CMSCouch',
                    'WMCore.Database.CouchUtils', 'WMCore.ReqMgr.__init__'],
        'systems': ['wmc-base', 'wmc-rest'],
        'statics': ['src/couchapps/WMStats+',
                    'src/couchapps/WMStatsErl+',
                    'src/couchapps/WorkloadSummary+',
                    'src/couchapps/T0Request+',
                    'src/couchapps/LogDB+',
                    'src/html/WMStats+'],
    },
    'acdcserver': {
        'packages': ['WMCore.ACDC', 'WMCore.GroupUser', 'WMCore.DataStructs',
                     'WMCore.Wrappers+', 'WMCore.Database'],
        'modules': ['WMCore.Configuration',
                    'WMCore.Algorithms.ParseXMLFile', 'WMCore.Algorithms.Permissions',
                    'WMCore.Lexicon', 'WMCore.WMException', 'WMCore.Services.Requests',
                    'WMCore.Services.pycurl_manager'],
        'statics': ['src/couchapps/ACDC+',
                    'src/couchapps/GroupUser+']
    },
    't0': {
        'systems': ['wmagent']
    }
}
