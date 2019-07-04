FROM python:3.6-alpine as base

FROM base as builder

RUN mkdir /install
RUN apk update && apk add gcc python3-dev musl-dev
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip3 install --install-option="--prefix=/install" -r /requirements.txt

FROM base

RUN pip3 install setuptools
COPY --from=builder /install /usr/local
COPY . /services
RUN apk --no-cache add libpq
WORKDIR /services

CMD ["python3", "manage.py", "runserver", "5050"]


