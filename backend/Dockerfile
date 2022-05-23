FROM python:3.7
COPY . /
RUN pip3 install fastapi uvicorn gunicorn pymongo motor python-decouple pydantic[email]
ENTRYPOINT /start_docker.sh
#CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]