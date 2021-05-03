
# coding: utf-8

# # 工研院二次標註檔案json清理轉換

# ## 讀取標註檔案

# In[3]:


import pandas as pd
import json
from pprint import pprint
from pathlib import Path

# filepath = './A1_labeled.json'
# filepath = '工研院標註檔案_test.json'
# filepath = '完整_二次標註_1091014.json'

# df0 = pd.read_json(filepath)
# df0

# with open(filepath) as f:
#     data = json.load(f)
    
common_filename_1 = Path('./二次標註轉換測試/正式標註第(221條第1項)_1100331下載.json')
common_filename_2 = Path('./二次標註轉換測試/二次確認(第221條第1項)_1100429下午十五時下載.json')

# df = pd.read_json(args.input_file)
with open(common_filename_1) as f:
    data1 = json.load(f)

with open(common_filename_2) as f:
    data2 = json.load(f)
    
# pprint(data1)
# pprint(data2)


# In[4]:


data3 = {}

for key, value in data2.items():
    # pprint(data[key])
    # text_id = data1[key]['TextID']

    if value['Annotator'] == '':
        continue

    value['TextID'] = data1[value['TextID']]['TextID']

    data3.update({key: value})


# In[5]:


pprint(data3)


# In[7]:


save_path = Path(common_filename_2).with_name(common_filename_2.stem + '_second_labeled').with_suffix('.json')

with open(save_path, 'w', encoding='utf-8') as outfile:
    json.dump(data3, outfile, ensure_ascii=False, indent=4)


# ## 輸出二次上傳json

# In[10]:


get_ipython().system('python ../AI_Clerk_helper.py second_labeled -i1 ./二次標註轉換測試/正式標註第\\(221條第1項\\)_1100331下載.json -i2 ./二次標註轉換測試/二次確認\\(第221條第1項\\)_1100429下午十五時下載.json')

