#host="uat1.chinayie.com"
#host="uat1.chinayie.com"
host="uat1.chinayie.com"

host10='uat1.chinayie.com'


#sed -i "s/  /${host}/g" `grep 192.168.10.132 -rl /opt/nginx/html/*`

declare -A jars
jars[8081]=trade
jars[8080]=common-service
jars[8082]=platform-mgmt
jars[8083]=rating-mgmt
jars[8084]=rating-client
jars[8086]=point-mall
jars[8091]=crm-ser
jars[8094]=payment
jars[8095]=gy-erp
jars[9092]=socketio
jars[8098]=scs-server


for i in ${!jars[*]}
do
port=$i
#sed -i   "s/http:\/\/${host}:${port}/https:\/\/${host10}\/api\/${jars[$port]}/g"   `grep http:\/\/${host}\:${port}    -rl ll /opt/nginx/html0411/html/*`
#sed -i   "s/http:\/\/${host}:${port}/https:\/\/${host10}\/api\/${jars[$port]}/g"   `grep http:\/\/${host}\:${port}    -rl /opt/nginx/html/erp/*`
sed -i   "s/http:\/\/${host}:${port}/https:\/\/${host10}\/api\/${jars[$port]}/g"   `grep http:\/\/${host}\:${port}    -rl /opt/nginx/html/*`
done

#sed -i   "s/http:\/\/pic.chinayie.com/https:\/\/pic3.chinayie.com/g"   `grep http:\/\/pic.chinayie.com   -rl ll /opt/nginx/html0411/html/*`
#sed -i   "s/http:\/\/pic.chinayie.com/https:\/\/pic3.chinayie.com/g"   `grep http:\/\/pic.chinayie.com   -rl  /opt/nginx/html/erp/*`
sed -i   "s/http:\/\/pic.chinayie.com/https:\/\/pic3.chinayie.com/g"   `grep http:\/\/pic.chinayie.com   -rl  /opt/nginx/html/*`

#sed -i "s/http:\/\/${host}/https:\/\/${host10}/"     /opt/nginx/html10/im/static/scripts/gyim.js

#sed -i   "s/https:\/\/${host}\/api\/socketio/https:\/\/${host}:9092/g"   `grep https:\/\/${host}\/api\/socketio    -rl  /opt/nginx/html/erp/*`
sed -i   "s/https:\/\/${host}\/api\/socketio/https:\/\/${host}:9092/g"   `grep https:\/\/${host}\/api\/socketio    -rl  /opt/nginx/html/*`

