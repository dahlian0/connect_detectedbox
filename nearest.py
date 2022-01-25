import numpy as np
import os
import glob
import pandas as pd
import re

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
        df = pd.DataFrame(d)
        df.columns=["distance", "before", "after"]
    return  df

# 2つを比べる
def compare_two(csv1, csv2):
    df1=pd.read_csv(os.path.join(current_dir,'1', csv1))
    df2=pd.read_csv(os.path.join(current_dir,'1', csv2))
    l1 = df1[['left_x','top_y']].as_matrix()
    l2 = df2[['left_x','top_y']].as_matrix()
    df_result= nearest(l1,l2)
    df_result=pd.concat([df_result["distance"],df_result["before"].apply(pd.Series),df_result["after"].apply(pd.Series)], axis = 1)
    df_result.columns=["distance", "before_x", "before_y","after_x","after_y"]
    category= df1[['left_x','top_y','class','probability']]
    category.columns=["before_x", "before_y","class_before",'probability_before']
    df_result=pd.merge(df_result, category, on=['before_x','before_y'])
    category2= df2[['left_x','top_y','class','probability']]
    category2.columns=["after_x", "after_y","class_after",'probability_after']
    df_result=pd.merge(df_result, category2, on=['after_x','after_y'])
    #df_result.to_csv(os.path.join(current_dir,'1','compare_08_09.csv'),encoding='utf_8',index=False)
    return df_result

def comapare_many(list):
    #最初の2つを繋げておく
    # 5~9日だった場合、ここで５日と6日
    df_result = compare_two(list[0],list[1])
    #繋げていく
    for index in range(len(list)-2):
        # 5~9日だった場合、ここで6日と7日
        df = compare_two(list[index+1],list[index+2])
        print(index) ##最初の一回はsuffixがないため、分ける。ここで5~7日が繋がる
        if index == 0 :
            df_result = pd.merge(df_result,df, left_on=['after_x','after_y'], right_on=['before_x','before_y'], how='outer', suffixes=['', '_'+list[index+1]+''])
        else :
            df_result = pd.merge(df_result,df, left_on=['after_x_'+list[index]+'','after_y_'+list[index]+''], right_on=['before_x','before_y'], how='outer', suffixes=['_'+list[index]+'' , '_'+list[index+1]+''])
    df_result.to_csv(os.path.join(current_dir,'1','compare3.csv'),encoding='utf_8',index=False)
    return df_result

list = ["05.csv","06.csv","07.csv","08.csv","09.csv"]
comapare_many(list)

