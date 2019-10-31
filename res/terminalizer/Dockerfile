FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install python3 python3-pip vim npm curl -y
RUN apt-get install zsh -y
RUN apt-get install git -y

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
RUN apt-get install -y libgtk-3-0
RUN apt-get install -y \
    wget \
    unzip \
    fontconfig \
    locales \
    gconf-service \
    libasound2 \
    libatk1.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgcc1 \
    libgconf-2-4 \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libstdc++6 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    ca-certificates \
    fonts-liberation \
    libappindicator1 \
    libnss3 \
    lsb-release \
    xdg-utils \
    wget
ENTRYPOINT [ "docker-entrypoint.sh" ]
