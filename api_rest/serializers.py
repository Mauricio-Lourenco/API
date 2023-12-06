from rest_framework import serializers
from .models import Voos
from .models import Resultado_ia

class VoosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voos
        fields = '__all__'
