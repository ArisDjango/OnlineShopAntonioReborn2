# OnlineShopAntonioReborn2
- rebuild from OnlineShopAntonioReborn
- Note:
    - Payment system braintree masih gagal
    - notif/status cart tidak muncul pada beberapa page, mungkin masalah cache
    - email notif belum berhasil
    - masih native html/css/js
    - production set
    - prod:
        - redis belum optimal/jalan
<details>
<summary>Instalasi clone</summary>

- Local
    - git clone xxxx
    - `pipenv shell` (jika tidak bisa, activate manual di . source /home/aris/.local/share/virtualenvs/OnlineShopAntonioReborn2-9gnlXKj9/bin/activate)
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
        - `docker-compose run --rm onlineshopantonio /bin/bash -c "cd myshop; python3 manage.py migrate"`
    - super user
        - `docker-compose run --rm onlineshopantonio /bin/bash -c "cd myshop; python3 manage.py createsuperuser"`
    - collect static
        - `docker-compose run --rm onlineshopantonio /bin/bash -c "cd myshop; python3 manage.py collectstatic --no-input"`

    
</details>

<details>
<summary>Online Shop summary</summary>

<details>
<summary>Creating an online shop project</summary>

- Create Project
    - myshop project
    - shop app
- Creating shop product catalog models
    - Category() --> name, slug
    - Product() --> category(FK=Category), name, slug, image, desc, price, available, created, updated
    - install pillow
- Registering catalog models on the
administration site
    - CategoryAdmin() --> list_display: name, slug, prepopulated_fields: slug, name)
    - ProductAdmin() --> list_display, list_filter, list_editable, prepopulated_fields
    - createsuperuser
- Building catalog views
    - product_list() --> category, categories, products, --> list.html
    - product_detail() --> product --> detail.html
    - shop/urls.py, myshop/urls.py
    - models.py --> reverse(), get_absolute_url()
- Creating catalog templates
    - templates
    ```
    templates/
        shop/
            base.html
            product/
                list.html
                detail.html
    ```
    - settings.py --> MEDIA_URL, MEDIA_ROOT
    - urls.py --> if settings.DEBUG: ...
</details>

<details>
<summary>Building a shopping cart</summary>
<details>
<summary>
Using Django sessions</summary>

    - django.contrib.sessions.middleware.SessionMiddleware
</details>

<details>
<summary>Session settings</summary>

- SESSION_COOKIE_AGE, SESSION_COOKIE_DOMAIN, SESSION_COOKIE_SECURE, SESSION_EXPIRE_AT_BROWSER_CLOSE, SESSION_SAVE_EVERY_REQUEST
- https://docs.
djangoproject.com/en/3.0/ref/settings/#sessions
</details>
- Session expiration
    - If you set SESSION_EXPIRE_AT_BROWSER_CLOSE to True, the session will expire when the user closes the browser, and the SESSION_COOKIE_AGE setting will not have any effect.
    - You can use the set_expiry() method of request.session to overwrite the
duration of the current session.
- Storing shopping carts in sessions 
    - settings.py --> CART_SESSION_ID = 'cart'
    - python manage.py startapp cart
    - cart.py -->Cart():
        - `__init__()`
        - `__len__`
        - add()
        - save()
        - remove()
        - get_total_price()
        - clear()
- Creating shopping cart views
    - Adding items to the cart
        - cart > forms.py --> CartAddProductForm()
        - views.py:
            - cart_add()
            - cart_remove()
            - cart_detail()
            - cart > urls.py

    - Building a template to display the cart
        ```
        templates/
            cart/
                detail.html
        ```
    - Adding products to the cart
        - views.py > product_detail() --> `... cart_product_form = CartAddProductForm()...`
        - shop/product/detail.html --> `...form action="{% url "cart:cart_add" product.id %}...`
        - runserver > detail page > input quantity > Add to cart

    - Updating product quantities in the cart
        - Tujuan : Kemampuan Merubah quantity pada detail page
        - cart > views.py > cart_detail() > `...for item in cart: dst ...`
        - cart > detail.html
        - replace `{{ item.quantity }}` dengan ` ...<form action="{% url "cart:cart_add" product.id %}" ...`
        -  http://127.0.0.1:8000/cart/

- Creating a context processor for the current
cart
    - Context processors
        - Tujuan: Agar cart update bisa tampil secara global
        - cart > context_processors.py > cart()
        - settings.py > `TEMPLATES ... 'cart.context_processors.cart',`
        - shop > templates > base.html > `...{% with total_items=cart|length %} dst...`
    - Setting the cart into the request context

</details>
</details>