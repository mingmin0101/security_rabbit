from django.db import models

# Create your models here.
class computer_list(models.Model):
    """listing all the computers"""
    computer_name = models.CharField(max_length=20)
    computer_ip = models.GenericIPAddressField()
    mac_addr = models.CharField(max_length=50)

    def __str__(self):
        return self.computer_name

class scanning_history(models.Model):
    """each computer has a scanning_history table"""
    scan_sequence = models.IntegerField() # An IntegerField that automatically increments according to available IDs.
    scanning_start_time = models.DateTimeField()
    scanning_end_time = models.DateTimeField()

    computer = models.ForeignKey(computer_list, on_delete=models.CASCADE)#資料表的關聯性  
    def __str__(self):
        return str(self.scan_sequence)

class scanning_details(models.Model):
    """showing the details of each scanning record"""
    scanning_history_id = models.ForeignKey(scanning_history, on_delete=models.CASCADE)
    options = models.CharField(max_length=50) #還要再修正

    class Meta:
        verbose_name_plural = "Scanning_details"

class file_info(models.Model):
    """every scanning_details contains scanned files info"""
    scanning_details_id = models.ForeignKey(scanning_details, on_delete=models.CASCADE)
    file_info_url = models.URLField() # A CharField for a URL, validated by URLValidator. The default form widget for this field is a TextInput. Like all CharField subclasses, URLField takes the optional max_length argument. If you don’t specify max_length, a default of 200 is used.
        