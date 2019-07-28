from django.db import models

# Create your models here.
class computerList(models.Model):
    """listing all the computers"""
    computerName = models.CharField(max_length=20)
    computerIp = models.GenericIPAddressField()
    macAddr = models.CharField(max_length=50)
    os = models.CharField(max_length=30,default='os information')
    processorName = models.CharField(max_length=20,default='Processor Name')
    memoryCapacity = models.CharField(max_length=30,default='0MB')
    def __str__(self):
        return self.computerName

class scanningHistory(models.Model):
    """each computer has a scanning_history table"""
    scan_sequence = models.IntegerField() # An IntegerField that automatically increments according to available IDs.
    scanning_start_time = models.DateTimeField()
    scanning_end_time = models.DateTimeField()

    computer = models.ForeignKey(computerList, on_delete=models.CASCADE)#資料表的關聯性  
    def __str__(self):
        return str(self.scan_sequence)

class scanningDetails(models.Model):
    """showing the details of each scanning record"""
    scanning_history_id = models.ForeignKey(scanningHistory, on_delete=models.CASCADE)
    fileName = models.CharField(max_length=50) #還要再修正

    class Meta:
        verbose_name_plural = "Scanning_details"

class fileInfo(models.Model):
    """every scanning_details contains scanned files info"""
    scanning_details_id = models.ForeignKey(scanningDetails, on_delete=models.CASCADE)
    file_info_url = models.URLField() # A CharField for a URL, validated by URLValidator. The default form widget for this field is a TextInput. Like all CharField subclasses, URLField takes the optional max_length argument. If you don’t specify max_length, a default of 200 is used.
        
class Documents(models.Model):
    file = models.FileField(upload_to='documents')

class RSAKeys(models.Model):
    key = models.TextField()