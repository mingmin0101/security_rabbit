from django.contrib import admin
from uploadFile.models import File

class FileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in File._meta.get_fields()]
    # list_display = ['scanningRecord_id', 'file_path', 'file_hash', 'peutils_packed', 'signer', 'create_time', 'modified_time', 'accessed_time', 'file_state', 'pefile_txt', 'printablestr_txt', 'entropy', 'byte_distribution', 'score']
    
admin.site.register(File, FileAdmin) 
