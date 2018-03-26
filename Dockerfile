FROM python:3.6-alpine3.6

# Add dependency manifest
ADD ./requirements.txt /usr/src/app/
WORKDIR /usr/src/app/

# Install dependencies
RUN pip install -r requirements.txt

# Add Application Files
ADD . /usr/src/app/

ENV PORT=8080

# for a flask server
EXPOSE 8080

CMD gunicorn main:app