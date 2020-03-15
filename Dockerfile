FROM python:3.7-alpine
COPY . /app
WORKDIR /app
ENV FILENAME="cars.csv"
ENTRYPOINT python -u "/app/main.py" ${FILENAME}