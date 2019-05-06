
HOST=$1
shift
files=$@

confirm $HOST $files


echo "backing up the target"

ssh $HOST "export files='""$files'"';cd /opt/nginx ; \
          ARCHIVE=html-`date +%Y%m%d-%H%M%S`; \
          [ -e html  ] && cp -r  html $ARCHIVE; \
          echo  $ARCHIVE >./archive ; \
          echo "${ARCHIVE}  [ $files ]  will be updated"   >>./front_update.log'




echo "Syncing pages"

for file in $files
do
ssh $HOST "cd /opt/nginx/html/ ; rm -rf $file"
scp -r  /opt/nginx/html/$file    $HOST:/opt/nginx/html/
done



echo "Adjusting the address"
ssh $HOST "sed -i s/uat1.chinayie.com/$HOST/g"  '`grep uat1.chinayie.com -rl /opt/nginx/html/*`'


echo "部署成功!"
