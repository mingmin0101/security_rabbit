from django.db import models
from users.models import User

class Computer(models.Model):
    """
    listing all the computers.
    
    deviceUuid  ==>  wmic csproduct get UUID
    deviceName  ==>  platform.uname()   node
    userName    ==>  os.getlogin()
    ipAddr      ==>  wmi Win32_NetworkAdapterConfiguration
    macAddr     ==>  wmi Win32_NetworkAdapterConfiguration
    os          ==>  platform.uname()   system + release + version
    processor   ==>  platform.uname()   processor
    cpu         ==>  platform.uname()   machine
    memoryCapacity    ==>  wmi Win32_PhysicalMemory

    registry_StartupCommand    ==>  wmi Win32_StartupCommand

    latest_scan_score    ==>  user網頁直接撈最新的ScanningRecord分數
    """
    administrator = models.ForeignKey(User, on_delete=models.CASCADE)
    deviceUuid = models.CharField(max_length=50)
    deviceName = models.CharField(max_length=20)   
    userName = models.CharField(max_length=15)
    
    ipAddr = models.CharField(max_length=250, default='ip')
    macAddr = models.CharField(max_length=250, default='mac')
    
    os = models.CharField(max_length=35)   
    processor = models.CharField(max_length=80)   
    cpu = models.CharField(max_length=10)   
    memoryCapacity = models.CharField(max_length=10)
    
    registry_StartupCommand = models.TextField(blank=True)
    latest_scan_score = models.IntegerField(default=0)

    def score(self):
        '''Returns the computer's score .'''
        if self.latest_scan_score > 7:
            return "Dangerous"
        elif self.latest_scan_score > 4:
            return "Warning"
        else:
            return "Safe"
    
    def mac(self):
        mac_li = eval(self.macAddr)
        mac_list = []
        for item in mac_li:
            mac_list.append(eval(item))
        return mac_li

    def ip(self):
        return eval(self.ipAddr)

    def registry(self):
        return eval(self.registry_StartupCommand)
    
    def __str__(self):
        return self.deviceName


class ScanningRecord(models.Model):
    """each computer has a scanning_history table"""
    scan_id = models.AutoField(primary_key=True) 
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    normal_option = models.BooleanField()
    advance_option = models.BooleanField()
    customized_option = models.BooleanField()
    score = models.IntegerField(default=0)

    computer = models.ForeignKey(Computer, on_delete=models.CASCADE)#資料表的關聯性  
    

    def __str__(self):
        return str(self.scan_id)

class FileInfo(models.Model):
    """every scanning_details contains scanned files info"""
    
    file_path = models.TextField()
    file_hash = models.CharField(max_length=100)
    peutils_packed = models.CharField(max_length=200, blank=True)
    signer = models.CharField(max_length=300, blank=True)
    create_time = models.DateTimeField(blank=True)
    modified_time = models.DateTimeField(blank=True)
    accessed_time = models.DateTimeField(blank=True)
    file_state = models.IntegerField(blank=True, null=True)
    pefile_txt = models.IntegerField(blank=True, null=True)
    printablestr_txt = models.IntegerField(blank=True, null=True)   # 字串要不要先經過處理再存
    entropy = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    # byte_image =              # 讀出來的的byte要怎麼存 還是要轉存成圖片
    byte_distribution = models.TextField(blank=True)

    score = models.IntegerField(default=0)

    scanningRecord_id = models.ForeignKey(ScanningRecord, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.file_path)

class Documents(models.Model):
    file = models.FileField(upload_to='documents')
    uploaded_time = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return str(self.file)

    class Meta:
        verbose_name_plural = "Documents"

class RSAKeys(models.Model):
    key = models.TextField()
