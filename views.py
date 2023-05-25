import json
import time

from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from app import models

'''
请求控制基类
'''
class BaseView(View):
    '''
    检查指定的参数是否存在
    存在返回 True
    不存在返回 False
    '''
    def isExit(param):

        if (param == None) or (param == ''):
            return False
        else:
            return True

    '''
    转换分页查询信息
    '''
    def parasePage(pageIndex, pageSize, pageTotal, count, data):

        return {'pageIndex': pageIndex, 'pageSize': pageSize, 'pageTotal': pageTotal, 'count': count, 'data': data}

    '''
    转换分页查询信息
    '''
    def parasePage(pageIndex, pageSize, pageTotal, count, data):
        return {'pageIndex': pageIndex, 'pageSize': pageSize, 'pageTotal': pageTotal, 'count': count, 'data': data}

    '''
    成功响应信息
    '''
    def success(msg='处理成功'):
        resl = {'code': 0, 'msg': msg}
        return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')

    '''
    成功响应信息, 携带数据
    '''
    def successData(data, msg='处理成功'):
        resl = {'code': 0, 'msg': msg, 'data': data}
        return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')

    '''
    系统警告信息
    '''
    def warn(msg='操作异常，请重试'):
        resl = {'code': 1, 'msg': msg}
        return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')

    '''
    系统异常信息
    '''
    def error(msg='系统异常'):
        resl = {'code': 2, 'msg': '系统异常'}
        return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')

'''
系统请求处理
'''
class SysView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'login':
            return render(request, 'login.html')

        elif module == 'logout':

            del request.session["user"]

            return HttpResponseRedirect('/marks/login')

        if module == 'info':

            return SysView.getSessionInfo(request)

        elif module == 'show':
            return render(request, 'Index.html')

    def post(self, request, module, *args, **kwargs):

        if module == 'login':

            return SysView.login(request)

        if module == 'info':
            return SysView.updSessionInfo(request)

        if module == 'pwd':
            return SysView.updSessionPwd(request)

    def login(request):

        userName = request.POST.get('userName')
        passWord = request.POST.get('passWord')

        user = models.Users.objects.filter(userName=userName)

        if (user.exists()):

            user = user.first()
            if user.passWord == passWord:
                login_user = {
                    'id': user.id,
                    'userName': user.userName,
                    'passWord': user.passWord,
                    'name': user.name,
                    'age': user.age,
                    'gender': user.gender,
                    'type': user.type,
                }
                request.session["user"] = login_user

                return SysView.success()
            else:
                return SysView.warn('用户密码输入错误')
        else:
            return SysView.warn('用户名输入错误')

    def getSessionInfo(request):

        user = request.session.get('user')

        data = models.Users.objects.filter(id=user['id'])

        resl = {}
        for item in data:
            resl = {
                'id': item.id,
                'userName': item.userName,
                'passWord': item.passWord,
                'gender': item.gender,
                'name': item.name,
                'age': item.age,
                'address': item.address,
                'phone': item.phone,
                'type': item.type,
            }

        return SysView.successData(resl)

    def updSessionInfo(request):

        user = request.session.get('user')

        models.Users.objects.filter(id=user['id']).update(
            userName=request.POST.get('userName'),
            name=request.POST.get('name'),
            age=request.POST.get('age'),
            gender=request.POST.get('gender'),
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
        )

        data = models.Users.objects.filter(id=user['id'])

        resl = {}
        for item in data:
            resl = {
                'id': item.id,
                'userName': item.userName,
                'passWord': item.passWord,
                'gender': item.gender,
                'name': item.name,
                'age': item.age,
                'address': item.address,
                'phone': item.phone,
                'type': item.type,
            }

        del request.session["user"]
        request.session["user"] = resl

        return SysView.successData(user)

    def updSessionPwd(request):

        user = request.session.get('user')

        models.Users.objects.filter(id=user['id']).update(
            passWord=request.POST.get('password'),
        )

        data = models.Users.objects.filter(id=user['id'])

        resl = {}
        for item in data:
            resl = {
                'id': item.id,
                'userName': item.userName,
                'passWord': item.passWord,
                'gender': item.gender,
                'name': item.name,
                'age': item.age,
                'address': item.address,
                'phone': item.phone,
                'type': item.type,
            }

        del request.session["user"]
        request.session["user"] = resl

        return SysView.success()

'''
会员级别信息处理
'''
class LevelView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'info':

            return LevelView.getInfo(request)
        elif module == 'page':

            return LevelView.getPageInfo(request)
        elif module == 'show':

            return render(request, "MemberLevel.html")

    def post(self, request, module, *args, **kwargs):

        if module == 'add':

           return LevelView.addInfo(request)
        elif module == 'upd':

            return LevelView.updInfo(request)
        elif module == 'del':

            return LevelView.delInfo(request)
        else:

            return BaseView.error()

    def getInfo(request):

        data = models.MemberLevel.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id,
            'name': data.name,
            'total': data.total,
            'discount': data.discount
        }

        return BaseView.successData(resl)

    def getPageInfo(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')

        if BaseView.isExit(name):
            data = models.MemberLevel.objects.all().filter(name__contains=name)
        else:
            data = models.MemberLevel.objects.all()

        paginator = Paginator(data, pageSize)

        resl = []
        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'name': item.name,
                'total': item.total,
                'discount': item.discount
            }
            resl.append(temp)

        temp = BaseView.parasePage(pageIndex, pageSize,
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(temp)

    def addInfo(request):

        models.MemberLevel.objects.create(id=int(time.time()),
                                          name=request.POST.get('name'),
                                          total=request.POST.get('total'),
                                          discount=request.POST.get('discount')
                                          )
        return BaseView.success()

    def updInfo(request):

        models.MemberLevel.objects.filter(id=request.POST.get('id')) \
            .update(
                name=request.POST.get('name'),
                total=request.POST.get('total'),
                discount=request.POST.get('discount')
            )
        return BaseView.success()

    def delInfo(request):

        if models.MemberInfos.objects.filter(level__id=request.POST.get('id')).exists():

            return BaseView.warn('存在关联会员无法删除')
        else:
            models.MemberLevel.objects.filter(id=request.POST.get('id')).delete()
            return BaseView.success()

'''
会员信息处理
'''
class MembersView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'info':

            return MembersView.getInfo(request)
        elif module == 'page':

            return MembersView.getPageInfo(request)
        elif module == 'show':

            levels = models.MemberLevel.objects.all().values()

            return render(request, "MemberInfos.html", {'levels': list(levels)})

    def post(self, request, module, *args, **kwargs):

        if module == 'add':

           return MembersView.addInfo(request)
        elif module == 'upd':

            return MembersView.updInfo(request)
        elif module == 'del':

            return MembersView.delInfo(request)
        else:

            return BaseView.error()

    def getInfo(request):

        data = models.MemberInfos.objects.filter(phone=request.GET.get('phone')).first()

        resl = {
            'phone': data.phone,
            'total': data.total,
            'createTime': data.createTime,
            'levelId': data.level.id,
            'levelName': data.level.name,
        }

        return BaseView.successData(resl)

    def getPageInfo(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        phone = request.GET.get('phone')
        levelId = request.GET.get('levelId')

        qruery = Q();

        if BaseView.isExit(phone):
            qruery = qruery & Q(phone__contains=phone)

        if BaseView.isExit(levelId):
            qruery = qruery & Q(level__id=levelId)

        data = models.MemberInfos.objects.filter(qruery)

        paginator = Paginator(data, pageSize)

        resl = []
        for item in list(paginator.page(pageIndex)):
            temp = {
                'phone': item.phone,
                'total': item.total,
                'createTime': item.createTime,
                'levelId': item.level.id,
                'levelName': item.level.name,
            }
            resl.append(temp)

        temp = BaseView.parasePage(pageIndex, pageSize,
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(temp)

    def addInfo(request):

        models.MemberInfos.objects.create(phone=request.POST.get('phone'),
                                          total=request.POST.get('total'),
                                          level=models.MemberLevel.objects.get(id=request.POST.get('levelId')),
                                          createTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                          )
        return BaseView.success()

    def updInfo(request):

        models.MemberInfos.objects.filter(phone=request.POST.get('phone')) \
            .update(
                total=request.POST.get('total'),
                level=models.MemberLevel.objects.get(id=request.POST.get('levelId')),
            )
        return BaseView.success()

    def delInfo(request):

        models.Sals.objects.filter(member__phone=request.POST.get('phone')) \
            .update(
            member=None
        )

        models.MemberInfos.objects.filter(phone=request.POST.get('phone')).delete()
        return BaseView.success()

'''
商品信息处理
'''
class GoodTypesView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'info':

            return GoodTypesView.getInfo(request)
        elif module == 'page':

            return GoodTypesView.getPageInfo(request)
        elif module == 'show':

            return render(request, "GoodTypes.html")

    def post(self, request, module, *args, **kwargs):

        if module == 'add':

           return GoodTypesView.addInfo(request)
        elif module == 'upd':

            return GoodTypesView.updInfo(request)
        elif module == 'del':

            return GoodTypesView.delInfo(request)
        else:

            return BaseView.error()

    def getInfo(request):

        data = models.GoodTypes.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id,
            'name': data.name,
            'createTime': data.createTime
        }

        return BaseView.successData(resl)

    def getPageInfo(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')

        qruery = Q();

        if BaseView.isExit(name):
            qruery = qruery & Q(name__contains=name)

        data = models.GoodTypes.objects.filter(qruery)
        paginator = Paginator(data, pageSize)

        resl = []
        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'name': item.name,
                'createTime': item.createTime
            }
            resl.append(temp)

        temp = BaseView.parasePage(pageIndex, pageSize,
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(temp)

    def addInfo(request):

        models.GoodTypes.objects.create(id=int(time.time()),
                                        name=request.POST.get('name'),
                                        createTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                        )
        return BaseView.success()

    def updInfo(request):

        models.GoodTypes.objects.filter(id=request.POST.get('id')) \
            .update(
                name=request.POST.get('name')
            )
        return BaseView.success()

    def delInfo(request):

        if models.GoodInfos.objects.filter(type__id=request.POST.get('id')).exists():

            return BaseView.warn('存在关联商品无法删除')
        else:
            models.GoodTypes.objects.filter(id=request.POST.get('id')).delete()
            return BaseView.success()

'''
商品信息处理
'''
class GoodInfoView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'info':

            return GoodInfoView.getInfo(request)
        elif module == 'page':

            return GoodInfoView.getPageInfo(request)
        elif module == 'show':

            types = models.GoodTypes.objects.all().values()

            return render(request, "GoodInfos.html", {'types': list(types)})

    def post(self, request, module, *args, **kwargs):

        if module == 'add':

           return GoodInfoView.addInfo(request)
        elif module == 'upd':

            return GoodInfoView.updInfo(request)
        elif module == 'del':

            return GoodInfoView.delInfo(request)
        else:

            return BaseView.error()

    def getInfo(request):

        data = models.GoodInfos.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id,
            'name': data.name,
            'price': data.price,
            'total': data.total,
            'typeId': data.type.id,
            'typeName': data.type.name,
            'createTime': data.createTime
        }

        return BaseView.successData(resl)

    def getPageInfo(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        name = request.GET.get('name')
        typeId = request.GET.get('typeId')

        qruery = Q();

        if BaseView.isExit(name):
            qruery = qruery & Q(name__contains=name)

        if BaseView.isExit(typeId):
            qruery = qruery & Q(type__id=typeId)

        data = models.GoodInfos.objects.filter(qruery)
        paginator = Paginator(data, pageSize)

        resl = []
        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'name': item.name,
                'price': item.price,
                'total': item.total,
                'typeId': item.type.id,
                'typeName': item.type.name,
                'createTime': item.createTime
            }
            resl.append(temp)

        temp = BaseView.parasePage(pageIndex, pageSize,
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(temp)

    def addInfo(request):

        models.GoodInfos.objects.create(id=int(time.time()),
                                        name=request.POST.get('name'),
                                        price=request.POST.get('price'),
                                        total=request.POST.get('total'),
                                        type = models.GoodTypes.objects.get(id=request.POST.get('typeId')),
                                        createTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                        )
        return BaseView.success()

    def updInfo(request):

        models.GoodInfos.objects.filter(id=request.POST.get('id')) \
            .update(
                name=request.POST.get('name'),
                price=request.POST.get('price'),
                total=request.POST.get('total'),
                type=models.GoodTypes.objects.get(id=request.POST.get('typeId'))
            )
        return BaseView.success()

    def delInfo(request):

        if models.SalLogs.objects.filter(good__id=request.POST.get('id')).exists() | \
                models.StockLogs.objects.filter(good__id=request.POST.get('id')).exists():

            return BaseView.warn('存在关联记录无法删除')
        else:

            models.GoodInfos.objects.filter(id=request.POST.get('id')).delete()
            return BaseView.success()



'''
系统用户信息处理
'''
class UsersView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'info':

            return UsersView.getInfo(request)
        elif module == 'page':

            return UsersView.getPageInfo(request)
        elif module == 'show':

            return render(request, "Users.html")

    def post(self, request, module, *args, **kwargs):

        if module == 'add':

           return UsersView.addInfo(request)
        elif module == 'upd':

            return UsersView.updInfo(request)
        elif module == 'del':

            return UsersView.delInfo(request)
        else:

            return BaseView.error()

    def getInfo(request):

        data = models.Users.objects.filter(id=request.GET.get('id')).first()

        resl = {
            'id': data.id,
            'userName': data.userName,
            'passWord': data.passWord,
            'name': data.name,
            'age': data.age,
            'gender': data.gender,
            'phone': data.phone,
            'address': data.address,
            'type': data.type,
        }

        return BaseView.successData(resl)

    def getPageInfo(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        userName = request.GET.get('userName')
        name = request.GET.get('name')
        phone = request.GET.get('phone')

        qruery = Q();

        if BaseView.isExit(userName):
            qruery = qruery & Q(userName__contains = userName)

        if BaseView.isExit(name):
            qruery = qruery & Q(name__contains = name)

        if BaseView.isExit(phone):
            qruery = qruery & Q(phone__contains = phone)

        data = models.Users.objects.filter(qruery)

        paginator = Paginator(data, pageSize)

        resl = []
        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'userName': item.userName,
                'passWord': item.passWord,
                'name': item.name,
                'age': item.age,
                'gender': item.gender,
                'phone': item.phone,
                'address': item.address,
                'type': item.type,
            }
            resl.append(temp)

        temp = BaseView.parasePage(pageIndex, pageSize,
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(temp)

    def addInfo(request):

        models.Users.objects.create(id=int(time.time()),
                                            userName = request.POST.get('userName'),
                                            passWord = request.POST.get('passWord'),
                                            name = request.POST.get('name'),
                                            age = request.POST.get('age'),
                                            gender = request.POST.get('gender'),
                                            phone = request.POST.get('phone'),
                                            address = request.POST.get('address'),
                                            type = request.POST.get('type'),
                                          )
        return BaseView.success()

    def updInfo(request):

        models.Users.objects.filter(id=request.POST.get('id')) \
            .update(
                userName=request.POST.get('userName'),
                name=request.POST.get('name'),
                age=request.POST.get('age'),
                gender=request.POST.get('gender'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address'),
                type=request.POST.get('type'),
            )
        return BaseView.success()

    def delInfo(request):

        models.Users.objects.filter(id=request.POST.get('id')).delete()
        return BaseView.success()

'''
销售记录处理
'''
class SalsView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'page':

            return SalsView.getPageInfo(request)
        elif module == 'show':

            return render(request, "Sals.html")

    def post(self, request, module, *args, **kwargs):
        if module == 'add':

            return SalsView.addInfo(request)

        elif module == 'del':

            return SalsView.delInfo(request)
        else:

            return BaseView.error()

    def getPageInfo(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)
        member = request.GET.get('member')

        qruery = Q();

        if BaseView.isExit(member):
            qruery = qruery & Q(member__phone__contains = member)

        data = models.Sals.objects.filter(qruery).order_by("-createTime")

        paginator = Paginator(data, pageSize)

        resl = []
        for item in list(paginator.page(pageIndex)):

            temp = {
                'id': item.id,
                'salTotal': item.salTotal,
                'discount': item.discount,
                'payTotal': item.payTotal,
                'createTime': item.createTime,
                'member': '----' if item.member == None else item.member.phone,
            }
            resl.append(temp)

        temp = BaseView.parasePage(pageIndex, pageSize,
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(temp)

    @transaction.atomic
    def addInfo(request):

        # 销售单信息
        isSal = True
        salId = int(time.time());
        salTotal = 0.00;
        createTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        goodIds = request.POST.getlist('goodIds[]')
        goodTotals = request.POST.getlist('goodTotals[]')
        memberId = request.POST.get('memberId')

        # 循环计算售价总和
        for i in range(len(goodIds)):

            goodInfo = models.GoodInfos.objects.filter(id=goodIds[i]).first()
            if (goodInfo.total - float(goodTotals[i])) < 0:
                isSal = False
                break
            else:
                salTotal = salTotal +  float(goodTotals[i])  * float(goodInfo.price)

        if isSal:

            if SalsView.isExit(memberId):

                member = models.MemberInfos.objects.filter(phone = memberId).first()
                models.Sals.objects.create(id = salId,
                                           member = member,
                                           salTotal = round(salTotal, 2),
                                           discount = round(member.level.discount, 2),
                                           payTotal = round(salTotal * member.level.discount, 2),
                                           createTime = createTime
                                           )

                models.MemberInfos.objects.filter(phone=memberId) \
                    .update(
                            total = member.total + round(salTotal * member.level.discount, 2),
                            )
            else:
                models.Sals.objects.create(id = salId,
                                            salTotal = round(salTotal, 2),
                                            discount = 0.00,
                                            payTotal = round(salTotal, 2),
                                            createTime = createTime
                                            )

            for i in range(len(goodIds)):

                goodInfo = models.GoodInfos.objects.filter(id=goodIds[i]).first()
                models.SalLogs.objects.create(
                                            sal = models.Sals.objects.get(id=salId),
                                            good = goodInfo,
                                            salPrice = goodInfo.price,
                                            salTotal = float(goodTotals[i])
                                           )
                models.GoodInfos.objects.filter(id=goodIds[i]) \
                    .update(
                    total=goodInfo.total - float(goodTotals[i])
                )

            return SalsView.success()
        else:
            return SalsView.warn('选择商品库存不足')



'''
销售清单处理
'''
class SalLogsView(BaseView):

    def get(self, request, *args, **kwargs):

        return SalLogsView.getSalInfos(request)

    def getSalInfos(request):

        resl = []

        salLogs = models.SalLogs.objects.filter(sal__id = request.GET.get('salId'))

        for item in salLogs:
            temp = {
                'id': item.id,
                'salPrice': item.salPrice,
                'salTotal': item.salTotal,
                'goodId': item.good.id,
                'goodName': item.good.name,
                'nowPrice': item.good.price,
            }
            resl.append(temp)

        return SalLogsView.successData(resl)



'''
采购记录处理
'''
class StocksView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'page':

            return StocksView.getPageInfo(request)
        elif module == 'show':

            return render(request, "Stocks.html")

    def post(self, request, module, *args, **kwargs):
        if module == 'add':

            return StocksView.addInfo(request)

        elif module == 'del':

            return StocksView.delInfo(request)
        else:

            return BaseView.error()

    def getPageInfo(request):

        pageIndex = request.GET.get('pageIndex', 1)
        pageSize = request.GET.get('pageSize', 10)

        data = models.Stocks.objects.all().order_by("-createTime")

        paginator = Paginator(data, pageSize)

        resl = []
        for item in list(paginator.page(pageIndex)):
            temp = {
                'id': item.id,
                'stockTotal': item.stockTotal,
                'createTime': item.createTime
            }
            resl.append(temp)

        temp = BaseView.parasePage(pageIndex, pageSize,
                                   paginator.page(pageIndex).paginator.num_pages,
                                   paginator.count, resl)

        return BaseView.successData(temp)

    @transaction.atomic
    def addInfo(request):

        # 采购单信息
        stockId = int(time.time());
        stockTotal = 0.00;
        createTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        goodIds = request.POST.getlist('goodIds[]')
        goodTotals = request.POST.getlist('goodTotals[]')
        goodPrices = request.POST.getlist('goodPrices[]')

        # 循环计算采购总额
        for i in range(len(goodIds)):

            stockTotal = stockTotal + float(goodTotals[i]) * float(goodPrices[i])

        models.Stocks.objects.create(id = stockId,
                                     stockTotal = stockTotal,
                                     createTime=createTime
                                    )

        for i in range(len(goodIds)):

            goodInfo = models.GoodInfos.objects.filter(id=goodIds[i]).first()

            models.StockLogs.objects.create(
                stock=models.Stocks.objects.get(id=stockId),
                good=goodInfo,
                stockPrice=float(goodPrices[i]),
                stockTotal=float(goodTotals[i])
            )
            models.GoodInfos.objects.filter(id=goodIds[i]) \
                .update(
                total=goodInfo.total + float(goodTotals[i])
            )

        return SalsView.success()


'''
采购清单处理
'''
class StockLogsView(BaseView):

    def get(self, request, *args, **kwargs):

        return StockLogsView.getStockInfos(request)

    def getStockInfos(request):
        resl = []

        stockLogs = models.StockLogs.objects.filter(stock__id=request.GET.get('stockId'))

        for item in stockLogs:
            temp = {
                'id': item.id,
                'stockPrice': item.stockPrice,
                'stockTotal': item.stockTotal,
                'goodId': item.good.id,
                'goodName': item.good.name,
                'nowPrice': item.good.price,
            }
            resl.append(temp)

        return StockLogsView.successData(resl)
