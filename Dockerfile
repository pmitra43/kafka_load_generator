FROM openjdk:alpine
RUN apk update && apk add bash
RUN mkdir -p /json-data-generator/ && \
    mkdir -p /kafka/
COPY json-data-generator-1.2.2-SNAPSHOT /json-data-generator/
COPY kafka_2.11-0.10.2.0 /kafka/
WORKDIR /json-data-generator
RUN pwd
RUN ls
CMD java -jar json-data-generator-1.2.2-SNAPSHOT.jar cpuUsageSimConfig.json
