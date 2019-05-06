# To retrive the filename, which contains the max build_number

get_file() {
       DIR=$1
       MOD=$2

      # BUILD=`eval  ls -l  $DIR | awk "/$MOD-[0-9]+\-[0-9]+\.jar"'/ {print $9}' \
      #           | awk -F- '{print $2}' |sort -n | tail -n1`
       LATEST=`eval  ls  $DIR | awk -F[-.]  "/$MOD-[0-9]+\-[0-9]+\.jar"'/ {print $3}' \
                   |sort -n | tail -n1`

       # JARFILE=`eval find $DIR -name $MOD-$BUILD*.jar | xargs basename`
         JARFILE=`eval find $DIR -name "${MOD}-*${LATEST}.jar" | xargs basename`

       echo $JARFILE
      }

#get_file  /opt/chinayie/payment gy_pay



# To retrieve the filename, to be used for rollback
rb_file() {
       DIR=$1
       MOD=$2

      # BUILD=`eval  ls -l  $DIR | awk "/$MOD-[0-9]+\-[0-9]+\.jar"'/ {print $9}' \
      #           | awk -F- '{print $2}' |sort -n | tail -n2 | head -n1`

       LAST=`eval  ls  $DIR | awk -F[-.]  "/$MOD-[0-9]+\-[0-9]+\.jar"'/ {print $3}' \
                   |sort -n | tail -n2  | head -n1`

       #JARFILE=`eval find $DIR -name $MOD-$BUILD*.jar | xargs basename`
       JARFILE=`eval find $DIR -name "${MOD}-*${LAST}.jar" | xargs basename`
       echo $JARFILE

#rb_file /opt/chinayie/payment gy_pay

env_check() {
   if [ $1 -lt 2 ]
   then
      echo -e  "\e[1;31m至少需要2个参数，第一为目标服务器地址，其他要同步文件（夹）！\e[0m"
      exit 10
   fi
}

confirm() {

   HOST=$1
   shift
   FILES=$@
   WARN=`echo -e "\e[1;31m真的要将${FILES}同步到${HOST}吗? [y/n] \e[0m"`

   read -r -p "$WARN" CONFIRM

   case $CONFIRM in
       [yY])
           ;;
        *)
            echo "终止执行脚本!"
            exit  10
   esac

}

