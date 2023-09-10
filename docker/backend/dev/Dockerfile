FROM python:3.11.4-slim-bullseye as python
# Python 'dev' stage
FROM python as backend-dev

ARG BUILD_ENVIRONMENT=local

RUN apt-get update \
  && apt-get install --no-install-recommends -y \
  build-essential \
  libpq-dev \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY ./requirements .

RUN pip install --no-cache-dir --no-index --upgrade pip setuptools wheel \
  && pip wheel --wheel-dir /usr/src/app/wheels -r ${BUILD_ENVIRONMENT}.txt

# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels/

RUN apt-get update \
  && apt-get install --no-install-recommends -y libpq5 gettext \
  # devcontainer dependencies and utils
  sudo git bash-completion nano ssh make \
  # Create devcontainer user and add it to sudoers
  && groupadd --gid 1000 dev-user \
  && useradd --uid 1000 --gid dev-user --shell /bin/bash --create-home dev-user \
  && echo dev-user ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/dev-user \
  && chmod 0440 /etc/sudoers.d/dev-user \
  && pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/*  \
  # cleaning up unused files
  && rm -rf /wheels/ \
  # && apt-get remove --purge -y libpq-dev \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  # && apt-get autoremove --purge -y \
  && apt-get clean \
  && rm -rf /tmp/* /var/lib/apt/lists/* /var/tmp/

COPY ./docker/backend/dev/entrypoint /entrypoint
COPY ./docker/backend/dev/start /start

RUN sed -i 's/\r$//g' /entrypoint \
  && sed -i 's/\r$//g' /start \
  && chmod +x /entrypoint \
  && chmod +x /start

# copy application code to WORKDIR
# COPY ./src ${APP_HOME}

ENTRYPOINT ["/entrypoint"]
