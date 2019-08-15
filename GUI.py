# coding: utf-8
# 2019-07-29 update

import tkinter as tk
from tkinter import filedialog  # 檔案視窗
from tkinter import ttk  # 比較美觀一點的介面套件
import platform
import os
import subprocess
import requests


# pip install requests 
# import requests

#status code 
#200 request success
#403 Forbidden (CSRF token not set) 
#500 internal server error

class RabbitClient:
    def __init__(self):
        self.downloadURL=""
        self.uploadURL=""
        self.client=None
        self.csrftoken=""
    
    def startSession(self):
        self.uploadURL='http://127.0.0.1:8000/uploadxml/'
        self.client = requests.session()
        r=self.client.get(self.uploadURL)
        self.csrftoken=self.client.cookies['csrftoken']

        #print(r.status_code)
        #print(self.csrftoken)

    def clientUploadfile(self,filetoupload):
        with open(filetoupload,'rb') as xmlfile:
            r2 = self.client.post(self.uploadURL,files={'docfile':xmlfile},data={'csrfmiddlewaretoken':self.csrftoken})
            #print(r2.status_code)
            #print(r2.content)
    
    def clientDownloadfile(self):
        self.downloadURL='http://127.0.0.1:8000/downloadpy/core_function'
        r = self.client.get(self.downloadURL)
        pyfile = open("rabbit_scanner.py",'wb+')
        pyfile.write(r.content)
        pyfile.close()

        self.downloadURL='http://127.0.0.1:8000/downloadexe/sigcheck'
        r2 = self.client.get(self.downloadURL)
        pyfile = open("sigcheck.exe",'wb+')
        pyfile.write(r2.content)
        pyfile.close()

        self.downloadURL='http://127.0.0.1:8000/downloadtxt/userdb_filter'
        r3 = self.client.get(self.downloadURL)
        pyfile = open("userdb_filter.txt",'wb+')
        pyfile.write(r3.content)
        pyfile.close()

        #print("clientDownloadfile")
        #print(r.status_code)
        
# if __name__ == '__main__':
#     rab=RabbitClient()
#     rab.startSession()
#     rab.clientUploadfile('test.txt')
#     rab.clientDownloadfile()


# In[11]:


# 掃描路徑選擇
dir_arr = ['','','','','','']   # 待掃描資料夾arr [homepath, programfiles, programfiles(x86), windir, systemdrive, (option)]
def path_selection():
    global var_homepath,var_programfiles,var_windir,var_systemdrive,var_other,filepath_var
    dir_arr[0] = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'] if (var_homepath.get() == 1) else ''
 
    if (var_programfiles.get() == 1):
        if(platform.architecture()[0] == "32bit"):
            dir_arr[1] = os.environ["ProgramFiles"]
        elif(platform.architecture()[0] == "64bit"):
            dir_arr[1] = os.environ["ProgramFiles"]        # 放64位元的
            dir_arr[2] = os.environ["ProgramFiles(x86)"]   # 放32位元的
    else:
        dir_arr[1] = ''
        dir_arr[2] = ''
    
    dir_arr[3] = os.environ['WINDIR'] if (var_windir.get() == 1) else ''
    dir_arr[4] = os.environ['systemdrive'] if (var_systemdrive.get() == 1) else ''
    dir_arr[5] = filepath_var.get() if (var_other.get() == 1 and filepath_var.get() != '請選擇路徑') else ''
        
# 自選待掃描資料夾
def selectDir():
    global filepath_var, filepath_input, var_other
    var_other.set(value=1)
    dir_opened = filedialog.askdirectory()
    filepath_var.set(dir_opened)
    dir_arr[5] = filepath_var.get() if (var_other.get() == 1 and filepath_var.get() != '請選擇路徑') else ''
    

# 按下開始後執行的功能 (到時候會向server取.py檔)
def parseFile():
    # 下載 server上的 py檔(or主功能py打包的exe)
    rab = RabbitClient()
    rab.startSession()
    rab.clientDownloadfile()
    
    global start_button, dir_arr
    
    start_button.config(text='掃描中...')
    start_button.config(state='disabled')
    
    # 掃描選項
    option_dict = {
        'pefile_option':general_options['自動解析檔案內部結構(pefile)'].get(),
        'peutils_option':general_options['加殼(peutils)'].get(),
        'rw_option':general_options['辨識檔案存取(讀、寫)能力'].get(),
        'internet_option':general_options['辨識檔案連網能力'].get(),
        'exec_option':general_options['是否可以執行其他可執行檔(WinExec)'].get(),
        'sigcheck_option':general_options['數位簽章(sigcheck)'].get(),
        'byte_option':advance_options['掃描每種byte個數'].get(),
        'printableString_option':advance_options['掃描可列印字元'].get(),
        'entropy_option':advance_options['計算entropy，辨識是否被壓縮加密'].get(),
        'scanHeader_option':advance_options['掃描檔案標頭，辨識檔案為windows PE執行檔'].get(),
        'hostInfo_option':general_options['硬體、軟體及作業系統資訊'].get(),
        'registry_option':general_options['是否註冊windows系統機碼'].get(),
        'fileTime_option':general_options['蒐集可執行檔之時間資訊'].get(),
        'fileVisibility_option':general_options['是否為隱藏檔案'].get()}

    option_arr = [ general_options[option_text] for option_text in general_options]

    # 暫時執行另一個file
    p = subprocess.Popen(['python','rabbit_scanner.py',str(option_dict), str(dir_arr)],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    scan_result = p.communicate()[0]
    erroutput = p.communicate()[1] 

    # 隱藏開始按鈕，顯示完成按鈕
    start_button.grid_forget()
    
    # 上傳檔案
    if(option_dict['pefile_option'] == 1):
        rab.clientUploadfile('pefileInfo.txt')
        
    if(option_dict['printableString_option'] == 1):
        rab.clientUploadfile('printableString.txt')
        
    rab.clientUploadfile('scanresultxml.xml')
    rab.clientUploadfile('pefile_scan_hostInfo.csv')
    rab.clientUploadfile('pefile_scan_result.csv')
    
def closeWindow():
    root.destroy()


# In[12]:


# 主視窗
root = tk.Tk()
root.title('Security Scan')  # 視窗標題
root.resizable(False, False)

# 創建 label 容器 ----- ttk.LabelFrame
# server_container = ttk.LabelFrame(root, text="Server")     # 創建容器，其父容器為 root
# server_container.grid(column=0, row=0, padx=5, pady=3, ipady=3, sticky=tk.E + tk.W)    # padx pady容器外圍要預留的空間，ipady容器內

dir_scan_container = ttk.LabelFrame(root, text="Directories to be scanned")    
dir_scan_container.grid(column=0, row=2, padx=5, pady=3, ipady=3, sticky=tk.E + tk.W)

options_container = ttk.LabelFrame(root, text="Options")    
options_container.grid(column=0, row=8, padx=5, pady=3, ipady=3, sticky=tk.E + tk.W)

# 建立 選server 下拉選單 ----- tkk.Combobox
# server_select = ttk.Combobox(server_container, values=["server1", "server2"], width=30)   # 設定下拉選單的選項，看有幾台 server
# server_select.current(0)    # default值，從values中選取
# server_select.grid(column=0, row=1, sticky=tk.E + tk.W)

# Directories to be scanned 掃描路徑選擇 ----- ttk.Checkbutton
var_homepath = tk.IntVar() # 用來獲取複選框是否有被勾選，透過.get()來獲取狀態，狀態值為int類型 : 勾選為1，未勾選為0
var_programfiles = tk.IntVar()
var_windir = tk.IntVar()
var_systemdrive = tk.IntVar()
var_other = tk.IntVar()
d1 = ttk.Checkbutton(dir_scan_container, text='homepath ('+os.environ['HOMEDRIVE']+os.environ['HOMEPATH']+')', variable=var_homepath, onvalue=1, offvalue=0, command=path_selection)
if(platform.architecture()[0] == "32bit"):
    d2 = ttk.Checkbutton(dir_scan_container, text='programfiles ('+os.environ["ProgramFiles"]+')', variable=var_programfiles, onvalue=1, offvalue=0, command=path_selection)
elif(platform.architecture()[0] == "64bit"):
    d2 = ttk.Checkbutton(dir_scan_container, text='programfiles ('+os.environ["ProgramFiles"]+', '+os.environ["ProgramFiles(x86)"]+')', variable=var_programfiles, onvalue=1, offvalue=0, command=path_selection)

d3 = ttk.Checkbutton(dir_scan_container, text='windir ('+os.environ['WINDIR']+')', variable=var_windir, onvalue=1, offvalue=0, command=path_selection)
d4 = ttk.Checkbutton(dir_scan_container, text='systemdrive ('+os.environ['systemdrive']+')', variable=var_systemdrive, onvalue=1, offvalue=0, command=path_selection)
d5 = ttk.Checkbutton(dir_scan_container, text='other', variable=var_other, onvalue=1, offvalue=0, command=path_selection)
d1.grid(column=0, row=3, sticky=tk.W) # sticky=tk.W 對齊用 (N北/上，S南/下，W西/左，E東/右) 
d2.grid(column=0, row=4, sticky=tk.W)
d3.grid(column=0, row=5, sticky=tk.W)
d4.grid(column=0, row=6, sticky=tk.W)
d5.grid(column=0, row=7, sticky=tk.W)

# 文字框(自訂輸入檔案路徑) + 瀏覽資料夾視窗
filepath_var = tk.StringVar(value='請選擇路徑')     
filepath_input = ttk.Entry(dir_scan_container, width=12, textvariable = filepath_var) # , state='disabled'   
filepath_input.place(x = 55, y = 85, width=150, height=20)      

browse_file_button = ttk.Button(dir_scan_container, text='...', command = selectDir) #按下按鈕執行 selectDir 這個 function 
browse_file_button.place(x = 210, y = 85, width=20, height=20)

def option_selection():
    mode = var_option.get()
    if (mode == 1):  # 一般掃描
        for option_text in general_options:
            general_options[option_text].set(value=1)

        for option_text in advance_options:
            advance_options[option_text].set(value=0)

        for button in general_buttons:
            button.config(state='disabled')

        for button in advance_buttons:
            button.config(state='disabled')
            
    elif (mode == 2):  # 深度掃描
        for option_text in advance_options:
            advance_options[option_text].set(value=1)

        for button in general_buttons:
            button.config(state='disabled')

        for button in advance_buttons:
            button.config(state='disabled')
         
    elif (mode == 3):   # 自訂
        for button in general_buttons:
            button.config(state='normal')
        
        for button in advance_buttons:
            button.config(state='normal')
        
# Options 進階選擇 ----- ttk.Radiobutton
var_option = tk.IntVar(value=1)   # value是預設值
o1 = ttk.Radiobutton(options_container, text='一般掃描', variable=var_option, value='1', command=option_selection)
o2 = ttk.Radiobutton(options_container, text='深度掃描', variable=var_option, value='2', command=option_selection)
o3 = ttk.Radiobutton(options_container, text='自訂掃描', variable=var_option, value='3', command=option_selection)
o1.grid(column=0, row=9, sticky=tk.W)
o2.grid(column=1, row=9, sticky=tk.W)
o3.grid(column=2, row=9, sticky=tk.W)

# option細項
general_options = {
                    '自動解析檔案內部結構(pefile)': tk.IntVar(value=1),
                    '數位簽章(sigcheck)': tk.IntVar(value=1),
                    '加殼(peutils)': tk.IntVar(value=1),
                    '蒐集可執行檔之時間資訊': tk.IntVar(value=1),
                    '硬體、軟體及作業系統資訊': tk.IntVar(value=1),
                    '是否可以執行其他可執行檔(WinExec)': tk.IntVar(value=1),
                    '辨識檔案存取(讀、寫)能力': tk.IntVar(value=1),
                    '辨識檔案連網能力': tk.IntVar(value=1),
                    '是否為隱藏檔案': tk.IntVar(value=1),
                    '是否註冊windows系統機碼':tk.IntVar(value=1)
                }
advance_options = {
                    '掃描檔案標頭，辨識檔案為windows PE執行檔': tk.IntVar(),
                    '掃描每種byte個數': tk.IntVar(),
                    '計算entropy，辨識是否被壓縮加密': tk.IntVar(),
                    '掃描可列印字元': tk.IntVar(),
                    '納入SYS、DLL': tk.IntVar()
                }
general_buttons = []
advance_buttons = []

#arrangement problem will come back later
for index,option_text in enumerate(general_options):
    general_buttons.append(ttk.Checkbutton(options_container, text=option_text, variable= general_options[option_text], onvalue=1, offvalue=0, command=option_selection, state='disabled'))
    general_buttons[index].grid(column=0, row = index + 10, sticky=tk.W)

for index,option_text in enumerate(advance_options):
    advance_buttons.append(ttk.Checkbutton(options_container, text=option_text, variable=advance_options[option_text], onvalue=1, offvalue=0, command=option_selection, state='disabled'))
    advance_buttons[index].grid(column=2, row=index + 10, sticky=tk.W)


# 執行按鈕 ----- ttk.Button
end_button = ttk.Button(root, text='完成', command=closeWindow) 
end_button.grid(column=0, row=11, sticky=tk.E, padx=5, pady=5)
start_button = ttk.Button(root, text='開始掃描', command=parseFile) # 按下按鈕執行parseFile這個function 
start_button.grid(column=0, row=11, sticky=tk.E, padx=5, pady=5)


# 進度條 ----- ttk.Progressbar
# progress_bar = ttk.Progressbar(root, orient='horizontal', length=150, mode='determinate')  # mode:定量(determinate)不定量(indeterminate)
# progress_bar.grid(column=0, row=11, sticky=tk.W, padx=5, pady=5)

root.mainloop() #讓程式推入與使用者互動模式

