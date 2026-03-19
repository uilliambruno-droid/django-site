from django.db import models


class Contact(models.Model):
    subject = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    message = models.TextField()
    cc_myself = models.BooleanField(default=False)

    def __str__(self):
        return self.subject
