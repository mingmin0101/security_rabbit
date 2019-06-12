# coding: utf-8

import peutils   # def peIdSignature()
import os
import subprocess
import pefile

# 判斷檔案是否有進行加殼 https://github.com/erocarrera/pefile/blob/wiki/PEiDSignatures.md
def peIdSignature(filename):
    with open('userdb3.txt', 'rt', encoding = 'utf8') as f:  # userdb.txt 有經過過濾處理，去掉不符合byte格式的
        sig_data = f.read()
    signatures = peutils.SignatureDatabase(data=sig_data)

    pe = pefile.PE(filename, fast_load=True)  #pe = pefile.PE(file_arr[f], fast_load=True)
    matches = signatures.match(pe, ep_only = True)
    matchall = signatures.match_all(pe, ep_only = True)
    return matches


# 判斷檔案是否具有可信認之數位簽章 https://docs.microsoft.com/en-us/sysinternals/downloads/sigcheck
def sigcheck():
    # 用 python 下 command ，subprocess 與 Popen()  https://www.cnblogs.com/Security-Darren/p/4733368.html
    p = subprocess.Popen('sigcheck -i MicrosoftEdge.exe', shell=True)
    myCmd = os.popen('sigcheck -i -nobanner MicrosoftEdge.exe').read()
    print(myCmd)
    ####### 還沒寫parser