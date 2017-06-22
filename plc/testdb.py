#encoding=utf8
from django.http import HttpResponse
from demo.models import Test

#数据库操作
def dbDemo(request):
	#添加数据
	test1 = Test(name = 'w3cschool.cc')
	test1.save()

	#通过objects这个模型管理器的all() 获得所有数据行，相当于SQL中的SELECT * FROM 
	list = Test.objects.all()
	print list
	#filter 相当于SQL中的WHERE,可设置条件过滤结果
	response0 = Test.objects.filter(id=1)
	print response0
	#获取单个对象
	response1 = Test.objects.get(id=1)
	print response1
	return HttpResponse("<p>数据库操作成功!</p>")

