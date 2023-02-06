
# coding: utf-8

# # 工研院json轉excel

# ## 讀取標註檔案

# In[1]:


import pandas as pd

# filepath = './A1_labeled.json'
filepath = '工研院標註檔案_test.json'
# filepath = '完整_二次標註_1091014.json'

df0 = pd.read_json(filepath)
df0


# ## 輸出excel

# In[2]:


import sys
sys.path.append("..")
from DataTag_helper import to_excel_AI_clerk_labeled_data

# filepath2 = './A1_labeled.xlsx'
filepath2 = './工研院標註檔案_test_labeled.xlsx'
# filepath2 = './完整_二次標註_1091014_labeled.xlsx'

df_content, df_document_label, df_sentence_label, df_sentence_label_wide, df_doc_label_cmp, df_sent_label_cmp_long, df_sent_label_cmp_wide, df_sent_doc_cmp = to_excel_AI_clerk_labeled_data(df0, filepath2)


# In[3]:


df_content


# In[4]:


df_document_label


# In[5]:


df_sentence_label


# In[6]:


df_document_label[pd.isnull(df_document_label['Crisis_Level'])]


# In[7]:


df_sentence_label[pd.isnull(df_sentence_label['Crisis_Level'])]


# In[91]:


df1 = pd.read_excel('A1.xlsx')


# In[102]:


df1[df1['Title'] == '好累卻不能說…甚至不了解自己']['Content'].iloc[0]


# In[93]:


df2 = pd.read_excel('NEW上傳_440_二次標註檔案_1090903_emojilized.xlsx')


# In[103]:


df2[df2['Title'] == '好累卻不能說…甚至不了解自己']['Content'].iloc[0]


# In[8]:


df3 = pd.read_excel('NEW上傳_440_二次標註檔案_1090903_TextID_mapping.xlsx')
df3


# In[104]:


df_A1 = pd.read_excel('A1_TextID_mapping.xlsx')


# In[105]:


df_A2 = pd.read_excel('A2_TextID_mapping.xlsx')


# In[106]:


df_all = pd.concat([df_A1, df_A2], axis=0)


# In[107]:


df_all


# In[117]:


df_sec = pd.read_excel('NEW上傳_440_二次標註檔案_1090903_TextID_mapping.xlsx')


# In[118]:


df_not_same = df_sec[~(df_sec['TextID(processed)'].isin(df_all['TextID(processed)']))]


# In[119]:


df_content[df_content['TextID'].isin(df_not_same['TextID'])]


# In[114]:


import re
pattern2 = re.compile(u'\\\\\\\\%')


# In[116]:


pattern2.sub('%', u'還不是@#$\\\\%\\\\%…\n\n容易')


# In[9]:


if all(df_content['TextID'].isin(df3['TextID'])):
    df4 = pd.merge(df3, df_content, how='right', on=['TextID'])
    display(df4)
else:
    print('false')


# In[10]:


df4_tmp = df4[~(df4['TextID(emojilized)'] == df4['TextID'])]
df4_tmp


# In[11]:


df4[~(df4['TextID(remove_illegal_characters)'] == df4['TextID'])]


# In[12]:


df4[~(df4['TextID(deemojilized)'] == df4['TextID'])]


# In[13]:


df5 = pd.read_excel('all_data.xlsx')
df5


# In[14]:


df4_tmp[~df4_tmp['TextID(emojilized)'].isin(df5['TextID'])]


# In[46]:


df1 = pd.read_excel('A2.xlsx')


# In[47]:


import hashlib



text1 = df1[df1['Title'] == '⚠️（最後一更）我被家暴了']['Content'].iloc[0]
print(hashlib.md5(text1.encode('utf-8')).hexdigest()[:10])
text1


# In[31]:


df2[df2['TextID'] == '76c492c986']


# In[48]:


df2 = pd.read_excel('NEW上傳_440_二次標註檔案_1090903_emojilized.xlsx')


# In[49]:


text2 = df2[df2['Title'] == '⚠️（最後一更）我被家暴了']['Content'].iloc[0]
print(hashlib.md5(text2.encode('utf-8')).hexdigest()[:10])
text2


# In[52]:


import difflib

case_a = 'afrykbnerskojęzyczny'
case_b = 'afrykanerskojęzycznym'

output_list = [li for li in difflib.ndiff(case_a, case_b) if li[0] != ' ']


# In[53]:


output_list


# In[66]:


[li for li in difflib.ndiff(text1, text2)][17:20]


# In[70]:


text1[17:20].encode('unicode-escape')


# In[213]:


text1[13:15].encode('unicode-escape')


# In[117]:


b'  \\u2764'.decode('unicode-escape')


# In[19]:


'◀️'.encode('unicode-escape')


# In[116]:


u'\U0001F1FF'


# In[189]:


difflib.ndiff(text1, text2)


# In[211]:


u'\uFE0F'.encode('unicode-escape')


# In[217]:


[li for li in difflib.ndiff(text1, text2)]


# In[1]:


import emoji

emoji.emojize('\n:angry_face_with_horns:\n', variant="emoji_type").encode('unicode-escape')


# In[132]:


'♀'.encode('unicode-escape')


# In[121]:


import re

with open("emoji-variation-sequences.txt", "r") as text_file:
#     print(text_file.read())
    text = text_file.read()

new_text = re.sub('#.*[\n]', '', text)
new_text2 = re.sub('(text|emoji) style;', '', new_text)
new_text3 = re.sub('\s*(FE0E\s*|FE0F\s*)', '', new_text2)
text4 = re.split(';\s*', new_text3)
newlist = list(dict.fromkeys(text4))[:-1]

# newlist

newlist2 = [('\\u' + code).encode('utf8').decode('unicode-escape') for code in newlist]
newlist2


# In[120]:


newlist2[0].decode('unicode-escape')


# In[103]:


'\u000'.decode('unicode')


# In[146]:


string = u'\U0001F926\U0000200D\U00002640'.encode('unicode-escape').decode('utf8')


# In[164]:


('\\' + string.split('\\')[-1]).encode('utf8').decode('unicode-escape')


# In[8]:


for i in newlist2:
    print('{}, '.format(i))


# In[65]:


type(newlist[0])


# In[67]:


'\\U000'


# In[42]:


with open("emoji-variation-sequences.txt", "r") as text_file:
#     print(text_file.read())
    text = text_file.read()


# In[43]:


print(text)


# In[74]:


import re

new_text = re.sub('#.*[\n]|\n*', '', text)


# In[75]:


new_text


# In[86]:


new_text2 = re.sub('\s*(text|emoji) style;\s*', '', new_text)


# In[87]:


new_text2


# In[88]:


new_text3 = re.sub('\s*(FE0E\s*|FE0F\s*)', '', new_text2)


# In[89]:


new_text3


# In[90]:


text4 = re.split(';\s*', new_text3)


# In[91]:


text4


# In[55]:


newlist = list(dict.fromkeys(text4))


# In[58]:


newlist


# In[33]:


new_text.split(';')


# In[29]:


from pandas.compat import BytesIO

memfile = BytesIO()

memfile.write(new_text.encode('utf8'))


# In[26]:


with open(memfile, "w") as text_file:
#     print(text_file.read())
    text_file.write('{}'.format(new_text))


# In[31]:


pd.read_csv(memfile)

