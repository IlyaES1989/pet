from django.db import models
from django.contrib.auth.models import User

import os

def user_directory_path(instance, filename):
    return os.path.join(
      "user_%d" % instance.report.user.id, '%s' % filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True, default='images.jpg')

    def __str__(self):
        return str(self.user)


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=256, default='')
    last = models.FileField(upload_to='last_report', default='')
    last_year = models.FileField(upload_to='last_y_report', default='')
    tag = models.CharField(max_length=128, default='')
    month = models.PositiveSmallIntegerField(default=0)
    year = models.PositiveSmallIntegerField(default=1900)
    open_last_report = models.BooleanField(default=True)


    def __str__(self):
        return self.item


class PreparationFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Report, on_delete=models.CASCADE)
    primarily_file = models.FileField(upload_to='prepare', default='')
    ready_file = models.FileField(upload_to='prepare', default='')
    tage_file = models.CharField(max_length=64, default='')

    def __str__(self):
        return self.tage_file


class Outcome(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    time = models.DateTimeField()
    file = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return str(self.file.name)


