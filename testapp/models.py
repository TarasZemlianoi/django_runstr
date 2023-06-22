from django.db import models


class Order(models.Model):

    order_dt = models.DateTimeField(auto_now=True)
    order_textt = models.CharField(max_length=200)
