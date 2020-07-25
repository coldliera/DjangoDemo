from django.db import models

# Create your models here.


class Table1(models.Model):
    primary_key = models.AutoField(primary_key=True)
    property_one = models.CharField(max_length=15, unique=True)


class Table2(models.Model):
    foreign_primary_key = models.OneToOneField('Table1', on_delete=models.CASCADE, to_field='primary_key', related_name='foreign_primary_key', primary_key=True)
    foreign_property = models.ForeignKey('Table1', on_delete=models.SET_NULL, null=True, to_field='property_one', related_name='foreign_property')
    property_two = models.IntegerField()


class PropertyTable(models.Model):
    primary_key = models.IntegerField(primary_key=True)
    times = models.IntegerField()
