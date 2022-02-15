FROM artifactory.cloud.cms.gov/docker/python:3.7-slim as base
WORKDIR /app
RUN pip3 install gunicorn

RUN apt-get update 
RUN apt-get upgrade -y
RUN apt-get install git -y

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app

CMD [ "python3", "metadata_service/metadata_wsgi.py" ]

FROM base as oidc-release

RUN pip3 install .[oidc]
RUN python3 setup.py install
ENV FLASK_APP_MODULE_NAME flaskoidc
ENV FLASK_APP_CLASS_NAME FlaskOIDC
ENV FLASK_OIDC_WHITELISTED_ENDPOINTS status,healthcheck,health
ENV SQLALCHEMY_DATABASE_URI sqlite:///sessions.db

# You will need to set these environment variables in order to use the oidc image
# FLASK_OIDC_CLIENT_SECRETS - a path to a client_secrets.json file
# FLASK_OIDC_SECRET_KEY - A secret key from your oidc provider
# You will also need to mount a volume for the clients_secrets.json file .

FROM base as release
RUN python3 setup.py install
