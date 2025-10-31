from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from effMobApp.models import Users, Passwords

class CustomAuthenticationBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        print("authenticate")
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            return None
        
        password_entry = Passwords.objects.filter(user=user).order_by('-date').first()

        if not password_entry:
            return None
        
        salt = password_entry.salt

        if check_password(password + salt, password_entry.hashed_password):
            print("access allowed")
            return user
        
        return None
    
    def get_user(self, user_id):
        try:
            return Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return None
