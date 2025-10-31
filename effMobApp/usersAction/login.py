from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from ..main import get_access, get_user_by_id
import json

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                request.user = user

                return JsonResponse({
                    'status': 'success',
                    'message': 'Login successful',
                    'user_id': user.id,
                    'redirect_url': f'/profile/{user.id}/' 
                })
            else:
                return JsonResponse({'status': 'error', 'message': 'Authentification is failed. Email or password is incorrect'}, status=401)
        else:
            return JsonResponse({'status': 'error', 'message': 'Authentification is failed. Email or password is incorrect'}, status=401)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
@login_required
def profile_page(request, id): 
    allowed, response = get_access(request, id)
    if not allowed:
        return response

    user = get_user_by_id(id)
    if user:
        return render(request, 'effMobApp/profile.html', {
            'user': user,
        })
    else:
        return render(request, 'effMobApp/error.html')