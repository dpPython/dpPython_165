FROM python:3.6-alpine as base

FROM base as builder

RUN mkdir /install
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM base

COPY --from=builder /install /usr/local
COPY . /app
RUN apk --no-cache add libpq
RUN /bin/sh -c "apk add --no-cache bash"
WORKDIR /app

ENV DOCKER=1

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
