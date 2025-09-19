from rest_framework.serializers import ModelSerializer

from core.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'name', 'is_active', 'is_staff'
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        """Create user with encrypted password."""
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """Update user with encrypted password."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user