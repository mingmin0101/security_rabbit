from __future__ import absolute_import, unicode_literals
from celery import shared_task

import os
from django.conf import settings

from data.models import Computer, ScanningRecord, FileInfo
from users.models import User

import numpy as np
import pandas as pd
import Orange
import pickle
import csv
from io import StringIO
from collections import OrderedDict
from Orange.data import Table, Domain, ContinuousVariable, DiscreteVariable

import datetime
import json
from sqlalchemy import create_engine

resourceDir = os.path.join(settings.MEDIA_ROOT,"documents")

# orange
def pandas_to_orange(df):
    domain, attributes, metas = construct_domain(df)
    orange_table = Orange.data.Table.from_numpy(domain = domain, X = df[attributes].values, Y = None, metas = df[metas].values, W = None)
    return orange_table

def construct_domain(df):
    columns = OrderedDict(df.dtypes)
    attributes = OrderedDict()
    metas = OrderedDict()
    for name, dtype in columns.items():

        if issubclass(dtype.type, np.number):
            if len(df[name].unique()) >= 13 or issubclass(dtype.type, np.inexact) or (df[name].max() > len(df[name].unique())):
                attributes[name] = Orange.data.ContinuousVariable(name)
            else:
                df[name] = df[name].astype(str)
                attributes[name] = Orange.data.DiscreteVariable(name, values = sorted(df[name].unique().tolist()))
        else:
            metas[name] = Orange.data.StringVariable(name)

    domain = Orange.data.Domain(attributes = attributes.values(), metas = metas.values())

    return domain, list(attributes.keys()), list(metas.keys())
#--------------------------------------------

@shared_task
def calculate_score(userid, deviceuuid):
    calculate_start_time = datetime.datetime.now()
    filepath = os.path.join(resourceDir, "exeinfo_" + str(userid) + "_" + deviceuuid + ".json")
    
    # reading the JSON data using json.load()
    with open(filepath) as file:
        json_dict = json.load(file)   

    # converting json dataset from dictionary to dataframe
    json_dict["hostinfo"]["registry_list"] = str(json_dict["hostinfo"]["registry_list"])
    host_df = pd.DataFrame(json_dict["hostinfo"],index=[0])
    file_df = pd.read_json(json_dict["fileinfo"]) #pd.read_json
    meta_df = pd.DataFrame(json_dict["metainfo"],index=[0])

    orange_dt = pandas_to_orange(file_df)
    with open(os.path.join(settings.MEDIA_ROOT,"model","tree.pkcls"), "rb") as f:   # tree.pkcls
        model = pickle.load(f)

    data = Orange.data.Table(orange_dt)  # "test_data_bad.xlsx"
    pred_ind = model(data)  # array of predicted target values (indices)
    li = [model.domain.class_var.str_val(i) for i in pred_ind]  # convert to value names (strings)
    prob = model(data, model.Probs)  # array of predicted probabilities
    prob_li=[(round(prob[i][1]*100)/10) for i in range (len(prob))]
    # print(prob_li)
    file_df["score"] = prob_li
    print(file_df["score"])
    file_df_filter = file_df.copy()
    #file_df_filter = file_df.filter(["score","AddressOfEntryPoint", "Characteristics", "signers", "counter_signers", "Export_directories", "Import_directories", "Machine", "NumberOfSections", "Section_info", "TimeDateStamp", "created", "entropy", "exec_ability", "exec_ability_dic", "file_attribute", "file_name", "file_sha1", "file_size", "last_accessed", "last_modified", "network_ability", "network_ability_dic", "pack", "rw_ability", "rw_ability_dic", "sigcheck_Company", "sigcheck_Description", "sigcheck_File version", "sigcheck_Link date", "sigcheck_MachineType", "sigcheck_Prod version", "sigcheck_Product", "sigcheck_Verified"], axis=1)
    #"signers",
    calculate_end_time = datetime.datetime.now()
    
    # 存Computer電腦資訊  如果沒有全部資訊都有會跑錯!
    if Computer.objects.filter(administrator=User.objects.get(id=userid)).filter(deviceUuid=deviceuuid).exists():
        # computer = Computer.objects.filter(administrator=User.objects.get(id=userid)).filter(deviceUuid=deviceuuid)
        # computer.update(deviceName=host_df["deviceName"],userName=host_df["userName"],ipAddr=host_df["ipAddr"],macAddr=host_df["macAddr"],os=host_df["os"],processor=host_df["processor"],cpu=host_df["cpu"],memoryCapacity=host_df["memoryCapacity"],registry_StartupCommand=host_df["registry_list"],latest_scan_score=int(round(mean(prob_li))))
        Computer.objects.filter(administrator=User.objects.get(id=userid)).filter(deviceUuid=deviceuuid).update(latest_scan_score=int(round(np.mean(prob_li))))
    else:
        Computer.objects.create(administrator=User.objects.get(id=userid),deviceUuid=deviceuuid,deviceName=host_df["deviceName"],userName=host_df["userName"],ipAddr=host_df["ipAddr"],macAddr=host_df["macAddr"],os=host_df["os"],processor=host_df["processor"],cpu=host_df["cpu"],memoryCapacity=host_df["memoryCapacity"],registry_StartupCommand=host_df["registry_list"],latest_scan_score=int(round(np.mean(prob_li))))

    # 存scanRecord掃描紀錄資訊   掃描選項待討論!
    if(meta_df['scan_type'][0] == "0"): 
        normal_option = True
        advance_option = False
        customized_option = False 
    elif(meta_df['scan_type'][0] == "1"):  
        normal_option = False
        advance_option = True
        customized_option = False
    else: 
        normal_option = False
        advance_option = False
        customized_option = True
    
    ScanningRecord.objects.create(start_time=str(json_dict["metainfo"]["start_time"]), end_time=calculate_end_time, normal_option=normal_option, advance_option=advance_option, customized_option=customized_option, score=int(round(np.mean(prob_li))), computer=Computer.objects.filter(administrator=User.objects.get(id=userid)).get(deviceUuid=deviceuuid))

    file_df_filter.file_name = file_df_filter.file_name.astype(str)
    file_df_filter.created = file_df_filter.created.astype(str)
    file_df_filter.last_modified = file_df_filter.last_modified.astype(str)
    file_df_filter.last_accessed = file_df_filter.last_accessed.astype(str)
    file_df_filter.signers = file_df_filter.signers.astype(str)
    file_df_filter.counter_signers = file_df_filter.counter_signers.astype(str)
    file_df_filter.network_ability_dic = file_df_filter.network_ability_dic.astype(str)
    file_df_filter.rw_ability_dic = file_df_filter.rw_ability_dic.astype(str)
    file_df_filter.exec_ability_dic = file_df_filter.exec_ability_dic.astype(str)
    file_df_filter.pack = file_df_filter.pack.astype(str)
    file_df_filter.Section_info = file_df_filter.Section_info.astype(str)
    file_df_filter.Import_directories = file_df_filter.Import_directories.astype(str)
    file_df_filter.Export_directories = file_df_filter.Export_directories.astype(str)
    # file_df_filter.printable_strs = file_df_filter.printable_strs.astype(str)
    file_df_filter.file_sha1 = file_df_filter.file_sha1.astype(str)

    # 存fileinfo檔案掃描紀錄
    file_df_filter["scanningRecord_id"] = ScanningRecord.objects.filter(computer=Computer.objects.filter(administrator=User.objects.get(id=userid)).get(deviceUuid=deviceuuid)).latest("start_time")
    #file_df_filter.rename(columns={"signers":"signer", "counter_signers":"counter_signer","file_sha1":"file_hash_sha1","Machine":"pe_machine","NumberOfSections":"pe_sectionNum","TimeDateStamp":"pe_timeDateStamp ","Characteristics":"pe_characteristics","AddressOfEntryPoint":"pe_entryPoint","Section_info":"pe_sections","Import_directories":"pe_imports","Export_directories":"pe_exports","pack":"peutils_packed","file_name":"file_path","created":"create_time","last_modified":"modified_time","last_accessed":"accessed_time","sigcheck_Verified":"signature_verification","sigcheck_Company":"company","sigcheck_Description":"description","sigcheck_File version":"file_version","sigcheck_Link date":"link_date","sigcheck_MachineType":"machine_type","sigcheck_Prod version":"prod_version","sigcheck_Product":"product"}, inplace=True)
    #"signers":"signer",
    #df.column_name = df.column_name.astype(str)
    #file_df_filter.to_string(columns=["signer","counter_signer","pe_sections","pe_imports","pe_exports","peutils_packed"])
    #print(FileInfo._meta.get_fields())
    saveData(file_df_filter)
    
    # 刪除上傳的json檔
    # os.remove(filepath)

    return "analysis task finished!"

# def saveData(df): #, dtypedict
#     # https://codeday.me/bug/20190206/621744.html
#     # user = settings.DATABASES["default"]["USER"]
#     # password = settings.DATABASES["default"]["PASSWORD"]
#     database_name = settings.DATABASES["default"]["NAME"]

#     database_url = "sqlite:///{database_name}".format(
#         # user=user,
#         # password=password,
#         database_name=database_name,
#     )

#     engine = create_engine(database_url, echo=False)
#     # engine = create_engine(settings.DATABASES["default"]["ENGINE"], echo=False)
#     pd.io.sql.to_sql(df, "FileInfo", con=engine, if_exists = "append", index=False)  # dtype=dtypedict

def saveData(df):
    # Not able to iterate directly over the DataFrame
    df_records = df.to_dict('records')  # 'series'

    model_instances = [FileInfo(
            file_path = record['file_name'],
            file_hash_sha1 = record['file_sha1'],
            file_size = record['file_size'],
            
            peutils_packed = record['pack'],
            entropy = record['entropy'],
            
            create_time = record['created'],
            modified_time = record['last_modified'],
            accessed_time = record['last_accessed'],
            
            company = record['Company'],
            description = record['Description'],
            product = record['Product'],
            prod_version = record['Prod version'],
            file_version = record['File version'],
            machine_type = record['MachineType'],

            signature_verification = record['Verified'],
            link_date = record['Link date'],
            signing_date = record['Signing date'],

            signer = record['signers'],
            counter_signer = record['counter_signers'],
            
            pe_machine = record['Machine'],
            pe_sectionNum = record['NumberOfSections'],
            pe_timeDateStamp = record['TimeDateStamp'],
            pe_characteristics = record['Characteristics'],
            pe_entryPoint = record['AddressOfEntryPoint'],
            
            pe_sections = record['Section_info'],
            pe_imports = record['Import_directories'],
            pe_exports = record['Export_directories'],
            
            network_ability = record['network_ability'],
            rw_ability = record['rw_ability'],
            exec_ability = record['exec_ability'],
            
            score = record['score'],
            scanningRecord_id = record['scanningRecord_id'],


    ) for record in df_records]
            
    #FileInfo.objects.bulk_create(model_instances)
    for r in model_instances:
        r.save()
    #FileInfo.objects.create(**df_records)