FROM liquibase/liquibase:latest

ADD https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.4/postgresql-42.7.4.jar \
    /liquibase/internal/lib/postgresql.jar

USER root
RUN chmod 644 /liquibase/internal/lib/postgresql.jar
USER liquibase
