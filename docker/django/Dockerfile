FROM python:3.10.1
LABEL maintainer="kamolov.amir2000@yandex.ru"

RUN pip install pipenv

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /storage/
COPY ./Pipfile ./
COPY ./Pipfile.lock ./ 
RUN pipenv install

COPY ./ ./

RUN pipenv run python ./manage.py collectstatic --noinput

EXPOSE 8080

ENTRYPOINT [ "pipenv", "run", "gunicorn", "--reload", "--bind", "0.0.0.0:8080", "application.wsgi:application" ]