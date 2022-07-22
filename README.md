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
<summary>A. Create Base Online Shop</summary>

<details>
<summary>1. Creating an online shop project</summary>

- Create Project
    - myshop project
    - shop app
- Creating shop product catalog models
    - Category()
        - name
        - slug
    - Product()
        - category --> FK=Category
        - name
        - slug
        - image
        - desc
        - price
        - available
        - created
        - updated
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
<summary>2. Building a shopping cart</summary>
<details>
<summary>2.1. Using Django sessions</summary>

- django.contrib.sessions.middleware.SessionMiddleware
</details>

<details>
<summary>2.2. Session settings</summary>

- SESSION_COOKIE_AGE, SESSION_COOKIE_DOMAIN, SESSION_COOKIE_SECURE, SESSION_EXPIRE_AT_BROWSER_CLOSE, SESSION_SAVE_EVERY_REQUEST
- https://docs.
djangoproject.com/en/3.0/ref/settings/#sessions
</details>

<details>
<summary>2.3. Session expiration</summary>

- If you set SESSION_EXPIRE_AT_BROWSER_CLOSE to True, the session will expire when the user closes the browser, and the SESSION_COOKIE_AGE setting will not have any effect.
- You can use the set_expiry() method of request.session to overwrite the
duration of the current session.
</details>

<details>
<summary>2.4. Storing shopping carts in sessions</summary>

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
</details>

<details>
<summary>2.5. Creating shopping cart views</summary>

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
</details>

<details>
<summary>2.6. Creating a context processor for the current cart</summary>

- Context processors
    - Tujuan: Agar cart update bisa tampil secara global
    - https://docs.djangoproject.com/en/3.0/ref/templates/api/#built-in-template-context-processors.
- Setting the cart into the request context
    - cart > context_processors.py > cart()
    - settings.py > `TEMPLATES ... 'cart.context_processors.cart',`
    - shop > templates > base.html > `...{% with total_items=cart|length %} dst...`
</details>

</details>

<details>
<summary>3. Registering customer orders</summary>

<details>
<summary>3.1 Creating order models</summary>

- startapp orders
- models.py >
- Order()
    - first_name
    - last_name
    - email
    - address
    - postal_code
    - city
    - created
    - updated
    - paid
    - ordering: created
    - `__str__()`
    - get_total_cost()
- OrderItem()
    - order --> FK:Order
    - product --> FK: Product
    - price
    - quantity
    - `__str__()`
    - get_cost()
- migrate
</details>

<details>
<summary>3.2 Including order models in the administration
site</summary>

- orders > admin.py
- OrderItemInline()
    - model => OrderItem
    - raw_id_fields
- OrderAdmin()
    - list_display
    - list_filter
    - inlines
- http://127.0.0.1:8000/admin/orders/order/add/
</details>

<details>
<summary>3.3 Creating customer orders</summary>

- orders > forms.py
    - OrderCreateForm()
        - model => Order
        - fields => first_name, last_name, dst
- orders > views.py
    - order_create()
    - render = orders/order/create.html
- orders > urls.py
    - path= create/ , views=order_create
- myshop > urls.py
    - path= orders/ , include=orders.urls
- template > cart > detail.html
    - `href="{% url "orders:order_create" %}"`
- orders/order/create.html
- orders/order/created.html
</details>


<details>
<summary>3.2 Launching asynchronous tasks with
Celery</summary>
</details>

</details>

<details>
<summary>4. Launching asynchronous tasks with
Celery</summary>

- Install Celery
- Install RabbitMQ
- Adding Celery to your project
    - myshop > celery.py
    - myshop/`__init__.py`
- Adding asynchronous tasks to your application
    - order > tasks.py
    - settings.py > set email backend
    - orders > views.py > ...order_created.delay(order.id) ...
    - `celery -A myshop worker -l info`
- Monitoring Celery
    - Install flower
    - celery -A myshop flower
    - http://localhost:5555/
</details>




</details>

<details>
<summary>B. Managing Payments
and Orders</summary>

<details>
<summary>1. Integrating a payment gateway</summary>
</details>

<details>
<summary>2. Exporting orders to CSV files</summary>

- Adding custom actions to the administration site
    - orders > admin.py
    - export_to_csv()
    - OrderAdmin() --> `...actions = [export_to_csv]...`
    - http://127.0.0.1:8000/admin/orders/order/
- Extending the administration site with custom views
    - orders > views.py
    - @staff_member_required --> admin_order_detail()
    - orders > urls.py
    - templates/orders
        ```
        admin/
            orders/
                order/
                    detail.html
        ```
    - edit detail.html
    - add a link to each Order object in the list display page of the administration site
        - orders > admin.py
        - order_detail()
        - OrderAdmin() --> list_display --> ...order_detail]
    - http://127.0.0.1:8000/admin/orders/order/
</details>

<details>
<summary>3. Generating PDF invoices dynamically</summary>

- https://docs.djangoproject.com/en/3.0/howto/outputting-pdf/
- pip install WeasyPrint==51
- Creating a PDF template
    - templates/orders/order/pdf.html
- Rendering PDF files
    - orders > views.py
    - settings.py > STATIC_ROOT
    - python manage.py collectstatic
    - orders > urls.py
        - path=`admin/order/<int:order_id>/pdf/`  , views.admin_order_pdf
    - orders > admin.py
        - order_pdf()
        - OrderAdmin() --> list_display --> ...order_pdf]
    - http://127.0.0.1:8000/admin/orders/order/
- Sending PDF files by email
    - payment >  tasks.py
    - payment_completed()
    - settings.py --> SMTP settings
    - payment > views.py
    - payment_process() --> ... payment_completed.delay(order.id)...
</details>





</details>

<details>
<summary>C. Extending Your Shop</summary>

<details>
<summary>1. Creating a coupon system</summary>

- Creating a coupon system
    - Building the coupon model
        - startapp coupons
        - coupon > models.py
        - Coupon()
            - code
            - valid_from
            - valid_to
            - discount
            - active
            - `__str__()`
    - Applying a coupon to the shopping cart
        - coupons > forms.py
            - CouponApplyForm()
        - coupons > views.py
            - @require_POST --> coupon_apply()
        - coupons > urls.py
            - `path('apply/', views.coupon_apply, name='apply'),`
        - myshop > urls.py
            - `path('coupons/', include('coupons.urls', namespace='coupons')),`
        - cart > cart.py
            - Cart()
            - `__init__` --> ...self.coupon_id = self.session.get('coupon_id')
        - get the coupon_id session key from the current session and store its value in the Cart object:
            - Cart()
                - @property
                - coupon()
                - get_discount()
                - get_total_price_after_discount()
        - include the coupon system in the cart's detail view:
            - cart > views.py
            - cart_datail() --> coupon_apply_form = CouponApplyForm()
        - Templates cart/detail.html
            - ... {% if cart.coupon %} ...
        - add the coupon to the next step of the purchase process
            - orders/order/create.html
            - ...{% if cart.coupon %}...
            - ...get_total_price_after_discount | floatformat:2...
        - http://127.0.0.1:8000/orders/create/
    - Applying coupons to orders
        - store the coupon that was applied to each order:
            - orders > models.py
            - Order() ...
                - coupon
                - discount
            - migrate
            - Order() ...
                - get_total_cost()
                    - total_cost --> total_cost - total_cost * (self.discount / Decimal(100))
        - save the related coupon and its discount when creating a new order:
            - orders > views.py
            - order_create()
                - if cart.coupon: ... order.save()
            - http://127.0.0.1:8000/admin/orders/order/
</details>
</details>