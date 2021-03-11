from django.db import models
from django.contrib.auth.models import User


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True, default='images.jpg')

    def __str__(self):
        return str(self.user)


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=256)
    last = models.FileField(upload_to='last_report')
    last_year = models.FileField(upload_to='last_y_report')
    tag = models.CharField(max_length=128)

    def __str__(self):
        return self.type


class Outcome(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    time = models.DateTimeField()
    filename = models.CharField(max_length=256)
    file = models.FileField(upload_to='user_directory_path')

    def __str__(self):
        return self.filename


class Variable(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    month = models.PositiveSmallIntegerField(default=1)
    year = models.PositiveSmallIntegerField(default=2021)
    open_last_report = models.BooleanField()

    def save(self, *args, **kargs):
        if self.month not in range(1, 13):
            self.month = 1

        super(Variable, self).save(*args, **kargs)

    def __str__(self):
        return str(self.user)


