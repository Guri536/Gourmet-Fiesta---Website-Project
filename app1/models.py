from django.db import models
from django.conf import settings
# Create your models here.
class ids(models.Model):
    user_id = models.IntegerField(unique=True, default=0)
    user_username = models.CharField(max_length=30)
    user_type = models.CharField(max_length=1, default='n')
    def set_type(self, val):
        self.user_type = val
        return self
    def get_data(self):
        return {"name":str(self.user_username), "id":str(self.user_id), "type":str(self.user_type)}
    def __str__(self):
        return self.user_username
    