from django.shortcuts import render
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from uploadFile.models import File, FileInfo
from uploadFile.serializers import FileSerializer, FileInfoSerializer

from uploadFile.tasks import file_info, byte_analysis,__one_gram_byte_summary,__entropy,sigcheck,__signers,check_pack,dll_import_analysis,pefile_infos

from django.conf import settings
import os
import time


# https://kite.com/python/docs/django.db.models.Model.save


# Save to DB
# https://github.com/pandas-dev/pandas/issues/14553
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html

# Create your views here.
class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

      file_serializer = FileSerializer(data=request.data)

      if file_serializer.is_valid():
          # 將檔案存下來
          file_serializer.save()
          file_id = file_serializer.data['id']
          file_path = os.path.join(settings.MEDIA_ROOT,file_serializer.data['file'])

          # 打開檔案蒐集特徵
          file_info.delay(file_path, file_id)
          time.sleep(5)
          response_serializer = FileInfoSerializer(FileInfo.objects.filter(upload_id=file_id), many=True)

          
          # 運算打分數，更新DB   update()


          # 運算完刪除DB檔案紀錄、刪除media裡面的檔案    delete()      拒絕存取 可能再另外刪
          # File.objects.get(id=file_id).delete()
          
          # 回傳特徵、分數
          return Response(response_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)