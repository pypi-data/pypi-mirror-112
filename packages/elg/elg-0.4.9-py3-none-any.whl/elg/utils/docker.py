ENTRYPOINT_FLASK = """\
#!/bin/sh\nexec /sbin/tini -- venv/bin/gunicorn --bind=0.0.0.0:8000 "--workers=$WORKERS" --worker-tmp-dir=/dev/shm "$@" {service_script}:app\n"""

ENTRYPOINT_QUART = """\
#!/bin/sh\nexec /sbin/tini -- venv/bin/hypercorn --bind=0.0.0.0:8000 "$@" {service_script}:app\n"""

DOCKERFILE = """\
FROM python:slim

# Install tini and create an unprivileged user
ADD https://github.com/krallin/tini/releases/download/v0.19.0/tini /sbin/tini
RUN addgroup --gid 1001 "elg" && adduser --disabled-password --gecos "ELG User,,," --home /elg --ingroup elg --uid 1001 elg && chmod +x /sbin/tini

# Copy in just the requirements file
COPY --chown=elg:elg requirements.txt /elg/

# Everything from here down runs as the unprivileged user account
USER elg:elg

WORKDIR /elg

# Create a Python virtual environment for the dependencies
RUN python -m venv venv 
RUN /elg/venv/bin/python -m pip install --upgrade pip
RUN venv/bin/pip --no-cache-dir install -r requirements.txt 

# Copy ini the entrypoint script and everything else our app needs
{required_folders}
COPY --chown=elg:elg docker-entrypoint.sh {required_files} /elg/

ENV WORKERS=1

RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]\
"""

COPY_FOLDER = "COPY --chown=elg:elg {folder_name} /elg/{folder_name}/"
