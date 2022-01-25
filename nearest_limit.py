import numpy as np
import os
import glob
import pandas as pd
import re

import numpy as np
from itertools import product



current_dir=os.path.dirname(os.path.abspath(__file__))
# 最近傍のBounding Boxの組み合わせを記したDataFrameを返す
def nearest(a, b):
    d=[]
    while (len(a) > 0) and (len(b) > 0):
        out_min = 999999999999999.9
        out_res = []
        for i in a:
            min = np.linalg.norm(i - b[0])
            result = [min, i, b[0]]  
            for j in b:
                c = np.linalg.norm(i - j)
                if min > c:
                    min = c
                    result = [min, i.tolist(), j.tolist()]  
                else:
                    pass

            if out_min > min:
                out_min = min
                out_res = result

        a = np.delete(a, np.where(a[:] == out_res[1])[0], 0)
        b = np.delete(b, np.where(b[:] == out_res[2])[0], 0)
        d.append(out_res) 
    
    #組み合わせに入らなかったものもdfに書き加える。距離が0であるからここ直す。
    # if len(a) != 0:
    #     for i in a :
    #         left = [0,i.tolist(),[0,0]]
    #         d.append (left) 
    # if len(b) != 0:
    #     for i in b :
    #         left = [0,[0,0],i.tolist()]
    #         d.append (left) 
        df = pd.DataFrame(d)
        df.columns=["distance", "before", "after"]
    return  df

# 2つを比べる
def compare_two(num1, num2):
    df1=pd.read_csv(os.path.join(current_dir,'1', ''+num1+'.csv'))
    df2=pd.read_csv(os.path.join(current_dir,'1', ''+num2+'.csv'))
    print(len(df1))
    print(len(df2))
    l1 = df1[['left_x','top_y']].as_matrix()
    l2 = df2[['left_x','top_y']].as_matrix()
    df_result= nearest(l1,l2)
    df_result =pd.concat([df_result["distance"],df_result["before"].apply(pd.Series),df_result["after"].apply(pd.Series)], axis = 1)
    df_result.columns=['distance_'+num1+'_'+num2+'', 'x_'+num1+'', 'y_'+num1+'','x_'+num2+'','y_'+num2+'']
    category_num1= df1[['left_x','top_y','class']]
    category_num1.columns=['x_'+num1+'', 'y_'+num1+'','class_'+num1+'']
    df_result=pd.merge(df_result, category_num1, on=['x_'+num1+'', 'y_'+num1+''])
    category_num2= df2[['left_x','top_y','class']]
    category_num2.columns=['x_'+num2+'', 'y_'+num2+'','class_'+num2+'']
    df_result=pd.merge(df_result, category_num2, on=['x_'+num2+'', 'y_'+num2+''])
    return df_result

print(compare_two('05','06'))
print(len(compare_two('05','06')))
#上限値を定める
#ここで距離30以上の組み合わせだった場合、組み合わせを解除する。
def compare_two_complete(num1, num2):
    df1 = compare_two(num1,num2)
    df1A = df1[df1['distance_'+num1+'_'+num2+''] < 30]
    df1B = df1[df1['distance_'+num1+'_'+num2+''] >= 30]
    offset = len(df1B)
    df1B = df1B.append([np.nan for x in range(offset)])
    df1B['x_'+num2+''] = df1B['x_'+num2+''].shift(periods=offset)
    df1B['y_'+num2+''] = df1B['y_'+num2+''].shift(periods=offset)
    df1B['class_'+num2+''] = df1B['class_'+num2+''].shift(periods=offset)
    df1B['distance_'+num1+'_'+num2+''] = 0
 
    #df1B = df1B['x_'+num1+'','y_'+num1+'','x_'+num2+'','y_'+num2+''].fillna(0)
    df_concat = pd.concat([df1A, df1B], join='inner')
    df_concat=df_concat.drop_duplicates()
    return df_concat

#print(compare_two('05','06'))
#print(compare_two_complete('08','09'))

def compare_many(list):
    #最初の2つを繋げておく
    df_result = compare_two_complete(list[0],list[1])
    #繋げていく
    for index in range(len(list)-2):
        # 5~9日だった場合、ここで6日と7日
        df = compare_two_complete(list[index+1],list[index+2])
        df_result = pd.merge(df_result,df, on=['x_'+list[index+1]+'','y_'+list[index+1]+''], how='outer')
    df_result.to_csv(os.path.join(current_dir,'1','compare4.csv'),encoding='utf_8',index=False)
    return df_result

list = ["05","06","07","08","09"]
#compare_many(list)

# #特定の値で
# df1 = compare_two("05.csv","06.csv")
# df1=pd.concat([df1["distance"],df1["before"].apply(pd.Series),df1["after"].apply(pd.Series)], axis = 1)
# df1.columns=["distance_05_06", "x_05", "y_05","x_06","y_06"]

# df1A = df1[df1['distance_05_06'] < 30]
# df1B = df1[df1['distance_05_06'] >= 30]
# offset = 3
# df1B = df1B.append([np.nan for x in range(offset)])
# df1B["x_06"] = df1B["x_06"].shift(periods=offset)
# df1B["y_06"] = df1B["y_06"].shift(periods=offset)
# df1B['distance_05_06'] = 0
# df1B = df1B.fillna(0)
# df_concat = pd.concat([df1A, df1B], join='inner')
# print(df_concat)


# df2 = compare_two("06.csv","07.csv")
# df2=pd.concat([df2["distance"],df2["before"].apply(pd.Series),df2["after"].apply(pd.Series)], axis = 1)
# df2.columns=["distance_06_07", "x_06", "y_06","x_07","y_07"]
#df_result = pd.merge(df1,df2, left_on=['x_06','y_06'], right_on=['x_06','y_06'], how='outer')
#print(df_result)




