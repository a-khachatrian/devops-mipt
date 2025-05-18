FROM  alpine:3.20 as build

RUN apk add --no-cache maven

WORKDIR /app

COPY pom.xml .
RUN mvn dependency:resolve-plugins dependency:resolve

COPY src/ src/
RUN mvn package

FROM alpine:3.20

RUN apk add --no-cache openjdk17-jre

WORKDIR /app

COPY --from=build /app/target/*.jar app.jar

RUN addgroup -S backgroup && \
    adduser -S backuser -G backgroup && \
    chown -R backuser:backgroup /app
USER backuser

CMD ["sh", "-c", "java -jar app.jar"]