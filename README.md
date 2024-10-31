# django-SHOP

**Django-SHOP** 
[django-CMS](https://www.django-cms.org/).

Here you can find the [full documentation for django-SHOP](https://shop.matinahmadi.ir/documentation).

## What is it?
this is a sample of shop that created by django that can help you to learn about django

## Demo shop
A demo shop can be tried here: [django-shop](https://shop.matinahmadi.ir/demo).

## What Django tools and features does the shop use?
*Django CBV
*Django management


## urls

**user activity** in /accounts/
* /login/ login user with **phone number** and password
* /logout/ logout
* /register/ register user with **phone number**, **firstname** and **password**. next send register code to his/her number
* /verify/ verify sended code

**product** in /category/
* /product/&gt;slug:slug&lt;/ show product detail

**cart and order** in /orders/
//
/cart/
/cart/add/&gt;int:product_id&lt;/
/cart/remove/&gt;int:product_id&lt;/
/detail/&gt;int:order_id&lt;/
/delete/&gt;int:order_id&lt;/
/create/
/apply/&gt;int:order_id&lt;/
