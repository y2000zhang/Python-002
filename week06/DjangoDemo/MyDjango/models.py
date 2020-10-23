# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class RegisterInfo(models.Model):
    user_code = models.CharField(max_length=32)
    status = models.CharField(max_length=1, blank=True, null=True)
    message = models.CharField(max_length=32, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'register_info'


class Shortcuts(models.Model):
    n_star = models.IntegerField(blank=True, null=True)
    short = models.CharField(max_length=400, blank=True, null=True)
    sentiment = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shortcuts'


class User(models.Model):
    user_code = models.CharField(primary_key=True, max_length=32)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=32, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
