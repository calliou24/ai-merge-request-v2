
from rest_framework import serializers

from automator.models import PAT 

class PATSerializer(serializers.ModelSerializer):
    token= serializers.CharField(write_only=True)

    class Meta:
        model=PAT
        fields=['id', 'name', 'token', 'is_active']
        read_only_fields=['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        """
            Here goes the encryption step
        """

        encrypted_pat = validated_data.pop('token')
        validated_data['encrypted_pat'] = encrypted_pat

        pat = PAT.objects.create(
            **validated_data
        )

        return pat      

    def update(self, instance, validated_data):
        if "token" not in validated_data: 
            return super().update(instance, **validated_data)

        """
            Here goes the encryption step
        """
        encrypted_pat = validated_data.pop("token")
        validated_data["encrypted_pat"] = encrypted_pat
        
        return super().update(instance, validated_data) 
