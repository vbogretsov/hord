FROM openjdk:jre-slim
ARG KARATE_VERSION=1.1.0
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*
RUN wget "https://github.com/intuit/karate/releases/download/v${KARATE_VERSION}/karate-${KARATE_VERSION}.jar" -O /opt/karate.jar
VOLUME /src/test/java
WORKDIR /src/test/java
CMD [ "java", "-jar", "/opt/karate.jar", "/src/test/java" ]
