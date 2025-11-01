
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Users, UserRoles, Roles
from ..serializers import UserSerializer
from ..main import get_access, get_user_role, ROLE_ADMIN_ID


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_data(request, id):  
    allowed, response = get_access(request, id)
    if not allowed:
        return response
    
    user = request.user
    user_role = get_user_role(user)

    if ((user_role == None) or 
        (user_role.role_id < ROLE_ADMIN_ID)):
        return Response({'status': 'error', 'message': 'Forbidden. Not enough rights for this activity'}, status=403)

    users = Users.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response({'status': 'success', 'data': serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user_role(request, id):
    allowed, response = get_access(request, id)
    if not allowed:
        return response
    
    user = request.user
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

    return Response({'status': 'success', 'message': f'Role for user {target_user_id} updated to {new_role_type}'})
