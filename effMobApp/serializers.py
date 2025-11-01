from rest_framework import serializers
from .models import Users, UserRoles

class UserSerializer(serializers.ModelSerializer):
    role_type = serializers.SerializerMethodField()
    role_date = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ['id', 'first_name', 'last_name', 'patronymic', 'email', 'is_active', 'role_type', 'role_date']

    def get_role_type(self, obj):
        latest = (
            UserRoles.objects
            .filter(user=obj)
            .order_by('-date')
            .select_related('role')
            .first()
        )
        return latest.role.role_type if latest else None
    
    def get_role_date(self, obj):
        latest = (
            UserRoles.objects
            .filter(user=obj)
            .order_by('-date')
            .first()
        )
        return latest.date if latest else None