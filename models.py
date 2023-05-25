from django.db import models

class Users(models.Model):
    id = models.CharField('用户编号', max_length=13, primary_key=True)
    userName = models.CharField('用户账号', db_column='user_name', max_length=32, null=False)
    passWord = models.CharField('用户密码', db_column='pass_word', max_length=32, null=False)
    name = models.CharField('用户姓名', max_length=20, null=False)
    age = models.IntegerField('用户年龄', null=False)
    gender = models.CharField('用户性别', max_length=4, null=False)
    phone = models.CharField('联系电话', max_length=11, null=False)
    address = models.CharField('联系地址', max_length=64, null=False)
    type = models.IntegerField('用户身份', null=False)
    class Meta:
        db_table = 'users'

class MemberLevel(models.Model):
    id = models.CharField('记录编号', max_length=13, primary_key=True)
    name = models.CharField('级别名称', max_length=20, null=False)
    total = models.FloatField('消费额度', null=False)
    discount = models.FloatField('折扣优惠', null=False)
    class Meta:
        db_table = 'member_level'

class MemberInfos(models.Model):
    phone = models.CharField('会员账号', max_length=11, primary_key=True)
    total = models.FloatField('消费额度', null=False)
    createTime = models.CharField('记录时间', db_column='create_time', max_length=19, null=False)
    level = models.ForeignKey(MemberLevel, on_delete=models.CASCADE, db_column="level_id", max_length=13)
    class Meta:
        db_table = 'member_infos'

class GoodTypes(models.Model):
    id = models.CharField('记录编号', max_length=13, primary_key=True)
    name = models.CharField('类别名称', max_length=20, null=False)
    createTime = models.CharField('记录时间', db_column='create_time', max_length=19, null=False)
    class Meta:
        db_table = 'good_types'

class GoodInfos(models.Model):
    id = models.CharField('商品编号', max_length=13, primary_key=True)
    name = models.CharField('商品名称', max_length=64, null=False)
    price = models.FloatField('商品售价', null=False)
    total = models.FloatField('商品库存', null=False)
    createTime = models.CharField('记录时间', db_column='create_time', max_length=19, null=False)
    type = models.ForeignKey(GoodTypes, on_delete=models.CASCADE, db_column="type_id", max_length=13)
    class Meta:
        db_table = 'good_infos'

class Sals(models.Model):
    id = models.CharField('记录编号', max_length=13, primary_key=True)
    salTotal = models.FloatField('销售总额', null=False)
    discount = models.FloatField('折扣力度', null=False)
    payTotal = models.FloatField('实付费用', null=False)
    createTime = models.CharField('记录时间', db_column='create_time', max_length=19, null=False)
    member = models.ForeignKey(MemberInfos, on_delete=models.CASCADE, db_column="member_id", max_length=13, null=True)
    class Meta:
        db_table = 'sals'

class SalLogs(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    good = models.ForeignKey(GoodInfos, on_delete=models.CASCADE, db_column="good_id", max_length=13)
    salPrice = models.FloatField('商品售价', null=False)
    salTotal = models.FloatField('出售数目', null=False)
    sal = models.ForeignKey(Sals, on_delete=models.CASCADE, db_column="sal_id", max_length=13)
    class Meta:
        db_table = 'sal_logs'

class Stocks(models.Model):
    id = models.CharField('记录编号', max_length=13, primary_key=True)
    stockTotal = models.FloatField('采购总额', null=False)
    createTime = models.CharField('记录时间', db_column='create_time', max_length=19, null=False)
    class Meta:
        db_table = 'stocks'

class StockLogs(models.Model):
    id = models.AutoField('记录编号', primary_key=True)
    good = models.ForeignKey(GoodInfos, on_delete=models.CASCADE, db_column="good_id", max_length=13)
    stockPrice = models.FloatField('商品进价', null=False)
    stockTotal = models.FloatField('采购数目', null=False)
    stock = models.ForeignKey(Stocks, on_delete=models.CASCADE, db_column="stock_id", max_length=13)
    class Meta:
        db_table = 'stock_logs'