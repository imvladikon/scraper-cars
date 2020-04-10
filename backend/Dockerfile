FROM python:3.8-alpine
COPY . /backend
WORKDIR /backend
RUN pip install -r requirements.txt
ENV FLASK_APP controller.py
CMD flask run --host=0.0.0.0
#ENV FILENAME="cars.csv"
#ENTRYPOINT python -u "/backend/main.py" ${FILENAME}
