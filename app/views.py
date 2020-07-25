from django.shortcuts import render
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class T1View(ModelViewSet):
    queryset = Table1.objects.all()
    serializer_class = Table1Serializer
    lookup_field = "primary_key"
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('primary_key', 'property_one', )


class T2View(ModelViewSet):
    queryset = Table2.objects.all()
    serializer_class = Table2Serializer
    lookup_field = "foreign_primary_key"
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('foreign_primary_key', 'foreign_property', 'property_two', )


class PTView(ModelViewSet):
    queryset = PropertyTable.objects.all()
    serializer_class = PTSeriaizer
    lookup_field = "primary_key"
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('primary_key', 'times', )


class AT1View(ListCreateAPIView):
    # 上面的三个 View 直接使用了默认的端口方法。这一端口重写 POST 方法和 GET 方法，以演示 View 和 Serializer 的关系。
    serializer_class = AnotherT1Serializer

    def post(self, request, *args, **kwargs):
        print('Entering POST of AT1V.')
        print('+++++++++++++++++++++++++++++++++++++++')
        data_of_request = self.get_serializer(data=request.data)
        data_of_request.is_valid(raise_exception=True)
        # 下面的语句调用序列化器中的 create 方法：
        self.perform_create(data_of_request)
        # 如不然，使用下列语句
        # Table1.objects.update_or_create(property_one=data_of_request.data['property_one'])
        # 来进行创建条目操作，就不会进入到重写的 create 方法中，请注意区别。
        print('+++++++++++++++++++++++++++++++++++++++')
        print('Finish creating of AT1V.')
        content = data_of_request.data
        print('data_of_request is:')
        print(data_of_request)
        print('+++++++++++++++++++++++++++++++++++++++')
        print('content is:')
        print(content)
        return Response(content, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        # 在 View 层可以根据业务逻辑判断并抛出异常。比如这个 GET 对所有 GET 请求均返回异常，相当于不接受 GET 操作。
        # 要想从传来的请求读取数据，可以使用以下语句
        # data_of_request = self.get_serializer(data=request.data)
        # 此时的 data_of_request 包含很多信息：
        # AnotherT1Serializer(context={'request': <rest_framework.request.Request object>, 'format': None, 'view': <app.views.AT1View object>}, data=<QueryDict: {'csrfmiddlewaretoken': ['BF6pxgTQpBIce3vux4q9Kxo9CUyhqLQD4j65Lw8xf7exJOZnxYIpQKdlYjSDL94O'], 'property_one': ['AnotherTry']}>):
        #     primary_key = IntegerField(read_only=True)
        #     property_one = CharField(max_length=15, validators=[<UniqueValidator(queryset=Table1.objects.all())>])
        # 如果想提取传来的数据，再使用一次：
        # content = data_of_request.data
        # 此时 content 成为一个字典，其中保存了键值对：
        # {'property_one': 'AnotherTry'}
        # 这样你就可以通过 content['property'] 来访问传入数据的某个属性了。
        raise exceptions.APIException('GET method is forbidden.')
