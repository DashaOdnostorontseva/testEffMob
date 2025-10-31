from django.http import JsonResponse
from .models import Users, UserRoles
from django.shortcuts import get_object_or_404
from django.shortcuts import render

ROLE_EMPTY = None
ROLE_USER_ID = 1
ROLE_OPERATOR_ID = 2
ROLE_ADMIN_ID = 3

# def get_access(request, id):
#     if not request.user.is_authenticated:
#         return False, JsonResponse({'status': 'error', 'message': 'Unauthorized access'}, status=401)
    
#     if request.user.id != id:
#         return False, JsonResponse({'status': 'error', 'message': 'Unauthorized access'}, status=401)
    
#     return True, None

def get_access(request, id):
    if not request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return False, JsonResponse({'status': 'error', 'message': 'Unauthorized access'}, status=401)
        return False, render(request, 'effMobApp/noRights.html', {'message': 'Неавторизованный доступ'}, status=401)

    if request.user.id != id:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return False, JsonResponse({'status': 'error', 'message': 'Forbidden: wrong user ID'}, status=403)
        return False, render(request, 'effMobApp/noRights.html', {'message': 'Доступ запрещён'}, status=403)

    return True, None

def get_user_role(user):
    user_role = UserRoles.objects.filter(user=user).order_by('-date').first()
    if not user_role:
        return ROLE_EMPTY
    return user_role

def get_user_by_id(id):
    return get_object_or_404(Users, id=id)

def user_is_exist(email):
    user = Users.objects.filter(email=email).first()
    if user:
        return True, user
    return False, None