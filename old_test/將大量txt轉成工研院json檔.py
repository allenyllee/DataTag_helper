
# coding: utf-8

# # 將大量txt轉成工研院json檔

# In[10]:


import hashlib
from collections import defaultdict
import json
import pandas as pd
from pathlib import Path

root_path = './gun_20201102'
common_path = Path(root_path)
print("input path:", common_path)

filename_pattern = '*/**/*.txt'
save_path = Path(common_path).with_name(Path(common_path).stem).with_suffix(".json")
print("output path:", save_path)

glob_path = Path(common_path)
filepathes=glob_path.glob(filename_pattern)

articles_dict = defaultdict(dict)

for filepath in filepathes:
    content_dict = {}
    content_dict['Title'] = filepath.stem
    content_dict['Content'] = ''
    content_dict['Author'] = ''
    content_dict['Time'] = ''

    with open(filepath, 'r', encoding='utf-8') as f:
        content_dict['Content'] = f.read()
        text_id = hashlib.md5(content_dict['Content'].encode('utf-8')).hexdigest()[:10]

    articles_dict['Articles'].update({text_id: content_dict})


# read into dataframe will automatically sort by index
dataframe = pd.DataFrame.from_dict(articles_dict)

# because articles_dict['Articles'] use text_id as key to update,
# if there were duplicate text_id, it'll replace by later items.
# so no need to check duplicate.
###
# dataframe.reset_index(inplace=True)
# dup_id = dataframe.duplicated(['index'], keep=False)
# print("duplicated entries: {}".format(len(dataframe[dup_id])))
# print(dataframe[dup_id])

# dataframe = dataframe.groupby(['index']).apply(lambda x: x.iloc[0])
# print("keep first, drop duplicated!")

# dataframe.set_index('index', inplace=True)

with open(save_path, 'w', encoding='utf-8') as outfile:
    json.dump(dataframe.to_dict(), outfile, ensure_ascii=False, indent=4)


# In[11]:


len(articles_dict['Articles'])


# ### cmdline

# In[17]:


get_ipython().system('python ../DataTag_helper.py original -d ./gun_20201102')

