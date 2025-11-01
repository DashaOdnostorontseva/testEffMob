from rest_framework.decorators import api_view, authentication_classes, permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from ..models import Users, UserRoles, Roles
from ..serializers import UserSerializer
from ..main import get_access, get_user_role, ROLE_ADMIN_ID

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def external_get_users(request):
    user = request.user
    user_id = user.id
    
    allowed, response = get_access(request, user_id)
    if not allowed:
        return response
    
    user_role = get_user_role(user)
    
    if ((user_role == None) or 
        (user_role.role_id < ROLE_ADMIN_ID)):
        return Response({'status': 'error', 'message': 'Forbidden. Not enough rights for this activity'}, status=403)

    users = Users.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response({'status': 'success', 'data': serializer.data})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def external_update_role(request):
    user = request.user
    user_id = user.id

    allowed, response = get_access(request, user_id)
    if not allowed:
        return response
    
    user_role = get_user_role(user)

    if ((user_role == None) or 
        (user_role.role_id < ROLE_ADMIN_ID)):
        return Response({'status': 'error', 'message': 'Forbidden. Not enough rights for this activity'}, status=403)

    data = request.data
    target_user_id = data.get('user_id')
    new_role_type = data.get('role_type')

    if ((not (target_user_id) or type(target_user_id) != str) or 
        (not (new_role_type)) or type(new_role_type) != str):
        return Response({'status': 'error', 'message': 'Invalid data'}, status=400)

    try:
        new_role = Roles.objects.get(role_type=new_role_type)
    except Roles.DoesNotExist:
        return Response({'status': 'error', 'message': 'Invalid role'}, status=400)

    target_user = Users.objects.get(id=target_user_id)
    UserRoles.objects.create(user=target_user, role=new_role, created_by=user)
    target_user.update_last_modified()

    return Response({'status': 'success', 'message': f'User {target_user_id} role updated to {new_role_type}'})
