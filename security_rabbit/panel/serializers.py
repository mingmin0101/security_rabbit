from rest_framework import serializers
from panel.models import computerList,scanningHistory,scanningDetails,fileInfo

class computerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = computerList
        fields = '__all__'

# class scanningHistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = scanningHistory
#         fields = '__all__'
class scanningHistorySerializer(serializers.ModelSerializer):
    computerName = serializers.CharField(source='computer')
    class Meta:
        model = scanningHistory
        fields = ('id','scan_sequence','scanning_start_time','scanning_end_time','computerName')

class scanningDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = scanningDetails
        fields = '__all__'

class fileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = fileInfo
        fields = '__all__'