FROM python:3.5

RUN groupadd -r uwsgi && \
    useradd -r -g uwsgi uwsgi && \
    pip install Flask uwsgi requests

USER uwsgi
WORKDIR /app
COPY app /app

EXPOSE 9090 9191 5000
ENTRYPOINT [ "./run_server.sh" ]
