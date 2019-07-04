FROM python:3.6-alpine as base

FROM base as builder

RUN mkdir /install
RUN apk update && apk add gcc python3-dev musl-dev
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM base

RUN pip install setuptools
COPY --from=builder /install /usr/local
COPY . /app
RUN apk --no-cache add libpq
WORKDIR /app

CMD ["celery", "-A app.celery_proj.celery", "-E", "--loglevel=INFO"]
CMD ["python", "manage.py", "runserver", "-p", "5050"]