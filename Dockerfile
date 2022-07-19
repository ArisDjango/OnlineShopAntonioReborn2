FROM python:3.8

RUN mkdir -p /opt/services/onlineshopantonio/src
WORKDIR /opt/services/onlineshopantonio/src

#RUN pip install gunicorn django
# we use --system flag because we don't need an extra virtualenv
COPY Pipfile Pipfile.lock /opt/services/onlineshopantonio/src/
RUN pip install pipenv && pipenv install --system

COPY . /opt/services/onlineshopantonio/src

EXPOSE 8000

CMD ["gunicorn", "--chdir", "blogApp", "--bind", ":8000", "core.wsgi:application" ]