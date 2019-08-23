# coding: utf-8
# 2019-07-29 update

# def pefile_info()  
import peutils  
import pefile
import os

# def sigcheck()  
import subprocess
import re   

# file_info (time, hidden)
import datetime
import time
import win32api,win32con

# def openfile()
import binascii
import string
import math

# def host_info()
import wmi
import platform
import subprocess
import os

# pandas
import pandas as pd
import sys

# xml
import xml.etree.ElementTree as ET
import hashlib


def host_info(hostInfo_option, registry_option):
    """
    1. 取得掃描端點之硬體、軟體及作業系統資訊(wmi)
    2. 判斷檔案是否註冊於windows系統機碼，開機可自動啟動(wmi) 
    """
    w = wmi.WMI()
    
    if(hostInfo_option == 1):
        x = subprocess.check_output('wmic csproduct get UUID')
        deviceUuid = x.decode("utf-8").split('  \r\r\n')[1]
        
        t = tuple(platform.uname())
        deviceName = t[1]
        OS = t[0]+'-'+t[2]+'-'+t[3]
        processor = t[5]
        cpu = t[4]
        
        userName = os.getlogin()
        
        totalSize = 0
        for memModule in w.Win32_PhysicalMemory():
            totalSize += int(memModule.Capacity)
        
        memoryCapacity = totalSize/1048576
        
    if(registry_option == 1):
        for s in w.Win32_StartupCommand(): 
            print((s.Location, s.Caption, s.Command))

    


def sigcheck(filepath):
    """
    判斷檔案(參數filepath)是否具有可信認之數位簽章，使用sigcheck.exe 
    
    參考網址 https://docs.microsoft.com/en-us/sysinternals/downloads/sigcheck
    
    ##### 重要備註 ######
    signer是可以被修改的(打開檔案可修改byte)，要進一步判斷是否有被修改過?
    哪些signer是安全的?    
    CMD 有編碼問題!!! 先用except error帶過
    """
    try:
        
        # 用 sigcheck下指令
        output_str = os.popen('sigcheck -i -nobanner ' + filepath).read()
        str_list = re.findall(r"\w+.+", output_str)  # 將結果切成 list

        # 確認是否有簽章，若無會回傳 None，若有簽章再看看是誰簽的
        # if re.search('Verified:\tSigned', output_str) != None:   # 從整串指令回傳的str中找字串比對
            # str_list = re.findall(r"\w+.+", output_str)          # 將結果切成 list

        if 'Verified:\tSigned' in str_list:                        # 先切割字串再比對

            signer_arr = []
            signer_index = str_list.index('Signers:')

            # print(str_list)

            signer_index += 1
            signer_arr.append(str_list[signer_index])  # 第一個 signer

            # 列出所有 signer
            while re.search(r':$', str_list[signer_index+9]) == None:
                signer_arr.append(str_list[signer_index+9])
                signer_index += 9

    #         if 'Counter Signers:' in str_list:  #如果有 counter signer
    #             countersigner_arr = []
    #             countersigner_index = str_list.index('Counter Signers:')
    #             #print(str_list[countersigner_index])
    #             countersigner_index += 1
    #             countersigner_arr.append(str_list[countersigner_index])

    #             # 列出所有 counter signer
    #             while re.search(r'^Company:', str_list[countersigner_index+9]) == None:
    #                 countersigner_arr.append(str_list[countersigner_index+9])
    #                 countersigner_index += 9
    #             #print(countersigner_arr)

    #             return signer_arr, countersigner_arr  #有簽章，有signer, counter signer
    #         else:
            return signer_arr  #有簽章，只有signer

        else:
            return None  #沒有簽章
    
    except UnicodeDecodeError as error:
        return 'error'
    
def pefile_dump(filepath):
    '''
    使用pefile套件，dump出該檔案所有資訊，並存成一個txt
    '''
    currentPath = os.getcwd()    # 取得當前檔案路徑 (要將txt存在掃描exe下載的同個資料夾)

    if os.path.isfile(currentPath+'\pefileInfo.txt') == False:  # 尚無txt檔就先建立
        fp = open("pefileInfo.txt","a")
        fp.close()
    startLine = len(open("pefileInfo.txt",'rU').readlines()) # 寫入前起始行數
    pe = pefile.PE(filepath, fast_load=True)

    fp = open("pefileInfo.txt","a") # 使用append才不會覆蓋舊有文字
    fp.write(pe.dump_info())   # dump_info() 全部資訊
    fp.close()
    endLine = len(open("pefileInfo.txt",'rU').readlines()) # 寫入後行數
    return (startLine, endLine)
 
def check_pack(pe_file):
    '''
    使用peutils套件，判斷檔案是否有進行加殼 
    '''
    with open('userdb_filter.txt', 'rt', encoding = 'utf8') as f:  # userdb_filter.txt 有經過過濾處理，去掉不符合byte格式的
        sig_data = f.read()
    signatures = peutils.SignatureDatabase(data = sig_data)

    matches = signatures.match(pe_file, ep_only = True)
    matchall = signatures.match_all(pe_file, ep_only = True)
    
    return matchall
    
def BOOL_RW(pe_file):
    '''
    讀寫檔案能力判斷
    '''
    FILE_MANAGEMENT_FUNCTIONS = ['advapi32.dll', 'kernel32.dll', 'wofutil.dll', 'lz32.dll']
    
    pe_file.parse_data_directories()
    for entry in pe_file.DIRECTORY_ENTRY_IMPORT:
        try:
            dll = entry.dll.decode('utf-8').lower()
            if dll in FILE_MANAGEMENT_FUNCTIONS:
                return True
            else:
                return False
        except AttributeError as error:
            pass
        
def BOOL_INTERNET(pe_file):
    '''
    連網能力判斷
    '''
    NETWORKING_AND_INTERNET = ['dnsapi.dll', 'dhcpcsvc.dll', 'dhcpcsvc6.dll', 'dhcpsapi.dll', 'connect.dll', 
                           'httpapi.dll', 'netshell.dll', 'iphlpapi.dll', 'netfwv6.dll', 'dhcpcsvc.dll',
                           'hnetcfg.dll', 'netapi32.dll', 'qosname.dll', 'rpcrt4.dll', 'mgmtapi.dll', 'snmpapi.dll',
                           'smbwmiv2.dll', 'tapi32.dll', 'netapi32.dll', 'davclnt.dll', 'websocket.dll',
                           'bthprops.dll', 'wifidisplay.dll', 'wlanapi.dll', 'wcmapi.dll', 'fwpuclnt.dll',
                           'firewallapi.dll', 'winhttp.dll', 'wininet.dll', 'wnvapi.dll', 'ws2_32.dll',
                           'webservices.dll']
    
    pe_file.parse_data_directories()
    for entry in pe_file.DIRECTORY_ENTRY_IMPORT:
        try:
            dll = entry.dll.decode('utf-8').lower()
            if dll in NETWORKING_AND_INTERNET:
                return True
            else:
                return False
        except AttributeError as error:
            pass
        
def BOOL_EXEC(pe_file):
    '''
    執行其他可執行檔能力判斷
    '''
    EXECUTION_FUNCTIONS = ['winexec']
    
    pe_file.parse_data_directories()
    for entry in pe_file.DIRECTORY_ENTRY_IMPORT:
        for function in entry.imports:
            try:
                if function.name.decode('utf-8').lower() in EXECUTION_FUNCTIONS:
                    return True
                else:
                    return False
            except AttributeError as error:
                pass

def pefile_info(filepath, pefile_option, peutils_option, rw_option, internet_option, exec_option, sigcheck_option, fileTime_option, fileVisibility_option):
    """
    1. 使用pefile套件，dump出該檔案所有資訊，並存成一個txt
    2. 使用peutils套件，判斷檔案是否有進行加殼 
    3. 讀寫檔案能力判斷
    4. 連網能力判斷
    5. 執行其他可執行檔能力判斷
    6. 判斷檔案是否具有可信認之數位簽章，使用sigcheck.exe
    7. 蒐集可執行檔之時間資訊(生成時間、存取時間、變更時間、編譯時間...)
    8. 是否為隱藏檔案(os.path)
       read only:1, hidden:2, directory:16, normal:128, compressed:2048, encrypted:16384
       
    參考套件網址
    https://github.com/erocarrera/pefile
    https://github.com/erocarrera/pefile/blob/wiki/PEiDSignatures.md
    https://docs.microsoft.com/en-us/sysinternals/downloads/sigcheck
    https://docs.microsoft.com/en-us/windows/win32/fileio/file-attribute-constants
    """
    result_dict = {}
    result_dict['filepath']=filepath
    
    if(pefile_option == 0 and (peutils_option == 1 or rw_option == 1 or internet_option == 1 or exec_option == 1)):
        pe = pefile.PE(filepath, fast_load=True) 
    
    # 1. pefile
    if(pefile_option == 1):
        currentPath = os.getcwd()    # 取得當前檔案路徑 (要將txt存在掃描exe下載的同個資料夾)

        if os.path.isfile(currentPath+'\pefileInfo.txt') == False:  # 尚無txt檔就先建立
            fp = open("pefileInfo.txt","a")
            fp.close()
        startLine = len(open("pefileInfo.txt",'r').readlines())+1 # 寫入前起始行數
        pe = pefile.PE(filepath, fast_load=True)

        fp = open("pefileInfo.txt","a",newline="\r\n") # 使用append才不會覆蓋舊有文字
        fp.write(pe.dump_info())   # dump_info() 全部資訊
        fp.close()
        endLine = len(open("pefileInfo.txt",'r').readlines()) # 寫入後行數
        
        result_dict['pefile_txt_offset_start'] = startLine
        result_dict['pefile_txt_offset_end'] = endLine
    
    # 2. peutils   
    if(peutils_option == 1):
        result_dict['peutils'] = str(check_pack(pe))
    
    # 3. 讀寫檔案能力判斷
    if(rw_option == 1):
        result_dict['rw'] = BOOL_RW(pe)
        
    # 4. 連網能力判斷
    if(internet_option == 1):
        result_dict['internet'] = BOOL_INTERNET(pe)
        
    # 5. 執行其他可執行檔能力判斷
    if(exec_option == 1):
        result_dict['exec_other_exe'] = BOOL_EXEC(pe)
        
    # 6. 判斷檔案是否具有可信認之數位簽章，使用sigcheck.exe
    if(sigcheck_option == 1):
        result_dict['signer'] = str(sigcheck(filepath))
    
    # 7. 蒐集可執行檔之時間資訊(生成時間、存取時間、變更時間、編譯時間...)
    if(fileTime_option == 1):
        create_time = time.ctime(os.path.getctime(filepath))   # create time
        last_modified_time = time.ctime(os.path.getmtime(filepath))   # modified time
        access_time = time.ctime(os.path.getatime(filepath))   # access time
        result_dict['create_time']=create_time
        result_dict['last_modified_time']=last_modified_time
        result_dict['access_time']=access_time
    
    # 8. 是否為隱藏檔案
    if(fileVisibility_option == 1):
        attribute = win32api.GetFileAttributes(filepath)
        result_dict['file_state(isHidden)']=attribute
    
    df = pd.DataFrame(result_dict, index = [0])
    return df


def openfile(filepath, file_arr, byte_option, printableString_option, entropy_option, scanHeader_option):
    """
    1. 開檔案讀每種byte的個數
    2. 開檔案讀連續3個以上的可列印字元string (回server後再用regex分析字串內容?or在這直接做? 看執行時間) 
    3. 計算該檔案的entropy
    4. 掃描標頭?
    
    可列印字元參考網址:
    https://stackoverflow.com/questions/42064158/checking-if-a-byte-is-ascii-printable
    """
    # byte
    byteResults = [0]*256
    
    # 可列印字元
    printable_chars = set(bytes(string.printable, 'ascii'))  #用 set 好像可以比單純比對 string 快
    printable_list = []
    tmp_printable_chars = ""
    
    # 標頭 0x5A4D
    header=''
    
    # return dict
    result_dict = {}
    
    if(byte_option!=0 and printableString_option!=0 and entropy_option!=0 and scanHeader_option!=0):
        with open(filepath, 'rb') as file:
            while True:
                byte = file.read(1)
                if byte:
                    
                    # 標頭判斷
                    if(scanHeader_option == 1 and len(header) < 4):  
                        header += binascii.hexlify(byte).decode('ascii')
                    elif(scanHeader_option == 1 and header != '4d5a'):
                        return
                        
                    # byte統計
                    if(byte_option == 1 or entropy_option == 1):   
                        data = int(binascii.hexlify(byte), 16)
                        byteResults[data] += 1 

                    # 可列印字元的處理
                    if(printableString_option == 1):
                        if int(binascii.hexlify(byte), 16) in printable_chars:  
                            tmp_printable_chars += byte.decode()
                        elif tmp_printable_chars != "" and len(tmp_printable_chars) >= 3:
                            printable_list.append(tmp_printable_chars)
                            tmp_printable_chars = ""
                        else:
                            tmp_printable_chars = ""
                else:
                    if(scanHeader_option == 1):
                        file_arr.append(filepath)    # 把路徑加到 arr
                        # result_dict['filepath'] = filepath
                    
                    if(byte_option==1):
                        for i in range(len(byteResults)):
                            result_dict[str(i)] = byteResults[i]
                        # result_arr.append(byteResults)
                    
                    if(printableString_option==1):
                        # result_dict['printable_list']=printable_list
                        # result_arr.append(printable_list)
                        currentPath = os.getcwd()    # 取得當前檔案路徑 (要將txt存在掃描exe下載的同個資料夾)

                        if os.path.isfile(currentPath+'\printableString.txt') == False:  # 尚無txt檔就先建立
                            fp = open("printableString.txt","a")
                            fp.close()
                        startLine = len(open("printableString.txt",'r').readlines()) # 寫入前起始行數

                        fp = open("printableString.txt","a") # 使用append才不會覆蓋舊有文字
                        fp.write(str(printable_list) + '\n')   
                        fp.close()
                        endLine = len(open("printableString.txt",'r').readlines()) # 寫入後行數
                        result_dict['printableString_offset'] = startLine
                        
                    if(entropy_option == 1):
                        entropy = 0
                        for item in byteResults:
                            freq = item / sum(byteResults)
                            entropy = entropy + freq * math.log(freq, 2)
                        entropy *= -1
                        result_dict['entropy'] = entropy
                        # result_arr.append(entropy)
                    
                    df = pd.DataFrame(result_dict, index = [0])
                    
                    return df
        


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)


def toXML(xmlname, option_dict, host_df, file_df):
    option_dic = eval(option_dict)
    root = ET.Element("scan")

    doc1=ET.SubElement(root,"engine", version="1.0")
    
    doc5 = ET.SubElement(root,"metadata")
    doc5_1 = ET.SubElement(doc5, "start_time")
    doc5_1.text = str(host_df.loc[0,'start_time'])
    doc5_2 = ET.SubElement(doc5, "end_time")
    doc5_2.text = str(host_df.loc[0,'end_time'])
    
    if(option_dic['hostInfo_option'] == 1):
        doc2=ET.SubElement(root,"machine")
        doc2_1=ET.SubElement(doc2, "user")
        doc2_1.text = str(host_df.loc[0,'username'])
        doc2_2=ET.SubElement(doc2, "computer_name")
        doc2_2.text = str(host_df.loc[0,'hostname'])
        doc2_3=ET.SubElement(doc2, "mac_addr")
        doc2_3.text = str(host_df.loc[0,'mac_addr'])
        # doc2_4=ET.SubElement(doc2, "processor_name")
        doc2_5=ET.SubElement(doc2, "memory_capacity-MB")
        doc2_5.text = str(host_df.loc[0,'memory_capacity(MB)'])
        # doc2_6=ET.SubElement(doc2, "os")
        doc2_7=ET.SubElement(doc2, "ip")
        doc2_7.text = str(host_df.loc[0,'ip_addr'])
        # doc2_8=ET.SubElement(doc2, "cpu_LoadPercentage")
        # doc2_9=ET.SubElement(doc2, "sys")
        # doc2_10=ET.SubElement(doc2, "startup_command")
    
    if (option_dic['registry_option'] == 1):
        doc3=ET.SubElement(root,"registry")
        doc3_1=ET.SubElement(doc3,"HKEY_LOCAL_MACHINE - SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
        doc3_1.text = str(host_df.loc[0,'HKEY_LOCAL_MACHINE(SOFTWARE\Microsoft\Windows\CurrentVersion\Run)'])
        doc3_2=ET.SubElement(doc3,"HKEY_LOCAL_MACHINE - SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce")
        doc3_2.text = str(host_df.loc[0,'HKEY_LOCAL_MACHINE(SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce)'])
        doc3_3=ET.SubElement(doc3,"HKEY_CURRENT_USER - SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
        doc3_3.text = str(host_df.loc[0,'HKEY_CURRENT_USER(SOFTWARE\Microsoft\Windows\CurrentVersion\Run)'])
        doc3_4=ET.SubElement(doc3,"HKEY_CURRENT_USER - SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce")
        doc3_4.text = str(host_df.loc[0,'HKEY_CURRENT_USER(SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce)'])
    
    doc4=ET.SubElement(root,"config")
    doc4_1=ET.SubElement(doc4, "checked_option")
    doc4_1.text = str(option_dict)
        
    doc6=ET.SubElement(root,"files")
    
    for i in range(len(file_df.index)):
#         m = hashlib.sha256()
#         h = m.update(str(file_df.loc[i,'filepath']).encode("utf-8")).hexdigest()
#         hashValue=h,
        doc6_1 = ET.SubElement(doc6,"file", filePath=str(file_df.loc[i,'filepath']),  size=file_size(str(file_df.loc[i,'filepath'])))
        
        if (option_dic['fileTime_option'] == 1):
            doc_6_1_1 = ET.SubElement(doc6_1,"create_time")
            doc_6_1_1.text = str(file_df.loc[i,'create_time'])
            doc_6_1_2 = ET.SubElement(doc6_1,"last_modify_time")
            doc_6_1_2.text = str(file_df.loc[i,'last_modified_time'])
            doc_6_1_3 = ET.SubElement(doc6_1,"last_access_time")
            doc_6_1_3.text = str(file_df.loc[i,'access_time'])
        
        if (option_dic['pefile_option'] == 1):
            doc_6_1_4 = ET.SubElement(doc6_1,"pefiletxt_offset")
            doc_6_1_4.text = '('+str(file_df.loc[i,'pefile_txt_offset_start'])+','+str(file_df.loc[i,'pefile_txt_offset_end'])+')'
        
        if (option_dic['rw_option'] == 1):
            doc_6_1_9 = ET.SubElement(doc6_1,"rw")
            doc_6_1_9.text = str(file_df.loc[i,'rw'])
            
        if (option_dic['internet_option'] == 1):
            doc_6_1_10 = ET.SubElement(doc6_1,"internet")
            doc_6_1_10.text = str(file_df.loc[i,'internet'])
        
        if (option_dic['exec_option'] == 1):
            doc_6_1_10 = ET.SubElement(doc6_1,"exec_other_exe")
            doc_6_1_10.text = str(file_df.loc[i,'exec_other_exe'])
        
        if (option_dic['peutils_option'] == 1):
            doc_6_1_5 = ET.SubElement(doc6_1,"packed")
            doc_6_1_5.text = str(file_df.loc[i,'peutils'])
        
        if (option_dic['sigcheck_option'] == 1):
            doc_6_1_6 = ET.SubElement(doc6_1,"signed")
            doc_6_1_6.text = str(file_df.loc[i,'signer'])
        
        if (option_dic['fileVisibility_option'] == 1):
            doc_6_1_7 = ET.SubElement(doc6_1,"file_state")   # is_hidden
            doc_6_1_7.text = str(file_df.loc[i,'file_state(isHidden)'])
        
        if (option_dic['entropy_option'] == 1):
            doc_6_1_8=ET.SubElement(doc6_1,"entropy")
            doc_6_1_8.text = str(file_df.loc[i,'entropy'])
        
        
        # offset
    tree=ET.ElementTree(root)
    tree.write(os.getcwd()+'/'+xmlname+'.xml',encoding="unicode")


def main(option_dic, dir_array):
    '''
    主程式
    option_dic 掃描勾選選項
    dir_array  待掃描資料夾
    '''  
    start_time = datetime.datetime.now()
    option_dict = eval(option_dic)
    dir_arr = eval(dir_array)
    
    # 讀端點電腦資訊
    host_data = host_info(option_dict['hostInfo_option'], option_dict['registry_option'])
    
    # 從選取的資料夾中讀取檔案 , file_arr存放檔案路徑 https://www.ewdna.com/2012/04/pythonoswalk.html
    file_arr = []
    file_df = pd.DataFrame()
    for d in range(len(dir_arr)):
        if dir_arr[d] != '':  # 從該目錄下讀取子目錄及檔案
            for dirPath, dirNames, fileNames in os.walk(dir_arr[d]):
                for f in fileNames:
                    # 需要再判斷檔案是不是exe
                    if (option_dict['scanHeader_option'] != 1): # 直接看檔名結尾判斷是否為exe
                        ext = os.path.splitext(f)[-1]  #用.分隔 
                        if ext == '.exe':
                            file_arr.append(os.path.join(dirPath, f))
                            file_df2 = pefile_info(os.path.join(dirPath, f), option_dict['pefile_option'], option_dict['peutils_option'], option_dict['rw_option'], option_dict['internet_option'], option_dict['exec_option'], option_dict['sigcheck_option'], option_dict['fileTime_option'], option_dict['fileVisibility_option'])
                            file_df = pd.concat([file_df, file_df2], ignore_index=True)
                    else:
                        file_df1 = openfile(os.path.join(dirPath, f), file_arr, option_dict['byte_option'], option_dict['printableString_option'], option_dict['entropy_option'], option_dict['scanHeader_option'])
                        file_df2 = pefile_info(os.path.join(dirPath, f), option_dict['pefile_option'], option_dict['peutils_option'], option_dict['rw_option'], option_dict['internet_option'], option_dict['exec_option'], option_dict['sigcheck_option'], option_dict['fileTime_option'], option_dict['fileVisibility_option'])
                        file_df_concat = pd.concat([file_df2, file_df1] , axis=1)
                        file_df = pd.concat([file_df, file_df_concat], ignore_index=True)
        else:
            pass
    
    end_time = datetime.datetime.now()
    timeInfo = pd.DataFrame({'start_time':start_time, 'end_time':end_time}, index=[0])
    host_df = pd.concat([timeInfo, host_data], axis=1)
    
    host_df.to_csv('pefile_scan_hostInfo.csv')
    file_df.to_csv('pefile_scan_result.csv')
    toXML('scanresultxml',option_dic, host_df, file_df)    
        
    return option_dic, host_df, file_df         



main(sys.argv[1], sys.argv[2])    # sys.argv[1]: option_dict, sys.argv[2]: dir_arr
