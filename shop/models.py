from django.db import models


class Members(models.Model):
    userName = models.CharField(max_length=16, primary_key=True)
    password = models.CharField(max_length=16)
    authority = models.CharField(max_length=8)
    email1 = models.EmailField(max_length=32)
    balance = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    loginTime = models.CharField(max_length=32, null=True, blank=True)
    logoutTime = models.CharField(max_length=32, null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)


class Goods(models.Model):
    goodsName = models.CharField(max_length=32, primary_key=True)
    userName = models.ForeignKey(to=Members, to_field="userName", on_delete=models.CASCADE)
    kind = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField()
    mainImg = models.ImageField(upload_to="img", null=True, blank=True)
    img1 = models.ImageField(upload_to="img", null=True, blank=True)
    img2 = models.ImageField(upload_to="img", null=True, blank=True)
    img3 = models.ImageField(upload_to="img", null=True, blank=True)
    intro = models.TextField(null=True, blank=True)


class BuyLog(models.Model):
    orderNumber = models.CharField(max_length=32)
    userName = models.ForeignKey(to=Members, to_field="userName", on_delete=models.CASCADE)
    goodsName = models.CharField(max_length=32)
    kind = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    num = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)


class UserBrowsingLog(models.Model):
    userName = models.ForeignKey(to=Members, to_field="userName", on_delete=models.CASCADE, null=True, blank=True)
    goodsName = models.ForeignKey(to=Goods, to_field="goodsName", on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)


class OperationLog(models.Model):
    userName = models.ForeignKey(to=Members, to_field="userName", on_delete=models.CASCADE)
    operation = models.CharField(max_length=16)
    ip = models.GenericIPAddressField()
    time = models.DateTimeField(auto_now_add=True)


class TempCode(models.Model):
    code = models.CharField(max_length=6)
    userName = models.CharField(max_length=16)
    authority = models.CharField(max_length=8)
    email1 = models.EmailField(max_length=32)


class ShopCart(models.Model):
    userName = models.ForeignKey(to=Members, to_field="userName", on_delete=models.CASCADE)
    shopCart = models.CharField(max_length=65530)
#goodsname:num