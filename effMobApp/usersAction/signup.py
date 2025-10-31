from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from effMobApp.models import Users, Passwords, Roles, UserRoles
from .passwords import hash_password
from ..main import user_is_exist
import json

def create_user(first_name, last_name, patronymic, email, password):
    hashed_password, salt = hash_password(password)

    user = Users.objects.create_user(
        first_name=first_name,
        last_name=last_name,
        patronymic=patronymic,
        email=email,
        password=hashed_password
    )

    password_entry = Passwords.objects.create(
        user=user,
        salt=salt,
        hashed_password=hashed_password
    )
    
    password_entry.save()

    user_role_id, created = Roles.objects.get_or_create(role_type='user')

    user_role_entry = UserRoles.objects.create(
        user=user,
        role=user_role_id
    )
    user_role_entry.save()

    return user

@csrf_exempt
def signup(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
    data = json.loads(request.body)

    password = data.get('password')
    password_repeat = data.get('password_repeat')

    if password != password_repeat:
        return JsonResponse({'status': 'error', 'message': 'Passwords do not match'})
    
    email = data.get("email")
    
    is_exist, exist_user = user_is_exist(email)

    if ((is_exist) and 
        (user.is_active)):
            return JsonResponse({'status': 'error', 'message': 'User with this email already exists. Please use the login form.'}, status=400)
    
    if ((is_exist) and 
        (not user.is_active)):          
            auth_user = authenticate(request, email=email, password=password)

            if auth_user:
                user.is_active = True
                user.save()
                login(request, auth_user)
                return JsonResponse({'status': 'success', 'message' : 'Account successfully restored', 'redirect_url': f'/profile/{user.id}/'})
            return JsonResponse({'status': 'error', 'message': 'Incorrect password for existing (inactive) account'})
    
    try:
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        patronymic = data.get("patronymic")

        user = create_user(first_name = first_name,
                    last_name = last_name,
                    patronymic = patronymic,
                    email = email,
                    password = password)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
    auth_user = authenticate(request, email=email, password=password)

    if auth_user:
        login(request, auth_user)
        return JsonResponse({'status': 'success', 'message' : 'Registration successful', 'redirect_url': f'/profile/{user.id}/'})

    return JsonResponse({'status': 'error', 'message': 'Authentication failed after signup'}, status=401)
            
    
