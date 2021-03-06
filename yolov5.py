import numpy as np
import os
import glob
import pandas as pd
import re
# 現在のディレクトリを取得
current_dir=os.path.dirname(os.path.abspath(__file__))
# 最近傍のBounding Boxの組み合わせを記したDataFrameを返す
def nearest(a, b):
    d=[]
    while (len(a) > 0) and (len(b) > 0):
        out_min = 9999999999.9
        out_res = []
        for i in a:
            if i is not np.nan:
                min = np.linalg.norm(i - b[0])
                result = [min, i, b[0]]  
                for j in b:
                    if j is not np.nan:
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
def compare_two(num1, num2):
    df1=pd.read_csv(os.path.join(current_dir,'data', ''+num1+'.txt'), header=None,delim_whitespace=True)
    df1.columns = ['class', 'x', 'y','w','h']
    df2=pd.read_csv(os.path.join(current_dir,'data', ''+num2+'.txt'), header=None,delim_whitespace=True)
    df2.columns = ['class', 'x', 'y','w','h']
    l1 = df1[['x','y']].as_matrix()
    l2 = df2[['x','y']].as_matrix()
    df_result= nearest(l1,l2)
    df_result =pd.concat([df_result["distance"],df_result["before"].apply(pd.Series),df_result["after"].apply(pd.Series)], axis = 1)
    df_result.columns=['distance_'+num1+'_'+num2+'', 'x_'+num1+'', 'y_'+num1+'','x_'+num2+'','y_'+num2+'']
    category_num1= df1[['x','y','class']]
    category_num1.columns=['x_'+num1+'', 'y_'+num1+'','class_'+num1+'']
    df_result=pd.merge(df_result, category_num1, on=['x_'+num1+'', 'y_'+num1+''], how='outer')
    category_num2= df2[['x','y','class']]
    category_num2.columns=['x_'+num2+'', 'y_'+num2+'','class_'+num2+'']
    df_result=pd.merge(df_result, category_num2, on=['x_'+num2+'', 'y_'+num2+''], how='outer')
    df_result=df_result.drop_duplicates()
    return df_result

#上限値を定める
def compare_two_complete(num1, num2,limit):
    df1 = compare_two(num1,num2)
    df1A = df1[df1['distance_'+num1+'_'+num2+''] < limit]
    df_result=df1A.drop_duplicates()
    df_result.to_csv(os.path.join(current_dir,'data','result_two.csv'),encoding='utf_8',index=False)
    return df_result

def compare_many(list,limit):
    #最初の2つを繋げておく
    df_result = compare_two_complete(list[0],list[1])
    #繋げていく
    for index in range(len(list)-2):
        # 5~9日だった場合、ここで6日と7日
        df = compare_two_complete(list[index+1],list[index+2],limit)
        df_result = pd.merge(df_result,df, on=['x_'+list[index+1]+'','y_'+list[index+1]+''], how='outer')
    df_result.to_csv(os.path.join(current_dir,'data','result_many.csv'),encoding='utf_8',index=False)
    return df_result

if __name__ == '__main__':
    val = input('Enter the Mode (two/many): ')

    if val == 'two':
        val1 = input('Enter the first csv name: ')
        val2 = input('Enter the second csv name: ')
        limit = input('Enter the limit: ')
        compare_two_complete(val1, val2,limit)
    
    elif val == 'many':
        limit = input('Enter the limit: ')
        os.chdir("/data")
        compare_many(glob.glob("./*.csv"),limit)

    else:
        print('入力値は(two/many)から選んでください')