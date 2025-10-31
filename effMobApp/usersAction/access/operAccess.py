from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from ...main import get_access, get_user_by_id, get_user_role, ROLE_OPERATOR_ID

@csrf_exempt
@login_required
def operatorPage(request, id):
    allowed, response = get_access(request, id)
    if not allowed:
        return response

    user = get_user_by_id(id)  
    user_role = get_user_role(user)
    if user_role.role_id >= ROLE_OPERATOR_ID:
        if request.method == 'POST':
                return JsonResponse({'status': 'success', 'redirect_url': f'/profile/{id}/operatorPage/'})
        elif request.method == 'GET':
            return render(request, 'effMobApp/operatorPage.html')
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    else:
        return JsonResponse({'status': 'error', 'message': 'User doesn’t have enough rights for this view'}, status=403)