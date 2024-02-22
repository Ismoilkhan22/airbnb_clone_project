from django.db import models


class Category(models.Model):
    """
              Category For model
    """
    title = models.CharField(max_length=200)

    description = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}->{self.status}'
