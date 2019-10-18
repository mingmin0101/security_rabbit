from rest_framework import serializers
from uploadFile.models import File, FileInfo


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = "__all__"


class FileInfoSerializer(serializers.ModelSerializer):
    signer_dic = serializers.ListField(child=serializers.CharField())
    counter_signer_dic = serializers.ListField(child=serializers.CharField())
    sections = serializers.ListField(child=serializers.CharField())
    imports = serializers.ListField(child=serializers.CharField())
    exports = serializers.ListField(child=serializers.CharField())
    # state = serializers.CharField()
    machine = serializers.CharField()
    characteristics = serializers.CharField()
    packed = serializers.ListField(child=serializers.CharField())
    
    class Meta:
        model = FileInfo
        fields = '__all__'