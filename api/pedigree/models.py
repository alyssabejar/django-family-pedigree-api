from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE

from rest_framework.reverse import reverse


class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    vital_status = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='members', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('members-detail', kwargs={'pk': self.pk})

