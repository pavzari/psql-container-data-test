FROM python:3.9

WORKDIR /code
ENV PYTHONPATH=/code/src

ADD ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./ /code/

ENTRYPOINT ["tail", "-f", "/dev/null"]
