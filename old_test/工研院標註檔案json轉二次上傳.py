
# coding: utf-8

# # 工研院標註檔案json轉二次上傳

# ## 讀取標註檔案

# In[5]:


import pandas as pd
import json
from pprint import pprint

# filepath = './A1_labeled.json'
filepath = '工研院標註檔案_test.json'
# filepath = '完整_二次標註_1091014.json'

# df0 = pd.read_json(filepath)
# df0

with open(filepath) as f:
    data = json.load(f)

pprint(data)


# In[8]:


data2 = {}

for key, value in data.items():
    pprint(data[key])
    data2.update({data[key]['TextID']: data[key]})

    print("-----------")


# In[9]:


pprint(data2)


# In[10]:


save_path = '工研院標註檔案_test_second_upload.json'

with open(save_path, 'w', encoding='utf-8') as outfile:
    json.dump(data2, outfile, ensure_ascii=False, indent=4)


# ## 輸出二次上傳json

# In[14]:


get_ipython().system('python ../DataTag_helper.py second_upload -i ./工研院標註檔案_test.json')

