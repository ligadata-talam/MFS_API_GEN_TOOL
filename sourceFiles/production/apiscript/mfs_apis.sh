#!/bin/bash

export SPARK_MAJOR_VERSION=2

API_SCRIPT=@@rootPath@@/apiscript

API_CONVERT=@@rootPath@@/apiconversion

java -Xmx64g -Xms32g  -Dlog4j.configurationFile=file:$API_SCRIPT/mfs_log4j2.xml -Dlog4j2.formatMsgNoLookups=true -cp @@dependencies@@ com.ligadata.api.scripts.ApiScript --config $API_SCRIPT/config/mfs_apis_config.json --dataDates $1 --feeds $2 --deleteExtractedData true