# OnlineShopAntonioReborn2
- rebuild from OnlineShopAntonioReborn
- Note:
    - Payment system braintree masih gagal
    - notif/status cart tidak muncul pada beberapa page, mungkin masalah cache
    - email notif belum berhasil
    - masih native html/css/js
<details>
<summary>Instalasi clone</summary>

- Local
    - git clone xxxx
    - `pipenv shell` (jika tidak bisa, activate manual di . source /home/aris/.local/share/virtualenvs/BlogAntonio-J9LzUExB/bin/activate)
    - `pipenv install`
    - pada settings.py, set allowed_host: 'localhost'
    - Database
        - set: user, pass, database, --> settings.py
        - `sudo service postgresql start`
        - sudo su --> su - postgres --> psql
        - `CREATE USER user_name WITH ENCRYPTED PASSWORD 'mypassword';`
        - `CREATE DATABASE dbname OWNER rolename;`
        - `GRANT ALL PRIVILEGES ON dbname TO aris;`
    - RabbitMQ & Celery (for email notif when place order)
        - [Install rabbitMq ubuntu](https://www.rabbitmq.com/install-debian.html)
        - sudo rabbitmq-server
        - cd myshop
        - celery -A myshop worker -l info
        - celery -A myshop flower >> open http://localhost:5555 (flower = monitoring celery)
    - Redis (recomendation system)
        - [Instalasi](https://redis.io/docs/getting-started/installation/install-redis-on-linux/)
        - [other command](https://github.com/ArisDjango/orm-postgres/blob/main/redis.)
        - `redis-server`
    - `python manage.py migrate`
    - `python manage.py createsuperuser`
    - `python manage.py runserver`
    - konten:
        - localhost:8000
        - localhost:8000/admin/
    - Backup:
        - `python manage.py dumpdata blog --indent=2 --output=blog/fixtures/backup2022.json`
    - Load:
        - `python manage.py loaddata backup2022.json`
- Production (docker)
    - git clone xxxx
    - pada settings.py, set allowed_host: 'XXX' --> IP Public
    - `docker-compose up`
    - `docker container ls` --> pastikan container jalan
    - migrate:
        - `docker-compose run --rm blogantonio /bin/bash -c "cd blogApp; python3 manage.py migrate"`
    - super user
        - `docker-compose run --rm blogantonio /bin/bash -c "cd blogApp; python3 manage.py createsuperuser"`
    - collect static
        - `docker-compose run --rm blogantonio /bin/bash -c "cd blogApp; python3 manage.py collectstatic --no-input"`

    
</details>