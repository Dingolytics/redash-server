FROM python:3.10.11-slim-bullseye AS dependencies

# Multi-stage build:
# https://docs.docker.com/develop/develop-images/multistage-build/
# https://pythonspeed.com/articles/multi-stage-docker-python/

# Stage 1: Install Python dependencies
#-------------------------------------

RUN apt update -y && \
  apt install -y --no-install-recommends \
    curl \
    unzip \
    build-essential \  
    libffi-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip~=23.0.1 --timeout 120 \
  && pip install --user -r requirements.txt --timeout 120

# Stage 2: Create image with application code
#--------------------------------------------

FROM python:3.10.11-slim-bullseye AS application

ARG USERNAME=redash
RUN useradd --create-home ${USERNAME}

COPY --chown=${USERNAME} --from=dependencies \
  /root/.local /home/${USERNAME}/.local

ENV PATH=/home/${USERNAME}/.local/bin:$PATH

WORKDIR /home/${USERNAME}/app/

USER ${USERNAME}

COPY --chown=${USERNAME} LICENSE* manage.py docker-entrypoint.sh ./
COPY --chown=${USERNAME} etc ./etc/
COPY --chown=${USERNAME} migrations ./migrations/
COPY --chown=${USERNAME} redash ./redash/

EXPOSE 5000

ENTRYPOINT ["./docker-entrypoint.sh"]

# Stage 3: Create image for testing
#----------------------------------

FROM application AS tests

COPY --chown=${USERNAME} etc/requirements.tests.txt ./
RUN pip install --user -r requirements.tests.txt --timeout 120
