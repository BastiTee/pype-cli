# Travis-like build pipeline for Python 3.7
FROM ubuntu:18.04

# Setup basic system environment
ENV LANG=C.UTF-8
RUN apt-get update
RUN apt-get install curl python3.7 python3-pip -y

# Clone from source
ADD ./* /pype/
WORKDIR /pype
ENV LC_ALL=C.UTF-8
ENTRYPOINT [ "bash", "-c", "./make clean && ./make build" ]
