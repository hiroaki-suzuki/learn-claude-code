FROM mcr.microsoft.com/devcontainers/python:dev-3.14-trixie

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    tmux \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
