from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from axf.models import SliderShow, Product, MainDescription, Categorie, ChildCategorie, User, Cart, Order

from axf.sms import send_sms

import random, uuid

# Create your views here.

def index(request):
    return redirect("/home/")
def home(request):
    sliders = SliderShow.objects.all()
    mainList = MainDescription.objects.all()
    for item in mainList:
        products = []
        categoryProducts = Product.objects.filter(category_id=item.category_id)
        products.append(categoryProducts.get(product_id=item.product1))
        products.append(categoryProducts.get(product_id=item.product2))
        products.append(categoryProducts.get(product_id=item.product3))
        item.products = products
    return render(request, "home/home.html", {"sliders":sliders,"mainList":mainList})






def market(request, gid, cid, sid):
    # 获取左侧导航条数据
    leftCategorieList = Categorie.objects.all()
    # 获取子组信息数据
    childs = ChildCategorie.objects.filter(categorie__category_id=gid)

    #获取要展示的商品数据
    products = Product.objects.filter(category_id=gid)
    # 获取子组商品数据
    if cid != "0":
        products = products.filter(child_cid=cid)
    if sid == "1":
        products = products.order_by("-price")
    elif sid == "2":
        products = products.order_by("price")
    elif sid == "3":
        products = products.order_by("store_nums")
    #
    userCarts = Cart.objects.filter(user__tokenValue=request.COOKIES.get("token"))
    for userCart in userCarts:
        for product in products:
            if product.product_id == userCart.product.product_id:
                product.num = userCart.num
    return render(request, "market/market.html", {"leftCategorieList":leftCategorieList,"products":products, "childs":childs, "gid":gid, "cid":cid})

#修改购物车  增加、删除、是否选中
def carts(request):
    num = int(request.GET.get("num"))

    #已知用户
    user = request.user
    #获取要添加到购物车的商品
    gid = request.GET.get("gid")
    pid = request.GET.get("pid")
    product = Product.objects.filter(category_id=gid).get(product_id=pid)
    if product.store_nums == 0 and num == 1:
        return JsonResponse({"error": 2})

    # 当前用户的所有没进入订单的购物车信息
    usercarts =  Cart.objects.filter(user__tokenValue=request.token)
    try:
        productCart = usercarts.get(product__product_id=pid)
        #添加过
        productCart.num += num
        #库存
        product.store_nums -= num
        product.save()
        if productCart.num == 0:
            productCart.delete()
        else:
            productCart.isChose = not productCart.isChose
            productCart.save()
    except Cart.DoesNotExist as e:
        if num == 1:
            #没添加过
            productCart = Cart.create(user,None,product,1)
            productCart.save()
            #库存
            product.store_nums -= num
            product.save()
        elif num == -1:
            return JsonResponse({"error": 0, "num": 0})
    return JsonResponse({"error":0,"num":productCart.num,"isChose":productCart.isChose})

def cart(request):
    userCarts = Cart.objects.filter(user__tokenValue=request.COOKIES.get("token"))
    return render(request, "cart/cart.html", {"carts":userCarts})



def order(request):
    token = request.COOKIES.get("token")

    #用户
    user = User.objects.get(tokenValue=token)

    #创建订单
    order_id = str(uuid.uuid4())
    userOrder = Order.create(order_id, user, 10)
    userOrder.save()

    # 带下订单的购物车数据
    userCarts = Cart.objects.filter(user__tokenValue=token).filter(isChose=True)
    for userCart in userCarts:
        userCart.order = userOrder
        userCart.isOrder = True
        userCart.save()

    return JsonResponse({"error":0})















def mine(request):
    phone = request.session.get("phone", default="未登录")
    return render(request, "mine/mine.html", {"phone":phone})
def login(request):
    fromPath = request.GET.get("from")
    gid = request.GET.get("gid")
    cid = request.GET.get("cid")
    sid = request.GET.get("sid")
    if request.method == "GET":
        return render(request, "mine/login.html", {"fromPath":fromPath,"gid":gid,"cid":cid,"sid":sid})
    else:
        phone = request.POST.get("username")
        tokenValue = str(uuid.uuid4())
        try:
            user = User.objects.get(pk=phone)
            #登陆
            user.tokenValue = tokenValue
            user.save()
        except User.DoesNotExist as e:
            #注册
            user = User.create(phone, tokenValue)
            user.save()
        #将电话号码写入session
        request.session["phone"] = user.phoneNum

        if gid:
            response = redirect("/"+fromPath+"/"+gid+"/"+cid+"/"+sid+"/")
        else:
            response = redirect("/"+fromPath+"/")
        #将token写入cookie
        response.set_cookie("token", user.tokenValue)
        return response
def verifycode(request):
    mobile = request.GET.get("mobile")
    strArr = "0123456789"
    rand_str = ""
    for i in range(0, 6):
        rand_str += random.choice(strArr)
    text = "您的验证码是：%s。请不要把验证码泄露给其他人。"%rand_str
    # print(send_sms(text, mobile))
    print("***********************",rand_str)
    #将验证码存储到session
    request.session["verifycode"] = rand_str
    return JsonResponse({"data":rand_str})
from django.contrib.auth import logout
def quit(request):
    logout(request)
    return redirect("/mine/")
