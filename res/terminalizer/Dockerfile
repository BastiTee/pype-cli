FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install python3 python3-pip vim npm curl zsh git -y

# Set bash as default shell and vim as default editor
ENV LANG=C.UTF-8
ENV SHELL=/bin/bash
ENV VISUAL=vim
ENV EDITOR=vim

# Configure pype
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
RUN pip3 install pype-cli
RUN pype pype.config shell-install

RUN npm install -g terminalizer
RUN terminalizer init

ENTRYPOINT [ "docker-entrypoint.sh" ]
