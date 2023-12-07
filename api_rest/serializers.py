from rest_framework import serializers
from .models import Voos
from .models import Resultado_ia


class VoosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voos
        fields = '__all__'


class Resultado_iaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultado_ia
        fields = ['resultado', 'voo']
