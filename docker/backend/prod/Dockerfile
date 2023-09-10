FROM python:3.11.4-slim-bullseye as python

# Python build stage
FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=production

RUN apt-get update && apt-get install --no-install-recommends -y \
    # dependencies for building Python packages
    build-essential \
    # psycopg2 dependencies
    libpq-dev
# Requirements are installed here to ensure they will be cached.
COPY ./requirements .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip install --no-cache-dir --no-index --upgrade pip setuptools wheel \
    && pip wheel --wheel-dir /usr/src/app/wheels -r ${BUILD_ENVIRONMENT}.txt

# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=production
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels/

RUN apt-get update && \
    apt-get install --no-install-recommends -y gettext libpq5 && \
    # cleaning up unused files
    pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/*  && \
    rm -rf /wheels/ && \
    # apt-get remove --purge -y libpq-dev && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    # apt-get autoremove --purge -y && \
    apt-get clean && \
    rm -rf /tmp/* /var/lib/apt/lists/* /var/tmp/ && \
    addgroup --system backend && \
    adduser --system --ingroup backend backend

COPY --chown=backend:backend ./docker/backend/prod/entrypoint /entrypoint
COPY --chown=backend:backend ./docker/backend/prod/start /start

RUN sed -i 's/\r$//g' /entrypoint \
    && sed -i 's/\r$//g' /start \
    && chmod +x /entrypoint \
    && chmod +x /start

# copy application code to WORKDIR
COPY --chown=backend:backend ./src ${APP_HOME}

# make backend owner of the WORKDIR directory as well.
RUN chown backend:backend ${APP_HOME}

USER backend

ENTRYPOINT ["/entrypoint"]
