from django.db import models


# Create your models here.
class Server(models.Model):
    name = models.CharField(max_length=30, unique=True)
    pkey = models.FilePathField(blank=True)
    port = models.IntegerField(default=22)
    user = models.CharField(max_length=30, default="root")
    tag = models.ManyToManyField("Tag")


class Host(models.Model):
    host_name = models.CharField(max_length=30, blank=True)
    host = models.CharField(max_length=256)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)


class ChallengePort(models.Model):
    server_name = models.CharField(max_length=30, blank=True)
    port = models.IntegerField()
    server = models.ForeignKey(Server, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)


class Config(models.Model):
    key = models.CharField(max_length=30, unique=True)
    value = models.CharField(max_length=30)
