FROM ubuntu:18.04

# Install python3 interpreter and package manager
RUN apt-get update
RUN apt-get install python3 python3-pip vim -y

# Copy wheel-distribution and install it
RUN mkdir /installer
COPY dist/*.whl /installer
RUN python3 -m pip install /installer/*.whl

# Install default pypes
RUN mkdir /pypes
COPY example_pypes/basics /pypes/basics

# Set bash as default shell and vim as default editor
ENV SHELL=/bin/bash
ENV VISUAL=vim
ENV EDITOR=vim

# Configure pype
RUN pype pype.config plugin-register -n basics -p /pypes
RUN pype pype.config install-shell -t ~/.bashrc

ENTRYPOINT [ "bash" ]
