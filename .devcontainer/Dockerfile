FROM mcr.microsoft.com/devcontainers/base:jammy

ARG UID=20000
ARG GID=20000
ARG USERNAME=dev

RUN groupadd -g ${GID} ${USERNAME} \
    && useradd -m -u ${UID} -g ${GID} ${USERNAME}
USER ${USERNAME}