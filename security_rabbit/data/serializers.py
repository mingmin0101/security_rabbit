from rest_framework import serializers
from data.models import Computer, ScanningRecord, FileInfo

# The ModelSerializer class provides a shortcut that lets you automatically create a Serializer class with fields that correspond to the Model fields.
class ComputerSerializer(serializers.ModelSerializer):
    last_scan_status = serializers.CharField(source='score')

    class Meta:
        model = Computer
        fields = '__all__'
        #fields = ['id', 'deviceUuid', 'deviceName', 'userName', 'ipAddr', 'macAddr', 'os', 'processor', 'cpu', 'memoryCapacity', 'last_scan_status']


class ScanningRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanningRecord
        fields = '__all__'


class FileNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileInfo
        fields = ['file_path']


# 需要加上讀取txt的字串
class FileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileInfo
        fields = '__all__'