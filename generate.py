# File: generate.py

from zipfile  import ZipFile
from datetime import datetime
import shutil
import json
import os
import re

goOn = 1
parentDirectory = os.getcwd()


def updateFile(filePath):
    try:
        file = open(filePath, 'r+')
        content = file.read()
        result = re.search('@@(.*)@@', content)
        while result != None:
            if (result.group(1) == 'dependencies'):
                deps = ''
                for dependency in vars['dependencies']:
                    deps = deps +  '$API_CONVERT/lib/' + dependency + ':'
                deps = deps[:-1]
                content = content.replace('@@' + result.group(1) + '@@', deps)
            elif result.group(1) == "extractLib":
                content = content.replace('@@' + result.group(1) + '@@', vars['rootPath'] + '/apiextraction/lib/' + vars[result.group(1)])
            elif result.group(1) == "convertLib":
                content = content.replace('@@' + result.group(1) + '@@', vars['rootPath'] + '/apiconversion/lib/' + vars[result.group(1)])
            elif result.group(1) == "parentRoot":
                parentRoot = vars['rootPath'][0:vars['rootPath'].rindex('/')]
                parentRoot = parentRoot[0:parentRoot.rindex('/') + 1]
                content = content.replace('@@' + result.group(1) + '@@', parentRoot)
            else:
                content = content.replace('@@' + result.group(1) + '@@', vars[result.group(1)])
            result = re.search('@@(.*)@@', content)
        
        file.seek(0)
        file.write(content)
        file.truncate()
    except FileNotFoundError:
        print("mfs_apis.sh does not exist")
        goOn = 0
    return


##  1. Start Reeding config_vars.json  ##
if(goOn):
    try:
        with open(parentDirectory + '/config_vars.json') as jsonFile:
            vars = json.load(jsonFile)
            jsonFile.close()
    except FileNotFoundError:
        print("config_vars.json does not exist")
        goOn = 0
##  1. Done  Reeding config_vars.json  ##


##  2. Start Creating Configaration Copy  ##
if(goOn):
    sourceDirectory = 'mfs_config_' + datetime.now().strftime("%d%m%Y%H%M%S")
    try:
        with ZipFile('sourceFiles.zip', 'r') as zip:
            zip.extractall(parentDirectory + '/' + sourceDirectory)
        os.chdir(sourceDirectory)
    except FileNotFoundError:
        print("sourceConfig.zip does not exist")
        goOn = 0
##  2. Done  Creating Configaration Copy  ##


##  3. Start Updating Files  ##
if(goOn):
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            updateFile(root + '/' + file)
##  3. Done  Updating Files  ##


##  4. Start Creating Directories  ##
if(goOn):
    if not os.path.exists(vars['rootPath'] + '/apidata/cdrs/mobile_lending_report_adept/summary'):
        os.makedirs(vars['rootPath'] + '/apidata/cdrs/mobile_lending_report_adept/summary')
    if not os.path.exists(vars['rootPath'] + '/apidata/cdrs/mobile_lending_report_adept/Daily'):
        os.makedirs(vars['rootPath'] + '/apidata/cdrs/mobile_lending_report_adept/Daily')
    if not os.path.exists(vars['rootPath'] + '/apidata/cdrs/mobile_lending_report/summary'):
        os.makedirs(vars['rootPath'] + '/apidata/cdrs/mobile_lending_report/summary')
    if not os.path.exists(vars['rootPath'] + '/apidata/cdrs/mobile_lending_report/Daily'):
        os.makedirs(vars['rootPath'] + '/apidata/cdrs/mobile_lending_report/Daily')
    if not os.path.exists(vars['rootPath'] + '/apiscript/config'):
        os.makedirs(vars['rootPath'] + '/apiscript/config')
    if not os.path.exists(vars['rootPath'] + '/apiextraction/config'):
        os.makedirs(vars['rootPath'] + '/apiextraction/config')
    if not os.path.exists(vars['rootPath'] + '/apiconversion/config'):
        os.makedirs(vars['rootPath'] + '/apiconversion/config')
    if not os.path.exists(vars['rootPath'] + '/apiconversion/logs'):
        os.makedirs(vars['rootPath'] + '/apiconversion/logs')
    if not os.path.exists(vars['rootPath'] + '/apilogs/mfs_api_logs'):
        os.makedirs(vars['rootPath'] + '/apilogs/mfs_api_logs')
    if not os.path.exists(vars['rootPath'] + '/apilogs/mfs_ext_audit_grp'):
        os.makedirs(vars['rootPath'] + '/apilogs/mfs_ext_audit_grp')
##  4. Done  Creating Directories  ##


##  5. Start Copying Files  ##
if(goOn):
    try:
        for root, dirs, files in os.walk(os.getcwd() + '/production'):
            for file in files:
                fileFullPath = os.path.join(root, file)
                shutil.copyfile(fileFullPath, vars['rootPath'] + fileFullPath[fileFullPath.rindex('production')+10:len(fileFullPath)])
        os.chdir('webapps')
        for nodeIP in vars["tomcatNodes"]:
            os.system('scp -r * daasuser@' + nodeIP + ':' + vars["classesPath"])
    except NotADirectoryError:
        print("Some directories is missing")
    except PermissionError:
        print("Some permissions is missing")
##  5. Done  Copying Files  ##
