# docker/advisory.Dockerfile
#
# Build context = the project root (docker-compose.yml sends "context: .").
# 1) Parent image: eclipse-temurin:21-jre  -> a minimal JRE that runs a Spring
#    Boot fat jar. We deliberately use "-jre" (not "-jdk") so the image stays small.
# 2) WORKDIR /app       -> the directory our jar will live in inside the image.
# 3) COPY target/...    -> copies the built jar from the HOST build context.
#    (you must run `mvn package -DskipTests` on the host first to create target/)
# 4) ENTRYPOINT java -jar -> the container's default command when it starts.
#
# Build locally:
#   docker build -f docker/advisory.Dockerfile -t agri-advisory:latest .
