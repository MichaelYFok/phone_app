from django.db import models

# Create your models here.

'''
轮播图表  表名slidershows    类名SliderShow
name
img
sort
trackid
'''
class SliderShow(models.Model):
    name = models.CharField(max_length=40)
    img  = models.CharField(max_length=200)
    sort = models.IntegerField()
    trackid = models.CharField(max_length=20)
    class Meta:
        db_table = "slidershows"
        # ordering = ["sort"]


'''
商品表    products
name            商品名
long_name       商品名+规格
product_id      商品id
store_nums      库存
specifics       规格
sort            排序   
market_price    超市价格  
price           价格     
category_id     分组id
child_cid       子组id
img             商品图片
keywords        搜索关键字
brand_id        品牌id
brand_name      品牌名称
safe_day        保质期长度
safe_unit       保质期单位模式
safe_unit_desc  保质期单位 
'''
class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(isDelete=False)
class Product(models.Model):
    objects = ProductManager()
    name = models.CharField(max_length=100)
    long_name = models.CharField(max_length=150)
    product_id = models.CharField(max_length=20)
    store_nums = models.IntegerField()
    specifics = models.CharField(max_length=20)
    sort = models.IntegerField()
    market_price = models.FloatField()
    price = models.FloatField()
    category_id = models.CharField(max_length=20)
    child_cid = models.CharField(max_length=20)
    img = models.CharField(max_length=200)
    keywords = models.CharField(max_length=200)
    brand_id = models.CharField(max_length=40)
    brand_name = models.CharField(max_length=200)
    safe_day = models.CharField(max_length=20)
    safe_unit = models.CharField(max_length=20)
    safe_unit_desc = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    class Meta:
        db_table = "products"
        # ordering = ["sort"]

'''  
主体信息表   maindescriptions
category_id     分组id
category_name   分组名称
sort            排序
img             图片
product1        商品1
product2        商品2
product3       商品3
'''

class MainDescription(models.Model):
    category_id = models.CharField(max_length=20)
    category_name = models.CharField(max_length=40)
    img = models.CharField(max_length=200)
    product1 = models.CharField(max_length=20)
    product2 = models.CharField(max_length=20)
    product3 = models.CharField(max_length=20)
    sort = models.IntegerField()
    class Meta:
        db_table = "maindescriptions"
        ordering = ["sort"]




'''
分组表     categories
category_id    组id（主键）
category_name  名称
sort           排序权重
'''
class CategorieManager(models.Manager):
    def get_queryset(self):
        return super(CategorieManager, self).get_queryset().filter(isDelete=False)
class Categorie(models.Model):
    objects = CategorieManager()
    category_id = models.CharField(max_length=20)
    category_name = models.CharField(max_length=40)
    sort = models.IntegerField()
    isDelete = models.BooleanField(default=False)
    class Meta:
        db_table = "categories"
        ordering = ["sort"]

'''
子组表     childcategories
child_id       子组id（主键）
child_name     名称
sort           排序权重
category       外键，所属的组
'''
class ChildCategorieManager(models.Manager):
    def get_queryset(self):
        return super(ChildCategorieManager, self).get_queryset().filter(isDelete=False)
class ChildCategorie(models.Model):
    objects = ChildCategorieManager()
    child_id = models.CharField(max_length=20)
    child_name = models.CharField(max_length=40)
    sort = models.IntegerField()
    categorie = models.ForeignKey("Categorie")
    isDelete = models.BooleanField(default=False)
    class Meta:
        db_table = "childcategories"
        ordering = ["sort"]


'''
用户表
手机号 (主键)
token值
创建时间
最后登录时间
'''
class UserManager(models.Manager):
    def get_queryset(self):
        return super(UserManager, self).get_queryset().filter(isDelete=False)
class User(models.Model):
    objects = UserManager()
    phoneNum = models.CharField(max_length=20, primary_key=True)
    tokenValue = models.CharField(max_length=100)
    createTime = models.DateTimeField(auto_now_add=True)
    lastTime = models.DateTimeField(auto_now=True)
    isDelete = models.BooleanField(default=False)
    class Meta():
        db_table = "users"
    @classmethod
    def create(cls, phoneNum, tokenValue):
        return cls(phoneNum=phoneNum, tokenValue=tokenValue)




'''
购物车表   carts
用户          user
所属订单      order   isNull
商品          product
数量          num
是否选中      isChose
是否进入订单  isOrder
'''
class CartManager(models.Manager):
    def get_queryset(self):
        return super(CartManager, self).get_queryset().filter(isOrder=False)
class Cart(models.Model):
    objects = CartManager()
    user = models.ForeignKey("User")
    order = models.ForeignKey("Order", null=True)
    product = models.ForeignKey("Product")
    num = models.IntegerField()
    isChose = models.BooleanField(default=True)
    isOrder = models.BooleanField(default=False)
    class Meta:
        db_table = "carts"
    @classmethod
    def create(cls, user, order, product, num):
        return cls(user=user, order=order, product=product, num=num)



'''
订单表      orders
订单编号    ordier_id  主键
所属用户    user
邮寄地址    address
总价        price
状态        flag
创建时间    createTime
修改时间    lastTime
是否删除    isDelete
'''
class Order(models.Model):
    order_id = models.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey("User")
    price = models.FloatField()
    flag = models.IntegerField(default=0)
    idDelete = models.BooleanField(default=False)
    createTime = models.DateTimeField(auto_now_add=True)
    lastTime = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "orders"
    @classmethod
    def create(cls, order_id, user, price):
        return cls(order_id=order_id, user=user, price=price)


'''
地址
'''

# class Address(models.Model):
#     name = models.CharField(max_length=20)
#     sex = models.BooleanField()
#     phoneNum = models.CharField(max_length=20)
#     detail = models.CharField(max_length=100)
#     user = models.ForeignKey("User")
#     isDelete = models.BooleanField(default=False)
#     class Meta:
#         db_table = "addresses"
#     @classmethod
#     def create(cls, name, sex, phoneNum, detail, user):
#         return cls(name=name,sex=sex,phoneNum=phoneNum,detail=detail, user=user)
#
