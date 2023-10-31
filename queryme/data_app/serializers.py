from rest_framework import serializers

class FileQuerySerializer(serializers.Serializer):
    file = serializers.FileField()
    type = serializers.CharField(allow_blank=True, required=False)