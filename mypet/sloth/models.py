import os

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone




def user_directory_path(instance, filename):
    now = timezone.now().strftime("%m%d%H%M%S")
    user_path = os.path.join(
        'user_%d' % instance.user.id, '%s' % instance.item, '%s_%s' % (now, filename))
    return user_path


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=user_directory_path, blank=True, default='images.jpg')

    def __str__(self):
        return str(self.user)


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=256, default='')
    last = models.FileField(upload_to=user_directory_path, default='')
    last_year = models.FileField(upload_to=user_directory_path, default='')
    tag = models.CharField(max_length=128, default='')
    month = models.PositiveSmallIntegerField(default=0)
    year = models.PositiveSmallIntegerField(default=1900)
    open_last_report = models.BooleanField(default=True)

    class Meta:
        unique_together = ['user', 'item']

    def __str__(self):
        return self.item


class PreparationFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Report, on_delete=models.CASCADE)
    ready_file = models.FileField(upload_to=user_directory_path, default='')
    file_tag = models.CharField(max_length=64, default='')

    def __str__(self):
        return self.file_tag


class Outcome(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Report, on_delete=models.CASCADE)
    time = models.DateTimeField(blank=True)
    file = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return str(self.file.name)
