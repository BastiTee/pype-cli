FROM ubuntu:18.04

# Install python3 interpreter and package manager
RUN apt-get update
RUN apt-get install python3 python3-pip -y

# Copy wheel-distribution and install it
RUN mkdir /installer
COPY dist/*.whl /installer
RUN python3 -m pip install /installer/*.whl

# Install default pypes
RUN mkdir /pypes
COPY example_pypes/basics /pypes/basics

# Install bash completion
RUN echo "eval \"\$(_PYPE_COMPLETE=source pype)\"" >> ~/.bashrc

ENTRYPOINT [ "bash" ]
