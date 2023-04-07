FROM python:3.10.9

ARG VERSION
LABEL org.label-schema.version=$VERSION

COPY ./requirements.txt /webapp/requirements.txt

WORKDIR /webapp

RUN pip install -r requirements.txt

COPY webapp/* /webapp
RUN mkdir templates && mv mainpage.html templates/mainpage.html

EXPOSE 5000
CMD [ "python", "app.py"]
