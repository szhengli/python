FROM  registry.cn-shanghai.aliyuncs.com/hlb-cloud/alpine-oraclejdk8
#FROM docker.io/anapsix/alpine-java

ARG  jar
ARG  profile

WORKDIR /opt/chinayie/common-service
COPY curl /usr/bin/
COPY run.sh ./
COPY $jar  ./
COPY $profile  config/

ENV PATH /opt/chinayie/common-service:$PATH
ENV jar  $jar
ENTRYPOINT ["run.sh"]

EXPOSE 8080

HEALTHCHECK CMD netstat -tnlp | grep 8080   || exit 1
