from django.contrib import admin
from panel.models import computerList, scanningHistory, scanningDetails, fileInfo

# 客製化 AdminSite
# https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#customizing-adminsite
# https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#django.contrib.admin.AdminSite
# from django.contrib.admin import AdminSite  

# class SecurityRabbitAdminSite(AdminSite):
#     site_header = 'Security Rabbit Panel'
#     site_title = "Security Rabbit"
#     index_title = "Welcome to Security Rabbit"

# admin_site = SecurityRabbitAdminSite(name='myadmin')   # name : used to identify the instance, especially when reversing admin URLs
# admin_site.register(MyModel)




# 將內建 user, group 顯示移除
# from django.contrib.auth.models import User, Group
# admin.site.unregister(User)
# admin.site.unregister(Group)

# 變更顯示
admin.site.site_header = "Security Rabbit Admin"
admin.site.site_title = "Security Rabbit"
admin.site.index_title = "Welcome to Security Rabbit"

# 註冊模型 Register your models here.
class ComputerAdmin(admin.ModelAdmin):
    list_display = ['computerName', 'computerIp', 'macAddr','os','processorName','memoryCapacity']
    list_filter = ['computerIp'] 
    search_fields = ['computerIp']
    # change_list_template = 'admin/security_rabbit.html'   # 可另外編輯頁面(不過admin介面應該不用)
    # fields = ('computer_name', 'computer_ip')  # 設定編輯區可編輯的欄位、欄位順序

admin.site.register(computerList, ComputerAdmin) 

class ScanAdmin(admin.ModelAdmin):
    list_display = ['scan_sequence', 'computer', 'scanning_start_time', 'scanning_end_time']
    list_filter = ['computer', 'scanning_start_time']
    ordering = ['scan_sequence']

admin.site.register(scanningHistory,ScanAdmin)  

admin.site.register(scanningDetails)         
admin.site.register(fileInfo) 


     

