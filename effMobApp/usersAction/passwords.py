from django.contrib.auth.hashers import make_password
import os
from effMobApp.models import Passwords

def hash_password(password):
    salt = os.urandom(16).hex()
    hashed_password = make_password(password + salt)

    return hashed_password, salt

def update_password(user, password):
    hashed_password, salt = hash_password(password)

    user.password = hashed_password
    user.save()

    password_entry = Passwords.objects.create(
        user=user,
        salt=salt,
        hashed_password=hashed_password
    )
    password_entry.save()
