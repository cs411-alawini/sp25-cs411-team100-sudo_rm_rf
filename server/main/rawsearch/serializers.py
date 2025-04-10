from rest_framework import serializers
from ..models import Rxnconso

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rxnconso
        fields = "__all__"
