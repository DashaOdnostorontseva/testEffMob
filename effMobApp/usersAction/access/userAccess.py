from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from ...main import get_access

@csrf_exempt
@login_required
def userPage(request, id):
    
    allowed, response = get_access(request, id)
    if not allowed:
        return response
    
    if request.method == 'POST':
        return JsonResponse({'status': 'success', 'redirect_url': f'/profile/{id}/userPage/'})
    elif request.method == 'GET':
            return render(request, 'effMobApp/userPage.html')
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)