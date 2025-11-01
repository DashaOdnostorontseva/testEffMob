from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from .passwords import update_password

import json

from ..main import get_access, get_user_by_id

@csrf_exempt
@login_required
def editProfile(request, id):
    allowed, response = get_access(request, id)
    if not allowed:
        return response

    user = get_user_by_id(id)
    
    if request.method == 'GET':
        return render(request, 'effMobApp/editProfile.html', {'user': user})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
@login_required
def updateProfileData(request, id):
    if request.method == 'POST':

        allowed, response = get_access(request, id)
        if not allowed:
            return response
        
        user = get_user_by_id(id)
    
        data = json.loads(request.body)

        user.update_profile_info(email = data.get('email'),
                                 first_name = data.get('first_name'),
                                 last_name = data.get('last_name'),
                                 patronymic = data.get('patronymic'))

        new_password = data.get('password')
        new_password_repeat = data.get('password_repeat')

        if new_password:
            if (new_password == new_password_repeat):
                update_password(user, new_password)
                user.save()
                return JsonResponse({'status': 'success', 'redirect_url': '/'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Passwords do not match'}, status=400)
        else:
            user.save()
            return JsonResponse({'status': 'success', 'redirect_url': f'/profile/{id}/'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})