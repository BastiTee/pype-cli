# Mint linux container image to test basic pype installation
FROM ubuntu

# Install python3 interpreter, package manager and zsh
RUN apt-get update
RUN apt-get install python3 python3-pip vim curl zsh git -y
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

# Set bash as default shell and vim as default editor
ENV LANG=C.UTF-8
ENV SHELL=/bin/zsh
ENV VISUAL=vim
ENV EDITOR=vim

# Copy wheel-distribution and install it
RUN mkdir /installer
COPY dist/*.whl /installer
RUN python3 -m pip install /installer/*.whl

# Install default pypes
RUN mkdir /pypes
COPY example_pypes/basics /pypes/basics

# Configure pype
RUN pype pype.config plugin-register -n basics -p /pypes
RUN pype pype.config shell-install

ENTRYPOINT [ "zsh" ]
