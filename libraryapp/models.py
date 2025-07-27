from django.db import models

class Users(models.Model):
    User_id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=100)
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=100)
    Membership_status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'Users'
