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
    
    file_path = models.TextField(blank=True)
    file_hash_sha1 = models.CharField(max_length=40)
    file_size = models.IntegerField(blank=True, null=True)
    file_magic = models.CharField(max_length=100,blank=True, null=True)
    file_state = models.IntegerField(blank=True, null=True)
    peutils_packed = models.CharField(max_length=200, blank=True)
    entropy = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)

    create_time = models.DateTimeField(blank=True)
    modified_time = models.DateTimeField(blank=True)
    accessed_time = models.DateTimeField(blank=True)

    company = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=60, blank=True)
    product = models.CharField(max_length=50, blank=True)
    prod_version = models.CharField(max_length=40, blank=True)
    file_version = models.CharField(max_length=40, blank=True)
    machine_type = models.CharField(max_length=20, blank=True)

    signature_verification = models.CharField(max_length=100)
    link_date = models.DateTimeField(blank=True)
    signing_date = models.DateTimeField(blank=True)

    signer = models.TextField(blank=True)
    counter_signer = models.TextField(blank=True)

    pe_machine = models.IntegerField(blank=True, null=True)
    pe_sectionNum = models.IntegerField(blank=True, null=True)
    pe_timeDateStamp = models.DateTimeField(blank=True)
    pe_characteristics = models.IntegerField(blank=True, null=True)
    pe_entryPoint = models.IntegerField(blank=True, null=True)

    pe_sections = models.TextField(blank=True)

    pe_imports = models.TextField(blank=True)

    pe_exports = models.TextField(blank=True)
    
    #pefile_txt = models.IntegerField(blank=True, null=True)
    printablestr_txt = models.IntegerField(blank=True, null=True)   # 字串要不要先經過處理再存
    byte_distribution = models.TextField(blank=True)

    score = models.IntegerField(default=0)

    scanningRecord_id = models.ForeignKey(ScanningRecord, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.file_path)

    def state(self):
        dictOfWords = {32:'ARCHIVE', 2048:'COMPRESSED', 64:'DEVICE', 16:'DIRECTORY', 16384:'ENCRYPTED', 2:'HIDDEN', 32768:'INTEGRITY STREAM', 128:'NORMAL', 8192:'NOT CONTENT INDEXED', 131072:'NO SCRUB DATA', 4096:'OFFLINE', 1:'READONLY', 4194304:'RECALL_ON_DATA_ACCESS', 262144:'RECALL_ON_OPEN', 1024:'REPARSE POINT', 512:'SPARSE FILE', 4:'SYSTEM', 256:'TEMPORARY', 65536:'VIRTUAL'}
        for (key, value) in dictOfWords.items():
            if (key == self.file_state):
                return value 
        

    def signer_dic(self):
        return eval(self.signer)

    def counter_signer_dic(self):
        return eval(self.counter_signer)

    def machine(self):
        dictOfWords = {0:'UNKNOWN', 467:'AM33', 34404:'AMD64', 448:'ARM', 43620:'ARM64', 452:'ARMNT', 3772:'EBC', 332:'I386', 512:'IA64', 36929:'M32R', 614:'MIPS16', 870:'MIPSFPU', 1126:'MIPSFPU16', 496:'POWERPC', 497:'POWERPCFP', 358:'R4000', 20530:'RISCV32', 20580:'RISCV64', 20776:'RISCV128', 418:'SH3', 419:'SH3DSP', 422:'SH4', 424:'SH5', 450:'THUMB', 361:'WCEMIPSV2'}
        for (key, value) in dictOfWords.items():
            if (key == self.pe_machine):
                return value 
        

    def characteristics(self):
        dictOfWords = {1:'RELOCS STRIPPED', 2:'EXECUTABLE IMAGE', 4:'LINE NUMS STRIPPED', 8:'LOCAL SYMS STRIPPED', 16:'AGGRESSIVE WS TRIM', 32:'LARGE ADDRESS AWARE', 128:'BYTES REVERSED LO', 256:'32BIT MACHINE', 512:'DEBUG STRIPPED', 1024:'REMOVABLE RUN FROM SWAP', 2048:'NET RUN FROM SWAP', 4096:'SYSTEM', 8192:'DLL', 16384:'UP SYSTEM ONLY', 32768:'BYTES REVERSED HI'}
        for (key, value) in dictOfWords.items():
            if (key == self.pe_characteristics):
                return value 
        

    def sections(self):
        return eval(self.pe_sections)

    def imports(self):
        return eval(self.pe_imports)

    def exports(self):
        return eval(self.pe_exports)

    def packed(self):
        s = self.peutils_packed.replace("['", '"').replace("']", '"')
        return eval(s)

class Documents(models.Model):
    file = models.FileField(upload_to='documents')
    uploaded_time = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return str(self.file)

    class Meta:
        verbose_name_plural = "Documents"

class RSAKeys(models.Model):
    key = models.TextField()
