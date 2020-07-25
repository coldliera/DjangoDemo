from rest_framework.serializers import ModelSerializer
from rest_framework import serializers, exceptions
from .models import *
from django.core import serializers
import json


class Table1Serializer(ModelSerializer):
    class Meta:
        model = Table1
        fields = '__all__'


class AnotherT1Serializer(ModelSerializer):
    class Meta:
        model = Table1
        fields = '__all__'

    def create(self, validated_data):
        print('Entering CREATE of AT1S.')
        print('---------------------------------------------------------')
        created_object = Table1.objects.create(**validated_data)
        print('---------------------------------------------------------')
        print('Finish creating objects in Table1.')
        return created_object

    def update(self, instance, validated_data):
        print('Entering UPDATE of AT1S.')
        print('---------------------------------------------------------')
        instance.primary_key = validated_data.get('primary_key', instance.primary_key)
        instance.property_one = validated_data.get('property_one', instance.property_one)
        instance.save()
        print('---------------------------------------------------------')
        print('Finish updating objects in AT1S.')
        return instance


class Table2Serializer(ModelSerializer):
    class Meta:
        model = Table2
        fields = '__all__'

    def create(self, validated_data):
        print('Entering CREATE of T2S.')
        created_object = Table2.objects.create(**validated_data)
        print('Finish creating objects in Table2.')
        data_of_created_object = created_object.property_two
        # 如果想要获取的列是一个对象而非一个值（往往在这个列是一个外键时出现，此时直接访问列.property返回的是被引用的对象），那么可以通过下列语句获取可操作的值:
        # data_of_an_object = json.loads(serializers.serialize("json", [object.property_name,]))[0]['fields']
        # 其中 object 是当前对象，property_name 是要获取的列名。它首先使用 serializers 提供的 serialize 方法把被引用的对象序列化，再用 json 提供的 loads 方法把 json 消息转化为字典。
        # ['fields']是固定的。你可以试试为什么需要这样操作。
        # 这一语句返回的是被引用对象的所有列的值，以字典形式存放。因此你就可以从当前表中的一条记录，溯回其中引用的被引用记录的各个列的值了。比如：
        # data_from_record = data_of_an_object['property_name']
        print('Finish serializing data fo created object. Data is:')
        print(data_of_created_object)
        related_object_from_PT = PropertyTable.objects.filter(primary_key=data_of_created_object)
        print('The QuerySet where primary_key=data_of_created_object["property_two"] of filtering PropertyTable is:')
        print(related_object_from_PT)
        if related_object_from_PT.count() == 0:
            print('There is no former record. Create a new record in PropertyTable.')
            PropertyTable.objects.create(primary_key=data_of_created_object, times=1)
        else:
            # 这里 .count() 和 .first() 都是 QuerySet 对象的方法。这是因为 Model.objects.filter() 返回满足过滤条件的 QuerySet.
            # 另: Model.objects.all() 返回表中的所有项，也是返回 QuerySet。
            print('Record Existed. Update the record.')
            old_times = related_object_from_PT.first().times    # 从一个表中的对象获取属性直接使用 .property
            related_object_from_PT.update(times=old_times+1)
        return created_object

    def update(self, instance, validated_data):
        print('Entering UPDATE of T2S.')
        instance.foreign_primary_key = validated_data.get('foreign_primary_key', instance.foreign_primary_key)
        instance.foreign_property = validated_data.get('foreign_property', instance.foreign_property)
        instance.property_two = validated_data.get('property_two', instance.property_two)
        # 以下几行与create方法中很类似，区别在于使用get方法获得正在更新的对象
        updated_object = Table2.objects.get(foreign_primary_key=instance.foreign_primary_key)
        print('Finish updating objects in Table2.')
        data_of_created_object = updated_object.property_two
        print('Finish serializing data fo updated object. Data is:')
        print(data_of_created_object)
        related_object_from_PT = PropertyTable.objects.filter(primary_key=data_of_created_object)
        print('The QuerySet where primary_key=data_of_created_object["property_two"] of filtering PropertyTable is:')
        print(related_object_from_PT)
        if related_object_from_PT.count() == 0:
            print('There is no former record. Create a new record in PropertyTable.')
            PropertyTable.objects.create(primary_key=data_of_created_object, times=1)
        else:
            print('Record Existed. Update the record.')
            old_times = related_object_from_PT.first().times
            related_object_from_PT.update(times=old_times+1)    # 请注意使用 .update() 方法时不会进入在上面序列化器中重写的 update 方法
        # 注意: 必须使用 instance.save() 否则实例的更新不会被储存
        instance.save()
        return instance


class PTSeriaizer(ModelSerializer):
    class Meta:
        model = PropertyTable
        fields = '__all__'

    def update(self, instance, validated_data):
        print('Entering UPDATE of PTS.')
        updating_object = PropertyTable.objects.filter(primary_key=validated_data.get('primary_key', instance.primary_key))
        if updating_object.count() != 0 and updating_object.first().times >= 5:
            # 当抛出异常时会返回对应的状态码。异常有许多种，可以根据情况调用 exceptions 中提供的各类异常。
            raise exceptions.ValidationError
        instance.primary_key = validated_data.get('primary_key', instance.primary_key)
        instance.times = validated_data.get('times', instance.times)
        instance.save()
        return instance
