import numpy as np
import os
import glob
import pandas as pd
import re

import numpy as np
from itertools import product

current_dir=os.path.dirname(os.path.abspath(__file__))
# この関数をもっと理解する
#それかこの前のexample.py使う
def nearest(a, b):
    na, nb = len(a), len(b)
    ## Combinations of a and b
    comb = product(range(na), range(nb))
    ## [[distance, index number(a), index number(b)], ... ]
    l = [[np.linalg.norm(a[ia] - b[ib]), ia, ib] for ia, ib in comb]
    ## Sort with distance
    l.sort(key=lambda x: x[0])
    print(l)

    xa = []
    xb = []
    d = []
    for _ in range(min(na, nb)):
        m, ia, ib = l[0]
        xa.append(ia) # 元データ配列からの削除用に追加
        xb.append(ib) # 同じ
        d.append([m, a[ia], b[ib]])  # 最短結果通知用に格納
        ## Remove items with same index number
        l = list(filter(lambda x: x[1] != ia and x[2] != ib, l))
        
    a = np.delete(a, xa, 0) # 元データ配列からデータ削除
    b = np.delete(b, xb, 0) # 同じ
    d.append(l) 
    if len(a) != 0:
        for i in a :
            left = [0,i,np.array([0,0])]
            print(left)
            d.append (left) 
    # if len(b) != 0:
    #     print(b)
    #     for i in b :
    #         #left = [0,[0,0],i.tolist()]
    #         left = [0,np.array([0,0]),i]
    #         d.append (left) 
    df = pd.DataFrame(d)
    df.columns=["distance", "before", "after"]

    # if len(a) != 0:
    #     df_left = pd.DataFrame(a)
    #     df_left.columns=["left_x", "top_y"]
        
    # if len(b) != 0:
    #     df_left = pd.DataFrame(b)
    #     df_left.columns=["left_x", "top_y"]
        
    return df

#yoloは二つで検出される時がある

def compare_two(num1, num2):
    df1=pd.read_csv(os.path.join(current_dir,'1', ''+num1+'.csv'))
    df2=pd.read_csv(os.path.join(current_dir,'1', ''+num2+'.csv'))
    #ここで重複したBoundingBoxをProbabilityの大きい方のみにする
    df2 = df2.sort_values('probability')
    df2 = df2.drop_duplicates(subset=['left_x','top_y'], keep='last')
    df2=df2.reset_index()
    l1 = df1[['left_x','top_y']].as_matrix()
    l2 = df2[['left_x','top_y']].as_matrix()
    df_result= nearest(l1,l2)
    df_result =pd.concat([df_result["distance"],df_result["before"].apply(pd.Series),df_result["after"].apply(pd.Series)], axis = 1)
    df_result.columns=['distance_'+num1+'_'+num2+'', 'x_'+num1+'', 'y_'+num1+'','x_'+num2+'','y_'+num2+'']
    category_num1= df1[['left_x','top_y','class']]
    category_num1.columns=['x_'+num1+'', 'y_'+num1+'','class_'+num1+'']
    df_result=pd.merge(df_result, category_num1, on=['x_'+num1+'', 'y_'+num1+''],how='right')
    category_num2= df2[['left_x','top_y','class']]
    category_num2.columns=['x_'+num2+'', 'y_'+num2+'','class_'+num2+'']
    df_result=pd.merge(df_result, category_num2, on=['x_'+num2+'', 'y_'+num2+''],how='right')
    return df_result

print(compare_two('06','07'))