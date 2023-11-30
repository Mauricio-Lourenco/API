from rest_framework import serializers

from .models import Voos


class VoosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voos
        fields = '__all__'
