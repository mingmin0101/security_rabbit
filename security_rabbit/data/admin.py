from django.contrib import admin
from data.models import Computer, ScanningRecord, FileInfo, Documents

admin.site.site_header = "Security Rabbit Admin"
admin.site.site_title = "Security Rabbit"
admin.site.index_title = "Welcome to Security Rabbit"

# Register your models here.
class ComputerAdmin(admin.ModelAdmin):
    list_display = ['administrator', 'deviceUuid', 'deviceName', 'userName', 'ipAddr','macAddr', 'os', 'processor', 'cpu', 'memoryCapacity', 'registry_StartupCommand']
    list_filter = ['deviceUuid', 'deviceName'] 
    # search_fields = ['computerIp']

class ScanAdmin(admin.ModelAdmin):
    list_display = ['scan_id', 'computer', 'start_time', 'end_time', 'normal_option', 'advance_option', 'customized_option', 'score']
    list_filter = ['computer', 'start_time']
    ordering = ['scan_id']

class FileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FileInfo._meta.get_fields()]
    # list_display = ['scanningRecord_id', 'file_path', 'file_hash', 'peutils_packed', 'signer', 'create_time', 'modified_time', 'accessed_time', 'file_state', 'pefile_txt', 'printablestr_txt', 'entropy', 'byte_distribution', 'score']
    list_filter = ['scanningRecord_id'] 
    # search_fields = ['file_info_url']

class DocumentAdmin(admin.ModelAdmin):
    list_display = ['file', 'uploaded_time']
    
        

admin.site.register(Computer, ComputerAdmin) 
admin.site.register(ScanningRecord, ScanAdmin)  
admin.site.register(FileInfo, FileAdmin)
admin.site.register(Documents, DocumentAdmin)