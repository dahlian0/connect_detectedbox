import os
import glob
import pandas as pd
import re
current_dir=os.path.dirname(os.path.abspath(__file__))
path = './1/*.txt'
# compare_1/フォルダ内にあって拡張子がtxtのファイル名を取得
file_list = glob.glob(path, recursive=True)
# ファイル名だけを抽出
file_list = [os.path.basename(r) for r in file_list] 

for i in file_list:
  df = pd.read_csv(os.path.join(current_dir,'1',str(i)) ,header=None, skiprows=14,delim_whitespace=True)
  df = df.iloc[:,[0,1,3,5,7,9]]
  df.columns=["class", "probability", "left_x", "top_y","width","height"]
  df["class"]=df["class"].str.replace(':',"")
  df["probability"]=df["probability"].str.replace('%',"")
  df["height"]=df["height"].str.replace(')',"")
  print(df)
  df.to_csv(os.path.join(current_dir,'1','merge_'+str(i)+'.csv'),encoding='utf_8',index=False)

  #word=df.iloc[1].str.split('left_x:')[-1].split('top_y:')[0]