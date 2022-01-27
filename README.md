# rose_detection
This repository assumes that the object does not move in an image acquired from a fixed point.
If we have an image acquired from the same location and an image with object detection, we can connect the nearest Bounding Box to each other.

1. txt to csv
<img width="908" alt="detection" src="https://user-images.githubusercontent.com/48791086/151365335-eeb161f3-dfc8-4a77-a5bc-af12eefd770d.png">

2. Connect the nearest Bounding Box to each other
<img width="1123" alt="スクリーンショット 2022-01-27 22 19 41" src="https://user-images.githubusercontent.com/48791086/151366987-a148596d-7088-4d8e-a17f-8a6a0d6c1f98.png">

# Installation
You can easily install the libraries using the requirements.txt file.
```bash
pip install -r requirements.txt
```

# Usage
Place the txt file you want to use in data file.

```bash
git clone https://github.com/dahlian0/connect_detectedbox.git
```
To install the library using the requirements.txt file
```bash
pip install -r requirements.txt
```
The execution command that change txt file to csv file is
```bash
python text.py
```
The main execution command is
```bash
python yolov5.py
```
The message 'Enter the Mode (two/many):' is displayed.
If you want to compare two images, use two
If you want to compare three or more images at the same time, use many
to compare three or more images at once.

## License
This software is released under the MIT License, see LICENSE.

## Authors
Lisa SHINODA (Master Course Student at Kyoto University)


