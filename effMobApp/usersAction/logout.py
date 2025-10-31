from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@csrf_exempt
@login_required
def logout_view(request, id):
    logout(request)
    return JsonResponse({'status': 'success', 'redirect_url': '/'})