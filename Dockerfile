FROM python:3.9-alpine3.13

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

# RUN apk add uvicorn
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

# Make port 5000 available to the world outside this container 
EXPOSE 5000
ENV FLASK_RUN_HOST=0.0.0.0
# Run the app
CMD ["flask", "run"]