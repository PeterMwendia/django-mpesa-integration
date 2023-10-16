FROM ubuntu:latest
LABEL authors="archie"

ENTRYPOINT ["top", "-b"]