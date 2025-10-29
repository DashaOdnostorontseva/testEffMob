from django.db import models

class Roles(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    role_type = models.CharField(max_length=255)

class Users(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def soft_delete(self):
        self.is_active = False
        self.deleted_at = models.DateTimeField(auto_now_add=True)
        self.save()

class UserRoles(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)

class Passwords(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    salt = models.CharField(max_length=255)
    hashed_password = models.CharField(max_length=255)

class EntryMonitoring(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()

