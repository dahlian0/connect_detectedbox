# rose_detection
This repository assumes that the object does not move in an image acquired from a fixed point.
If we have an image acquired from the same location and an image with object detection, we can connect the nearest Bounding Box to each other.


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


