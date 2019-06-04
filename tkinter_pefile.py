
# coding: utf-8


import pefile
import tkinter as tk
from tkinter import filedialog  # 檔案視窗
from tkinter import ttk  # 比較美觀一點的介面套件
import os #取目錄用


# 掃描路徑選擇
dir_arr = ['','','','','']  # 待掃描資料夾arr [homepath, programfiles, windir, systemdrive, (option)]
def path_selection():
    global var_homepath,var_programfiles,var_windir,var_systemdrive,var_other,filepath_var
    dir_arr[0] = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'] if (var_homepath.get() == 1) else ''
    dir_arr[1] = os.environ["ProgramFiles"] if (var_programfiles.get() == 1) else ''
    dir_arr[2] = os.environ['WINDIR'] if (var_windir.get() == 1) else ''
    dir_arr[3] = os.environ['systemdrive'] if (var_systemdrive.get() == 1) else ''
    dir_arr[4] = filepath_var.get() if (var_other.get() == 1 and filepath_var.get() != '請選擇路徑') else ''
        
# 自選待掃描資料夾
def selectDir():
    global filepath_var,filepath_input,var_other
    dir_opened = filedialog.askdirectory()
    filepath_var.set(dir_opened)
    dir_arr[4] = filepath_var.get() if (var_other.get() == 1 and filepath_var.get() != '請選擇路徑') else ''

# 進階選項(掃描模式)  
mode = 1
def option_selection():
    mode = var_option.get()

# 按下開始後執行的功能 (到時候會向server取.py檔)
def parseFile():
    global var_option, dir_arr
    
    # 掃描模式 ------之後要根據不同掃描模式要做什麼修改程式
    mode = var_option.get()
    
    # 從選取的資料夾中讀取檔案 , file_arr存放檔案路徑 https://www.ewdna.com/2012/04/pythonoswalk.html
    file_arr = []
    for d in range(len(dir_arr)):
        if dir_arr[d] != '':  # 從該目錄下讀取子目錄及檔案
            for dirPath, dirNames, fileNames in os.walk(dir_arr[d]):
                for f in fileNames:
                    # 需要再判斷檔案是不是exe
                    ext = os.path.splitext(f)[-1]  #用.分隔
                    if ext == '.exe':
                        file_arr.append(os.path.join(dirPath, f))      
        else:
            pass
     
    # 對取出的檔案們做一些運算 (e.g., 用 pefile 套件取值)
#     while(len(file_arr) != 0):
    for f in range(len(file_arr)):
        pe = pefile.PE(file_arr[f], fast_load=True)  # fast_load=True, prevent parsing the directories
        print(file_arr[f])
        for section in pe.sections:
            print (section.Name, hex(section.VirtualAddress), hex(section.Misc_VirtualSize), section.SizeOfRawData)
        print('----------------------')
        #file_arr.pop(file_arr[f])  # 做完就丟掉
    
    print(dir_arr)
    print(file_arr)
    print(mode)


#     for section in pe.sections:
#         print (section.Name, hex(section.VirtualAddress), hex(section.Misc_VirtualSize), section.SizeOfRawData)
#     for section in pe.sections:    
#         T.insert('insert', 'section name: '+str(section.Name)+', section virtual address: '+hex(section.VirtualAddress)+', section misc_virtualSize: '+hex(section.Misc_VirtualSize)+', section size of raw data: '+str(section.SizeOfRawData)+"\n")



# 主視窗
root = tk.Tk()
root.title('Security Scan')  # 視窗標題
root.resizable(False, False)

# 創建 label 容器 ----- ttk.LabelFrame
server_container = ttk.LabelFrame(root, text="Server")     # 創建容器，其父容器為 root
server_container.grid(column=0, row=0, padx=5, pady=3, ipady=3, sticky=tk.E + tk.W)    # padx pady容器外圍要預留的空間，ipady容器內

dir_scan_container = ttk.LabelFrame(root, text="Directories to be scanned")    
dir_scan_container.grid(column=0, row=2, padx=5, pady=3, ipady=3, sticky=tk.E + tk.W)

options_container = ttk.LabelFrame(root, text="Options")    
options_container.grid(column=0, row=8, padx=5, pady=3, ipady=3, sticky=tk.E + tk.W)

# 建立 選server 下拉選單 ----- tkk.Combobox
server_select = ttk.Combobox(server_container, values=["server1", "server2"], width=30)   # 設定下拉選單的選項，看有幾台 server
server_select.current(0)    # default值，從values中選取
server_select.grid(column=0, row=1, sticky=tk.E + tk.W)

# Directories to be scanned 掃描路徑選擇 ----- ttk.Checkbutton
var_homepath = tk.IntVar() # 用來獲取複選框是否有被勾選，透過.get()來獲取狀態，狀態值為int類型 : 勾選為1，未勾選為0
var_programfiles = tk.IntVar()
var_windir = tk.IntVar()
var_systemdrive = tk.IntVar()
var_other = tk.IntVar()
d1 = ttk.Checkbutton(dir_scan_container, text='homepath ('+os.environ['HOMEDRIVE']+os.environ['HOMEPATH']+')', variable=var_homepath, onvalue=1, offvalue=0, command=path_selection)
d2 = ttk.Checkbutton(dir_scan_container, text='programfiles ('+os.environ["ProgramFiles"]+')', variable=var_programfiles, onvalue=1, offvalue=0, command=path_selection)
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

browse_file_button = ttk.Button(dir_scan_container, text='...', command=selectDir) #按下按鈕執行 selectDir 這個 function 
browse_file_button.place(x = 210, y = 85, width=20, height=20)

# Options 進階選擇 ----- ttk.Radiobutton
var_option = tk.IntVar(value=1)
o1 = ttk.Radiobutton(options_container, text='一般掃描', variable=var_option, value='1', command=option_selection)
o2 = ttk.Radiobutton(options_container, text='深度掃描', variable=var_option, value='2', command=option_selection)
o1.grid(column=0, row=9, sticky=tk.W)
o2.grid(column=0, row=10, sticky=tk.W)

# 執行按鈕 ----- ttk.Button
button = ttk.Button(root, text='開始掃描', command=parseFile) #按下按鈕執行parseFile這個function 
button.grid(column=0, row=11, sticky=tk.E, padx=5, pady=5)

# 進度條 ----- ttk.Progressbar
# progress_bar = ttk.Progressbar(root, orient='horizontal', length=150, mode='determinate')  #mode:定量(determinate)不定量(indeterminate)
# progress_bar.grid(column=0, row=11, sticky=tk.W, padx=5, pady=5)

root.mainloop() #讓程式推入與使用者互動模式
