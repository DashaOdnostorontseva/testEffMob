from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..main import get_access, get_user_by_id
from django.utils import timezone

@csrf_exempt
@login_required
def deleteProfile(request, id):
    if request.method == 'POST':
        allowed, response = get_access(request, id)
        if not allowed:
            return response
        user = get_user_by_id(id)
        user.is_active = False
        user.deleted_at = timezone.now()
        user.save()
        return JsonResponse({'status': 'success', 'redirect_url': '/'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
