import json, rjsmin # to strip comments from the json file
import logging
import os

## Create these two exceptions for proper exception handling in the recursive funcion calls below

class JSONFileNotFoundError(Exception):
    pass

class JSONDecodeError(Exception):
    pass

log = logging.getLogger()
log.setLevel(logging.WARNING)
def loadModularJson(configFileName,baseTag='configBase'):

    """
    This method loads a json file. The reader strips comments from the json file.
    If the baseTag attribute is found in the root, the base file is loaded and
    the two files are merged. 
    If the baseTag returns a list, the first files in the list take precendence
    over the later.
    The delta file takes precedence over the base file(s).
    
    inputs:
        configFileName -- JSON file with comments
        baseTag        -- tag that indicates base file [default: configBase]

    outputs:
        config         -- dictionary from the merged JSON structure
    """
    def selective_merge(base_obj, delta_obj):
        """
        used to merge two objects
        merges delta_obj into base_obj 
        requires structural compatibility, i.e. can't merge dict into non-dict
        
        """
        if not isinstance(base_obj, dict):
            return delta_obj
        common_keys = set(base_obj).intersection(delta_obj)
        new_keys = set(delta_obj).difference(common_keys)
        for k in common_keys:
            base_obj[k] = selective_merge(base_obj[k], delta_obj[k])
        for k in new_keys:
            base_obj[k] = delta_obj[k]
        return base_obj

    
    ## load configuration
    if not isinstance(baseTag,str):
        raise TypeError('baseTag has to be a string')
    
    try:
        cfgFile = open(configFileName, mode='r') 
        strippedJSONHead = rjsmin.jsmin(cfgFile.read())
        cfgFile.close()
        configFile = json.loads(strippedJSONHead)
    except FileNotFoundError as e:
        log.error('Config file %s not found. Template can be found in conf.json.default' %(configFileName))    
        raise JSONFileNotFoundError('Config file %s not found. Template can be found in conf.json.default' %(configFileName)) from e

    confRoot = ''.join(c + '/' for c in configFileName.split('/')[:-1])

    def loadBaseFiles(deltaFile,confRoot):        
        if baseTag in deltaFile:
            # load base config
            baseConfigNames = deltaFile[baseTag]
            if isinstance(baseConfigNames,str):
                baseConfigNames = [baseConfigNames] # make it a list
            if not isinstance(baseConfigNames,list):
                raise TypeError('{} has to be a str or list'.format(baseTag))

            for baseConfigName in baseConfigNames:
                log.info("Loading base configuration file: %s", baseConfigName)
                try:
                    baseConfigPathFileName = confRoot + baseConfigName
                    cfgFile = open(confRoot+ baseConfigName, mode='r')
                    strippedJSONBase = rjsmin.jsmin(cfgFile.read())
                    cfgFile.close()
                    configBase = json.loads(strippedJSONBase)
                    confRoot = ''.join(c + '/' for c in baseConfigPathFileName.split('/')[:-1])
                    configBase = loadBaseFiles(configBase,confRoot)
                    deltaFile = selective_merge(configBase,deltaFile)
                except FileNotFoundError as e:
                    log.error('Base config file %s not found. Template can be found in conf.json.default' %(baseConfigName))    
                    raise JSONFileNotFoundError('Config file %s not found. Template can be found in conf.json.default' %(baseConfigName)) from e
                except json.JSONDecodeError as e:
                    raise JSONDecodeError('Syntax error in {}'.format(confRoot+baseConfigName),e.doc,e.pos ) from e
                    
        return deltaFile;


    
    return loadBaseFiles(configFile,confRoot)
