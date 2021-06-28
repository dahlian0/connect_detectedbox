import numpy as np
import os
import glob
import pandas as pd
import re
current_dir=os.path.dirname(os.path.abspath(__file__))
df1=pd.read_csv(os.path.join(current_dir,'1','merge_output_08.txt.csv'))
df2=pd.read_csv(os.path.join(current_dir,'1','merge_output_09.txt.csv'))
l1 = df1[['left_x','top_y']].as_matrix()
l2 = df2[['left_x','top_y']].as_matrix()


def nearest(a, b):
    d=[]
    while (len(a) > 0) and (len(b) > 0):

        out_min = 9999999999.9
        out_res = []

        for i in a:
            min = np.linalg.norm(i - b[0])
            result = [min, i, b[0]]  
            for j in b:
                c = np.linalg.norm(i - j)
                if min > c:
                    min = c
                    result = [min, i, j]  
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

df_result= nearest(l1,l2)
#print(df_result)
df_result.to_csv(os.path.join(current_dir,'1','compare_08_09.csv'),encoding='utf_8',index=False)