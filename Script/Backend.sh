#!/usr/bin/bash
source  /opt/lib.sh
env_check $#
HOST=$1
shift
FILES=$@
confirm $HOST $FILES
HOME="/opt/chinayie"
declare  -A JARS
JARS[$HOME/trade]=trades
JARS[$HOME/trade-task]=trade_task
JARS[$HOME/payment]=gy_pay
JARS[$HOME/point-mall]=point_mall
JARS[$HOME/common-service]=common_service
JARS[$HOME/platform-mgmt]=platform_mgmt
JARS[$HOME/socketIO-server]=socketIO_server
JARS[$HOME/rating-client]=rating_client
JARS[$HOME/batch-task]=batch_task
JARS[$HOME/rating-mgmt]=rating_mgmt
JARS[$HOME/gy-erp]=gy_erp
JARS[$HOME/crm-ser]=crm-ser
JARS[$HOME/scs-server]=scs_server

ssh $HOST "export files='""$FILES'"';records=backend-`date +%Y%m%d-%H%M%S`; \
           echo "${records} [ ${files}  ]  will be updated" >> /opt/chinayie/backend_update.logs '


sync_to()
{
 # sour=$1
  for jar  in $FILES
  do
    jarpath="${HOME}/${jar}"
    MOD=${JARS[$jarpath]}
    filename=$(jps | grep -o "${MOD}.*")
    file=${jarpath}"/${filename}"
    echo $file
    scp $file $HOST:${jarpath}/
    ssh $HOST "bash ${jarpath}/run.sh"
  done
}

sync_to

#case $HOST in
#  "192.168.10.34")
#  sync_to 192.168.10.132
#  ;;
#  "uat1.chinayie.com")
#  sync_to uat1.chinayie.com
#  ;;
#  "www.chinayie.com")
#  sync_to uat1.chinayie.com
#  ;;
#esac
