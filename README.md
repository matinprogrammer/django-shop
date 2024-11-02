# django-SHOP

**Django-SHOP** 
[django-CMS](https://www.django-cms.org/).

Here you can find the [full documentation for django-SHOP](https://shop.matinahmadi.ir/documentation).

## What is it?
this is a sample of shop that created by django that can help you to learn about django

## Demo shop
A demo shop can be tried here: [django-shop](https://shop.matinahmadi.ir/demo).

## What Django tools and features does the shop use?
* Django CBV
* Django management
* override django user


## urls

**user activity** in /accounts/
* /login/ login user with **phone number** and password
* /logout/ logout
* /register/ register user with **phone number**, **firstname** and **password**. next send register code to his/her number
* /verify/ verify sended code

**product** in /category/
* /product/&lt;slug:slug&gt;/ show product detail

**cart and order** in /orders/
* // list of order
* /cart/ show cart detail
* /cart/add/&lt;int:product_id&gt;/ and product in cart (if you click on 'add to cart' in product detail send to this page)
* /cart/remove/&lt;int:product_id&gt;/ remove cart
* /detail/&lt;int:order_id&gt;/ detail of order
* /delete/&lt;int:order_id&gt;/ delete order
* /create/ create order
* /apply/&lt;int:order_id&gt;/ apply coupon on order

## history

**1.0.0**

* full account register, login, logout
* simple category and post 
* use sqllite

**2.0.0 probebly in 2024/Nov/30, 1403/aban/30**

* nested category
* inheritance post category
* use postgresql
* use ArvanCloud for media files

**3.0.0 probebly in 2025/Jan/30, 1403/dey/30**

* use celery and rabbitmq for async process
* use redis catch
* create docker file


