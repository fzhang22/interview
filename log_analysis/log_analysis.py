#!/usr/bin/env python
# coding: utf-8

# 

# In[277]:


import pandas as pd
import json

def log_analysis():
    """超级简历笔试题分析log日志"""
    
    path = "last-1000-log" # 文件路径 + 文件名
    log_data = open(path,'r') # 打开日志文件
    
    # 对日志中的每个部分都新建一个list
    col_IP = []
    col_date = []
    col_request = []
    col_url = []
    col_httpVersion = []
    col_returnCode = []
    col_responseLength = []
    col_referer = []
    col_agent = []
    col_ifHIT = []
    
    # 对日志中的每条记录执行如下操作
    for line in log_data:
        # 提取IP,并将其append到IPlist中
        temp = line.split("- -")
        IP = temp[0].strip()
        col_IP.append(IP) 
        
        # 提取日期，并将其append到日期list中
        date = temp[1].split("  ")[0].strip()
        col_date.append(date)
        
        # 提取request方式，并将其append到request方式list中
        temp = temp[1].split("  ")[1].split(" ")
        get_or_Post = temp[0]
        col_request.append(get_or_Post)
        
        # 提取url， 并将其append到url list中
        url = temp[1]
        col_url.append(url)
        
        # 提取http版本，并将其append到http版本list中
        http_version = temp[2]
        col_httpVersion.append(http_version)
        
        # 提取返回码，并将返回码append到返回码list中
        return_code = temp[3]
        col_returnCode.append(return_code)
        
        # 提取response长度， 并将其append到response长度list中
        response_length = temp[4]
        col_responseLength.append(response_length)

        # 提取referer，由于第一行数据的referer比别的行多出了一个index的长度，因此需要将多出
        # 的index的长度跟原先的长度合并，合并之后再append到referer的list中
        referer = [temp[5] if temp[6] != '"com.zhihu.android/Futureve/5.42.0'                    else "".join(ele for ele in temp[5:7]).replace('""',"")]
        col_referer.append(referer)
        
        # 同理，由于第一行数据与其他行数据长度不一致，需分开判断做合并操作，合并之后再获得user_agent的数据
        # 然后再讲user_agent的数据append到list中
        if (temp[7] == 'Mozilla/5.0'):
            temp[7: -1] = ["".join(temp[7: -1])]
            user_agent = temp[7]
            col_agent.append(user_agent)
        else:
            temp[6: -1] = ["".join(temp[6: -1])]
            user_agent = temp[6]
            col_agent.append(user_agent)
        
        # 如果文本显示HIT，则append”HIT“，否则为“MISS”
        if temp[-1] == 'HIT\n':
            col_ifHIT.append("HIT")
        else:
            col_ifHIT.append("MISS")
    
    # 创建一个字典，将所有的list添加进来，key的名称与文档说明保持一致
    d = {"IP": col_IP,"日期": col_date, "Request方式": col_request,"url": col_url, "http版本": col_httpVersion,
        "返回码": col_returnCode, "reponse长度": col_responseLength, "referer": col_referer, 
         "user_agent": col_agent, "缓存是否命中": col_ifHIT}
    
    # 根据字典创建DataFrame
    df = pd.DataFrame(d)


    # 请分析附件中：
    # Q1. 合计多少次访问
    # 答： 访问的次数即是Request的次数，也是DataFrame的行数, 因此计算行数得知是1000次
    count_row = df.shape[0]
    print("Q1: 合计一共" + str(count_row) + "次访问 \n")

    # Q2. GET, POST, DELETE各是多少次
    # 答：对”Request的方式“ 该列分别计算GET, POST, DELETE的次数
    print("Q2: 从下表得知，GET共778次，POST共209次，DELETE共12次")
    print(df.groupby("Request方式").size())
    print("\n")

    # Q3.多少个独⽴IP。
    # 答：在“IP”列计算唯一值
    unique_ip = df["IP"].nunique(dropna = True)
    print("Q3: 独立IP一共" + str(unique_ip) + "个 \n")

    # Q4.每个IP出现了多少次
    # 答：计算每个独立IP的次数
    IP_occurrences = df["IP"].value_counts(dropna = True)
    print("Q4: 每个IP出现的次数如下表所示:")
    print(IP_occurrences)
    print("\n")

    # 5. 如果不考虑URL的参数（也就是URL中?和后⾯的部分都不考虑)的话，都出现过哪些URL，每个URL出现多少次？
    # 答：先移除掉问号后面的部分，然后对简化后的url计算次数并按照计算次数从高到低排列
    remove_qsmark = [url.split("?")[0] if "?" in url else url for url in df["url"]]
    df_result = pd.DataFrame(remove_qsmark, columns = ["简化后的url"])
    print("Q5: 不考虑参数的URL的出现次数由高到低排列如下:")
    print(df_result["简化后的url"].value_counts())


# Call the function
if __name__ == "__main__":
    log_analysis()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




