from rest_framework import serializers

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=256)
    new_password = serializers.CharField(max_length=256)
    confirm_password = serializers.CharField(max_length=256)
