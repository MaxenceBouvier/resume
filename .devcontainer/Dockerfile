FROM ghcr.io/xu-cheng/texlive-full:latest

RUN apk update \
 && apk add poppler poppler-utils

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=1000

# Create user and group in Alpine
RUN addgroup -g ${USER_GID} ${USERNAME} && \
    adduser -D -u ${USER_UID} -G ${USERNAME} ${USERNAME}

RUN apk add --no-cache openssh

USER ${USERNAME}
WORKDIR /home/${USERNAME}
