# 使い方
- yolov4で写真ごとのBounding Boxに関するtxtファイルを取得
- 必要な部分だけ抽出し、txtファイルからcsvを生成するため、text.pyを実行
　merge_(元のファイル名).csvというファイルを作成できる
- nearest.pyというファイルに近傍点を探す関数がある

# ToDo
- yoloで閾値を二つのクラスで超えた場合、二つのbounding Boxが表されている
- yolo側のオプションを変えるか、bounding boxの確率の高い方だけを残すようにする。

# yolov5の場合
- txtで表示されているのは, class名,x ,y ,w, h