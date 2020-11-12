
# coding: utf-8

# In[1]:


import pandas as pd

df = pd.DataFrame({'month': [1, 4, 7, 10],
                   'year': [2012, 2014, 2013, 2014],
                   'sale': [55, 40, 84, 31]})


# In[2]:


df


# In[3]:


df2 = df.set_index(['year', 'month'])


# In[4]:


df2


# In[5]:


df2.reset_index(level=['month', 'year'])


# In[6]:


df = pd.DataFrame({'foo': ['one', 'one', 'one', 'two', 'two',
                            'two'],
                    'bar': ['A', 'B', 'C', 'A', 'B', 'C'],
                    'baz': [1, 2, 3, 4, 5, 6],
                    'zoo': ['x', 'y', 'z', 'q', 'w', 't']})


# In[8]:


df


# In[7]:


df.pivot(index='foo', columns='bar')


# In[9]:


df = pd.DataFrame({"A": ["foo", "foo", "foo", "foo", "foo",
                          "bar", "bar", "bar", "bar"],
                    "B": ["one", "one", "one", "two", "two",
                          "one", "one", "two", "two"],
                    "C": ["small", "large", "large", "small",
                          "small", "large", "small", "small",
                          "large"],
                    "D": [1, 2, 2, 3, 3, 4, 5, 6, 7]})


# In[10]:


df


# In[11]:


from collections import defaultdict

df['E'] = df[['C', 'D']].apply(lambda x: {x[0]:[x[1]]}, axis=1)


# In[12]:


df


# In[13]:


sectors = df.groupby(['A', 'B'])


# In[14]:


sectors.groups.keys()


# In[15]:


sectors.get_group(('bar', 'one'))


# In[17]:


from functools import reduce

def merge(x, y):
    print(x)
    print(y)
    if isinstance(x, dict):
        for key in y.keys():
            if key in x.keys():
                x.update({key:x[key] + y[key]})
            else:
                x.update({key:y[key]})
    return x
    
    

pd.pivot_table(df, index=['A', 'B'], values=['E'], aggfunc=lambda x: reduce(merge, x))


# In[18]:


sectors.agg(lambda x: reduce(merge, x))


# In[19]:


x = {
    "生理反應(生理)_1": "我只是失眠者隨",
    "負向(情緒)_1": "過早國中談戀愛，失戀了，感覺到痛苦萬分",
    "自殺行為(行為)_1": "對國中的我來說，可能壓抑不過去。\n這是我失去理智自殘的第一次。也是第N次",
    "自殺與憂鬱(認知)_1": "中間戀愛發生戀愛過程導致憂鬱",
    "自殺行為(行為)_2": "我從未帶到至學校自殘過\n只是在家偷偷的劃著",
    "自殺與憂鬱(認知)_2": "我怠惰了，我也墮落了\n我也還不明白自己怎麼了",
    "自殺行為(行為)_3": "今年\n我將自己壓抑到一個極限",
    "自殺與憂鬱(認知)_3": "工作要求太完美，學業要求太細節\n我感覺什麼事情都做不好辦不到",
    "負向(情緒)_2": "重點是男友也不懂我為何每日低落",
    "自殺與憂鬱(認知)_4": "我曾經跟他詢問說我好像可能憂鬱症嗎？我想看個醫生，他只覺得我想太多",
    "自殺行為(行為)_4": "一直到我計畫很久了老樣子\n情緒崩潰\n我自殘了\n這次送了救護車到醫院",
    "生理反應(生理)_2": "在我的夢裡不斷做惡夢",
    "正向理由(認知)_1": "我不想跳樓，砸到車要賠\n我不想燒炭，會變凶宅",
    "負向(情緒)_3": "老樣子\n情緒崩潰",
    "自殺行為(行為)_5": "我第一次接受身心科的問診\n也第一次直接被派發到病床",
    "自殺行為(行為)_8": "畫面很血腥，手臂內外共縫了20幾針，必須送醫院\n最後因為割到肌鍵所以打石膏一個月",
    "自殺行為(行為)_7": "我沒有把照片.生病發給身邊任何平台\n所以朋友都不知道這些事，我都是蓋護腕",
    "自殺與憂鬱(認知)_5": "一直到現在我可能都還沒認清憂鬱的事實",
    "自殺行為(行為)_6": "鼓起勇氣\n看了幾次的醫生",
    "負向(情緒)_4": "雖然每次都爆哭"
}


# In[20]:


pd.DataFrame.from_dict(x, orient='index').stack()


# In[23]:


pd.DataFrame.from_dict(x, orient='index')


# In[27]:


pd.DataFrame.from_dict(x, orient='columns')


# In[21]:


def add(x, y) :
    print('debug')
    print(type(y))
    return x + y
 
reduce(add, [1]) 


# In[22]:


reduce(add, [1,2]) 

