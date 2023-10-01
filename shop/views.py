# Create your views here.
from django.contrib import admin
from django.db.models import Count
from django.shortcuts import render, HttpResponse, redirect, reverse
from shop.models import *
from shop.myfunc.myfunc1 import *
import random, json, time
from decimal import Decimal, ROUND_HALF_UP
import copy


def testcookies(request):
    a = Goods.objects.all().order_by("userName_id")
    b = Goods.objects.all()
    for i in a:
        print(i.userName_id)

    print("\n")
    for i in b:
        print(i.userName_id)

    return render(request, "testcookies.html")


def index(request):
    authority = getAuthority(request)
    username = request.COOKIES.get("username")
    if authority == "seller":
        goods = Goods.objects.filter(userName=request.COOKIES.get("username"))
        return render(request, "sellerindex.html", locals())
    if authority == "admin":
        return render(request, "adminindex.html", locals())
    if authority is None or authority == "user":
        # 得到基础信息
        goodsName = request.GET.get("goodsName")
        page = 0 if request.GET.get("page") is None else int(request.GET.get("page"))
        lentopgoods = 0

        if goodsName is not None:
            goods = Goods.objects.filter(goodsName__contains=goodsName)
        elif authority is None:
            goods = Goods.objects.all()
        else:
            username = request.COOKIES.get("username")
            recentGood = BuyLog.objects.filter(userName_id=username).order_by("-time").first()
            if recentGood is not None:
                kind = recentGood.kind
                topgoods = Goods.objects.filter(kind=kind)
                lentopgoods = topgoods.count()
                print(lentopgoods)
                if lentopgoods > 4:
                    lentopgoods = 4
                topgoods = topgoods[:lentopgoods]
                goods = Goods.objects.all()
            else:
                goods = Goods.objects.all()

        if page is None or page == 0:
            goods = goods[0:10 - lentopgoods]
        else:
            goods = goods[page * 10 - lentopgoods:(page + 1) * 10 - lentopgoods]

        if goods.__len__() == 0:
            return HttpResponse("没有这一页")
        username = request.COOKIES.get("username")
        rangee = range(10)
        return render(request, "index.html", locals())
    return render(request, "index.html")


def login(request):
    if request.method == "GET":
        cookies = request.COOKIES
        if cookies.get("username") is None:
            return render(request, "login.html")
        else:
            return redirect("/")

    username = request.POST.get("username")
    password = request.POST.get("password")
    if Members.objects.filter(userName=username).first() is not None \
            and password == Members.objects.filter(userName=username).first().password:
        resp = redirect("/")
        resp.set_cookie("username", username, max_age=7200)
        resp.set_cookie("password", password, max_age=7200)
        Members.objects.filter(userName=username).update(loginTime=nowtime2str(), ip=getip(request))
        return resp
    return render(request, "login.html", {"error": "密码或账号错误"})


def sendcode(request):
    email = request.GET.get("email")
    username = request.GET.get("username")
    authority = request.GET.get("authority")

    if Members.objects.filter(userName=username).first() is not None:
        return HttpResponse('{"msg":"账号已存在"}', content_type="application/json")
    # 随机六位验证码
    code = ""
    for i in range(6):
        code = code + str(random.randint(0, 9))
    # 验证码加入TempCode表里
    TempCode.objects.create(userName=username,
                            code=code,
                            authority=authority,
                            email1=email)
    # 发验证码短信给对应邮箱
    sendemail(email, "mysite验证码", "您的验证码是：" + code)
    return HttpResponse('{"msg":"验证码发送成功"}', content_type="application/json")


def register(request):
    if request.method == "GET":
        return render(request, "register.html")

    # 得到注册信息
    username = request.POST.get("username")
    password = request.POST.get("password")
    authority = request.POST.get("authority")
    email = request.POST.get("email")
    code = request.POST.get("code")

    if Members.objects.filter(userName=username).first() is not None:
        return render(request, "register.html", {"error": "账户已经注册"})

    checkparam = TempCode.objects.filter(userName=username,
                                         authority=authority,
                                         email1=email).last()

    # 写入数据库
    if checkparam is not None and checkparam.code == code:
        Members.objects.create(userName=username,
                               password=password,
                               authority=authority,
                               email1=email,
                               balance=0, )
        return redirect("/")

    return render(request, "register.html", {"error": "验证码错误,不是最后一个验证码，或发送验证码后修改了信息"})


def logout(request):
    cookies = request.COOKIES
    username = cookies.get("username")
    if username is not None:
        resp = render(request, "logout.html", {"username": username})
        resp.delete_cookie("username")
        resp.delete_cookie("password")
        ip = getip(request)
        Members.objects.filter(userName=username).update(ip=ip)
        Members.objects.filter(userName=username).update(logoutTime=nowtime2str())
        return resp
    else:
        return render(request, "plslogin.html")


def upload(request):
    if getAuthority(request) is None:
        return render(request, "plslogin.html")
    if getAuthority(request) != "seller":
        return HttpResponse("非卖家账号，不能添加商品")

    if request.method == "GET":
        return render(request, "upload.html")

    if getAuthority(request) == "seller":
        imgs = request.FILES.getlist("img")

        Goods.objects.create(goodsName="book02", userName=Members.objects.filter(userName="qwes").first(), kind="book",
                             price=10, inventory=10, mainImg=imgs[0], intro="结果反对开挂肌肤抵抗力价格浮动")
        return HttpResponse("ok")


def showphoto(request):
    good = Goods.objects.filter(goodsName="book02").first()

    img_url = good.mainImg.url

    data = {"img_url": img_url}

    print(data)

    return render(request, 'showphoto.html', data)


def modgood(request):
    if request.method == "GET":
        goodsname = request.GET.get("goodsname")
        good = Goods.objects.get(goodsName=goodsname)
        return render(request, "modgood.html", locals())
    Goods.objects.filter(goodsName=request.POST.get("goodsname")).update(
        kind=request.POST.get("kind"),
        price=request.POST.get("price"),
        inventory=request.POST.get("inventory"),
        intro=request.POST.get("intro"),
    )
    return render(request, "modgoodac.html")


def delgood(request):
    Goods.objects.get(goodsName=request.GET.get("goodsname")).delete()
    data = {
        "msg": "ok",
        "你好": "嘿嘿嘿"
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


def buylog(request):
    goodsname = request.GET.get("goodsname")
    logs = BuyLog.objects.filter(goodsName=goodsname)
    return render(request, "buylog.html", locals())


def browsinglog(request):
    goodsname = request.GET.get("goodsname")
    logs = UserBrowsingLog.objects.filter(goodsName=request.GET.get("goodsname"))

    return render(request, "browsinglog.html", locals())


def addgood(request):
    if getAuthority(request) is None:
        return render(request, "plslogin.html")
    if getAuthority(request) != "seller":
        return HttpResponse("非卖家账号，不能添加商品")

    if request.method == "GET":
        return render(request, "addgood.html")

    mainImg = request.FILES.get("mainImg")
    imgs = request.FILES.getlist("imgs")
    Goods.objects.create(
        goodsName=request.POST.get("goodsname"),
        userName=Members.objects.filter(userName=request.COOKIES.get("username")).first(),
        kind=request.POST.get("kind"),
        price=request.POST.get("price"),
        inventory=request.POST.get("inventory"),
        intro=request.POST.get("intro"),
        mainImg=mainImg,
        img1=listGet(imgs, 0),
        img2=listGet(imgs, 1),
        img3=listGet(imgs, 2),
    )
    return HttpResponse("添加成功")


def gooddetail(request):
    goodsname = request.GET.get("goodsname")
    good = Goods.objects.filter(goodsName=goodsname).first()
    username = request.COOKIES.get("username")
    if good is None:
        return HttpResponse("商品不存在")
    imglist = []
    if good.img1.name != "":
        imglist.append(good.img1.url)
    if good.img2.name != "":
        imglist.append(good.img2.url)
    if good.img3.name != "":
        imglist.append(good.img3.url)
    userbrowerlogg = UserBrowsingLog.objects.filter(
        goodsName_id=goodsname,
        userName_id=username,
    )
    if len(userbrowerlogg) == 0:
        UserBrowsingLog.objects.create(
            goodsName_id=goodsname,
            userName_id=username,
        )
    else:
        userbrowerlogg.delete()
        UserBrowsingLog.objects.create(
            goodsName_id=goodsname,
            userName_id=username,
        )
    return render(request, "gooddetail.html", locals())


def shopCart(request):
    if request.method == "POST":
        goodsname = request.POST.get("goodsname")
        username = request.POST.get("username")
        num = int(request.POST.get("num"))
        shopcart = ShopCart.objects.filter(userName=Members.objects.filter(userName=username).first()).first()
        print(type(ShopCart.objects.filter(userName=Members.objects.filter(userName=username).first())))
        print(type(ShopCart.objects.filter(userName=Members.objects.filter(userName=username))))
        if shopcart is None:
            d = dict()
            d[goodsname] = num
            ShopCart.objects.create(
                userName=Members.objects.filter(userName=username).first(),
                shopCart=json.dumps(d)
            )
        else:
            d = json.loads(shopcart.shopCart)
            d[goodsname] = num

            ShopCart.objects.filter(userName=Members.objects.get(userName=username)).update(
                shopCart=json.dumps(d)
            )
        return render(request, "shopCartadd.html")
    else:
        username = request.COOKIES.get("username")
        shopcartob = ShopCart.objects.filter(userName=Members.objects.get(userName=username)).first()
        if shopcartob is None:
            d = {}
            return render(request, "shopcart.html", locals())
        else:
            d = json.loads(shopcartob.shopCart)
            return render(request, "shopcart.html", locals())


def settlecart(request):
    username = request.COOKIES.get("username")
    shopcartob = ShopCart.objects.filter(userName=Members.objects.get(userName=username)).first()
    if shopcartob is None:
        return HttpResponse("未登录或未购物车无物品")
    else:
        shopcart = json.loads(shopcartob.shopCart)

        totalp = 0
        for goodsname, num in shopcart.items():
            price = Goods.objects.get(goodsName=goodsname).price
            inventory = Goods.objects.get(goodsName=goodsname).inventory

            if inventory < num:
                return HttpResponse("商品" + goodsname + "库存不足")
            else:
                totalp = totalp + num * price
        balance = Members.objects.get(userName=username).balance
        if totalp >= balance:

            return HttpResponse(
                f"您的余额为{Members.objects.get(userName=username).balance},购物车总价为:{totalp},余额不足请充值")
        else:
            # 正式开始订单结算
            # 生成订单号为13位时间戳加上五位随机数字
            code = ""
            for i in range(5):
                code = code + str(random.randint(0, 9))
            orderNumber = str(round(time.time() * 1000)) + code
            Members.objects.filter(userName=username).update(balance=balance - totalp)

            for goodsname, num in shopcart.items():
                goodob = Goods.objects.get(goodsName=goodsname)
                price = goodob.price
                inventory = goodob.inventory
                kind = goodob.kind
                Goods.objects.filter(goodsName=goodsname).update(inventory=inventory - num)
                sellerbalance = Members.objects.get(userName=goodob.userName.userName).balance
                Members.objects.filter(userName=goodob.userName.userName).update(
                    balance=sellerbalance + price * num)

                # 添加购买日志
                BuyLog.objects.create(orderNumber=orderNumber,
                                      userName=Members.objects.get(userName=username),
                                      goodsName=goodsname,
                                      price=price,
                                      num=num,
                                      kind=kind
                                      )
            # 删除购物车
            shopcartob.delete()
            return HttpResponse("结算成功")


def delshopcart(request):
    username = request.COOKIES.get("username")
    goodsname = request.GET.get("goodsname")
    if goodsname is not None and username is not None:
        shopcartob = ShopCart.objects.filter(userName=username).first()
        if shopcartob is not None:
            shopcartjson = json.loads(shopcartob.shopCart)
            shopcartjson.pop(goodsname)
            ShopCart.objects.filter(userName=username).update(shopCart=json.dumps(shopcartjson))

            return HttpResponse('{"msg":"ok"}')

        else:
            return HttpResponse("购物车没有商品")
    else:
        return HttpResponse("未登录或者未指定删除的购物车商品名")


def usercenter(request):
    username = request.COOKIES.get("username")
    if username is not None:
        if request.method == "GET":
            balance = Members.objects.filter(userName=username).first().balance
            return render(request, "usercenter.html", locals())
        else:
            addb = request.POST.get("addbalance")
            addb = Decimal(addb).quantize(Decimal("0.00"), ROUND_HALF_UP)

            balance = Members.objects.filter(userName=username).first().balance
            balance = addb + balance
            Members.objects.filter(userName=username).update(balance=balance)
            msg = "充值成功"
            return render(request, "usercenter.html", locals())
    else:
        return redirect("/")


def manageseller(request):
    if getAuthority(request) == "admin":
        adminname = request.COOKIES.get("username")
        if request.method == "GET":
            sellersob = Members.objects.filter(authority="seller")
            return render(request, "manageseller.html", locals())

    else:
        return HttpResponse("非管理员或未登录")


def memberupd(request):
    if getAuthority(request) == "admin":
        if request.method == "GET":
            username = request.GET.get("username")
            userOb = Members.objects.get(userName=username)
            return render(request, "memberupd.html", locals())
        else:
            username = request.POST.get("username")
            password = request.POST.get("password")
            email = request.POST.get("email")
            Members.objects.filter(userName=username).update(password=password, email1=email)
            addoplog("membermanage", request.COOKIES.get("username"), request)
            return HttpResponse("修改成功")


def addmember(request):
    if getAuthority(request) == "admin":
        if request.method == "GET":
            return render(request, "addmember.html")
        else:
            username = request.POST.get("username")
            password = request.POST.get("password")
            email = request.POST.get("email")
            Members.objects.create(
                userName=username,
                password=password,
                authority="seller",
                email1=email,
            )
            addoplog("membermanage", request.COOKIES.get("username"), request)
            return HttpResponse("添加卖家账号成功")
    else:
        HttpResponse("未登录或非管理员")


def delmember(request):
    if getAuthority(request) == "admin":
        username = request.GET.get("username")
        userob = Members.objects.filter(userName=username).first()
        if userob is not None:
            userob.delete()
            addoplog("membermanage", request.COOKIES.get("username"), request)
            return HttpResponse('{"msg":"ok"}', content_type="application/json")

    return HttpResponse("出错")


def sellinfo(request):
    if getAuthority(request) == "admin":
        goodsName = request.GET.get("goodsName")
        if goodsName == "" or goodsName is None:
            listt = []
            for i in Goods.objects.all():
                tempgoodsName = i.goodsName
                dict1 = {
                    "mainImg": i.mainImg.url,
                    "goodsName": tempgoodsName,
                    "inventory": i.inventory,
                    "price": i.price,
                }
                totalprice = 0
                sellnum = 0
                for j in BuyLog.objects.filter(goodsName=tempgoodsName):
                    num = j.num
                    sellnum = sellnum + num
                    totalprice = totalprice + i.price * num
                dict1["sellnum"] = sellnum
                dict1["totalprice"] = totalprice
                dict1["inventoryPCT"] = f"{(i.inventory / (i.inventory + sellnum)):.2%}"
                listt.append(dict1)
            del goodsName
            addoplog("sellinfo", request.COOKIES.get("username"), request)
            return render(request, "sellinfo.html", locals())
        else:
            goodob = Goods.objects.filter(goodsName=goodsName).first()
            if goodob is None:
                return render(request, "sellinfo.html", locals())
            listt = []
            dict1 = {
                "mainImg": goodob.mainImg.url,
                "goodsName": goodsName,
                "inventory": goodob.inventory,
                "price": goodob.price,
            }
            totalprice = 0
            sellnum = 0
            for j in BuyLog.objects.filter(goodsName=goodsName):
                num = j.num
                sellnum = sellnum + num
                totalprice = totalprice + goodob.price * num
            dict1["sellnum"] = sellnum
            dict1["totalprice"] = totalprice
            dict1["inventoryPCT"] = f"{(goodob.inventory / (goodob.inventory + sellnum)):.2%}"
            listt.append(dict1)
            addoplog("sellinfo", request.COOKIES.get("username"), request)
            return render(request, "sellinfo.html", locals())
    return HttpResponse("未登录或不是管理员")


def sellerPERF(request):
    if getAuthority(request) == "admin":
        userName = request.GET.get("userName")
        if userName == "" or userName is None:
            listt = []
            tempuserdict = {}
            templist = []
            tempuserName = ""
            goodall = Goods.objects.all().order_by("userName_id")
            for i in goodall:
                if tempuserName == i.userName_id:
                    tempgoodsName = i.goodsName
                    dict1 = {
                        "mainImg": i.mainImg.url,
                        "goodsName": tempgoodsName,
                        "inventory": i.inventory,
                        "price": i.price.__float__(),
                    }
                    totalprice = 0
                    sellnum = 0
                    for j in BuyLog.objects.filter(goodsName=tempgoodsName):
                        num = j.num
                        sellnum = sellnum + num
                        totalprice = totalprice + i.price.__float__() * num
                    dict1["sellnum"] = sellnum
                    dict1["totalprice"] = totalprice
                    dict1["inventoryPCT"] = f"{(i.inventory / (i.inventory + sellnum)):.2%}"
                    templist.append(dict1)

                if tempuserName != i.userName_id and len(templist) > 0:
                    salestotal = 0
                    salesnumtotal = 0
                    INVtotal = 0
                    INVtotalPCT = ""
                    for j in templist:
                        salestotal = salestotal + j.get("totalprice")
                        salesnumtotal = salesnumtotal + j.get("sellnum")
                        INVtotal = INVtotal + j.get("inventory")
                    INVtotalPCT = f"{(INVtotal / (INVtotal + salesnumtotal)):.2%}"
                    tempuserdict = {
                        "userName": tempuserName,
                        "salestotal": salestotal,
                        "salesnumtotal": salesnumtotal,
                        "INVtotal": INVtotal,
                        "INVtotalPCT": INVtotalPCT,
                        "goods": templist
                    }
                    listt.append(copy.deepcopy(tempuserdict))
                    tempuserdict.clear()
                    templist.clear()
                    tempuserName = i.userName_id
                    tempgoodsName = i.goodsName
                    dict1 = {
                        "mainImg": i.mainImg.url,
                        "goodsName": tempgoodsName,
                        "inventory": i.inventory,
                        "price": i.price.__float__(),
                    }
                    totalprice = 0
                    sellnum = 0
                    for j in BuyLog.objects.filter(goodsName=tempgoodsName):
                        num = j.num
                        sellnum = sellnum + num
                        totalprice = totalprice + i.price.__float__() * num
                    dict1["sellnum"] = sellnum
                    dict1["totalprice"] = totalprice
                    dict1["inventoryPCT"] = f"{(i.inventory / (i.inventory + sellnum)):.2%}"
                    templist.append(dict1)
                if tempuserName != i.userName_id and len(templist) == 0:
                    tempuserName = i.userName_id
                    tempgoodsName = i.goodsName
                    dict1 = {
                        "mainImg": i.mainImg.url,
                        "goodsName": tempgoodsName,
                        "inventory": i.inventory,
                        "price": i.price.__float__(),
                    }
                    totalprice = 0
                    sellnum = 0
                    for j in BuyLog.objects.filter(goodsName=tempgoodsName):
                        num = j.num
                        sellnum = sellnum + num
                        totalprice = totalprice + i.price.__float__() * num
                    dict1["sellnum"] = sellnum
                    dict1["totalprice"] = totalprice
                    dict1["inventoryPCT"] = f"{(i.inventory / (i.inventory + sellnum)):.2%}"
                    templist.append(dict1)

            salestotal = 0
            salesnumtotal = 0
            INVtotal = 0
            INVtotalPCT = ""
            for j in templist:
                salestotal = salestotal + j.get("totalprice")
                salesnumtotal = salesnumtotal + j.get("sellnum")
                INVtotal = INVtotal + j.get("inventory")
            INVtotalPCT = f"{(INVtotal / (INVtotal + salesnumtotal)):.2%}"
            tempuserdict = {
                "userName": tempuserName,
                "salestotal": salestotal,
                "salesnumtotal": salesnumtotal,
                "INVtotal": INVtotal,
                "INVtotalPCT": INVtotalPCT,
                "goods": templist
            }
            listt.append(tempuserdict)
            addoplog("sellerPERF", request.COOKIES.get("username"), request)
            return render(request, "sellerPERF.html", {"listt": listt})
        else:
            listt = []
            templist = []
            goods = Goods.objects.filter(userName=userName)
            if goods.first() is None:
                return render(request, "sellerPERF.html", {"userName": userName})
            for i in goods:
                tempgoodsName = i.goodsName
                dict1 = {
                    "mainImg": i.mainImg.url,
                    "goodsName": tempgoodsName,
                    "inventory": i.inventory,
                    "price": i.price,
                }
                totalprice = 0
                sellnum = 0
                for j in BuyLog.objects.filter(goodsName=tempgoodsName):
                    num = j.num
                    sellnum = sellnum + num
                    totalprice = totalprice + i.price * num
                dict1["sellnum"] = sellnum
                dict1["totalprice"] = totalprice
                dict1["inventoryPCT"] = f"{(i.inventory / (i.inventory + sellnum)):.2%}"
                templist.append(dict1)
            salestotal = 0
            salesnumtotal = 0
            INVtotal = 0
            INVtotalPCT = ""
            for j in templist:
                salestotal = salestotal + j.get("totalprice")
                salesnumtotal = salesnumtotal + j.get("sellnum")
                INVtotal = INVtotal + j.get("inventory")
            INVtotalPCT = f"{(INVtotal / (INVtotal + salesnumtotal)):.2%}"
            tempuserdict = {
                "userName": userName,
                "salestotal": salestotal,
                "salesnumtotal": salesnumtotal,
                "INVtotal": INVtotal,
                "INVtotalPCT": INVtotalPCT,
                "goods": templist
            }
            listt.append(copy.deepcopy(tempuserdict))
            addoplog("sellerPERF", request.COOKIES.get("username"), request)
            return render(request, "sellerPERF.html", {"userName": userName, "listt": listt})

            # del userName
            # return render(request, "sellinfo.html", locals())

def browsehistory(request):
    username = request.COOKIES.get("username")
    if username is None:
        return redirect("/login")
    rangee = range(10)
    page = 0 if request.GET.get("page")==None else int(request.GET.get("page"))
    if username is not None:
        goodsNames = UserBrowsingLog.objects.filter(userName_id=username).order_by("-time").distinct()
        goods = goodsNames
        print(goods)

    return render(request, "browsehistory.html", locals())

def userbuylog(request):
    username = request.COOKIES.get("username")
    if username is None:
        return redirect("/login")
    buy_log = BuyLog.objects.filter(userName_id=username).order_by("-time")
    orderNumber = buy_log.values_list("orderNumber", flat=True).distinct()
    log = {i: buy_log.filter(orderNumber=i) for i in orderNumber}.items()
    return render(request, "userbuylog.html", locals())

