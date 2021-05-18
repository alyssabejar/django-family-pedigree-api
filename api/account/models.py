from django.db import models
from django.db.models import CASCADE
from PIL import Image
from rest_framework.reverse import reverse


class Account(models.Model):
    user = models.OneToOneField('auth.User', on_delete=CASCADE)
    dob = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        if self.user:
            user = self.user
            return '{}'.format(user.username)
        return self.pk

    def get_absolute_url(self):
        return reverse('user-account-detail', kwargs={'pk': self.pk})



