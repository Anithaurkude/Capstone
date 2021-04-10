# -*- coding: utf-8 -*-
"""MoredataultralyticsYOLOv3

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QWJYySGwRFy7Gaj1qOcRwwsjABIZaeJB
"""

from google.colab import drive
drive.mount('/content/gdrive')

import os
os.chdir('/content/gdrive/My Drive/yolov3')

import os
import torch
from IPython.display import Image, clear_output 
print('PyTorch %s %s' % (torch.__version__, torch.cuda.get_device_properties(0) if torch.cuda.is_available() else 'CPU'))

# Commented out IPython magic to ensure Python compatibility.
# %pip install -qr requirements.txt  # install dependencies

import torch
from IPython.display import Image, clear_output  # to display images

clear_output()
print('Setup complete. Using torch %s %s' % (torch.__version__, torch.cuda.get_device_properties(0) if torch.cuda.is_available() else 'CPU'))

!pwd

# Commented out IPython magic to ensure Python compatibility.
# Tensorboard (optional)
# %load_ext tensorboard
# %tensorboard --logdir runs

# Commented out IPython magic to ensure Python compatibility.
# Weights & Biases (optional)
# %pip install -q wandb  
!wandb login  # use 'wandb disabled' or 'wandb enabled' to disable or enable

!ls -lrt

# Train YOLOv3 on COCO128 for 3 epochs
!python train.py --img 416 --batch 16 --epochs 1000 --data pothole.yaml --cfg models/yolov3.yaml --name potlholenewyolov3

"""# 4. Visualize"""

Image(filename='runs/train/potlholenewyolov3/train_batch1.jpg', width=400)  # train batch 0 mosaics and labels
Image(filename='runs/train/potlholenewyolov3/test_batch1_labels.jpg', width=400)  # test batch 0 labels
Image(filename='runs/train/potlholenewyolov3/test_batch1_pred.jpg', width=400)  # test batch 0 predictions

from utils.plots import plot_results 
plot_results(save_dir='runs/train/potlholenewyolov3')  # plot all results*.txt as results.png
Image(filename='runs/train/potlholenewyolov3/results.png', width=400)

from utils.plots import plot_results 
plot_results(save_dir='runs/train/potlholenewyolov3')  # plot all results*.txt as results.png
Image(filename='runs/train/potlholenewyolov3/results.png', width=400)

from utils.plots import plot_results 
plot_results(save_dir='runs/train/pt')  # plot all results*.txt as results.png
Image(filename='runs/train/pt2/results.png', width=400)

import pandas as pd
df = pd.DataFrame()
paths= ['/content/abcd','/kkh/kdfrf']
pred= [[0.56,9.77,0.55,0.5],[0.55,0.66,0.66,0.66]]
df = pd.DataFrame(paths)
df['preds'] = pred
df

orgdf = pd.read_csv('orginaldata.csv')
orgdf.head()

bb1 = orgdf.iloc[:,4:8]

bb1

preddf = pd.read_csv('dfnew.csv')
preddf.head()

bb2 = preddf.iloc[:,7:11]

bb2.shape,bb1.shape

bb1.iloc[0],bb2.iloc[0]

bb1.iloc[1],bb2.iloc[1]



get_iou(bb1.iloc[1:10],bb2.iloc[1:10])

iou_score = []
for i in range(len(bb1-1)):
  print(i)
  iou_score.append(get_iou(bb1.iloc[i],bb2.iloc[i]))
print(iou_score)

def get_iou(bb1, bb2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.

    Parameters
    ----------
    bb1 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x1, y1) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner
    bb2 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x, y) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner

    Returns
    -------
    float
        in [0, 1]
    """

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1['x1'], bb2['x1'])
    y_top = max(bb1['y1'], bb2['y1'])
    x_right = min(bb1['x2'], bb2['x2'])
    y_bottom = min(bb1['y2'], bb2['y2'])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both AABBs
    bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
    bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    
    return iou

# def get_iou(bb1, bb2):
#     """
#     Calculate the Intersection over Union (IoU) of two bounding boxes.

#     Parameters
#     ----------
#     bb1 : dict
#         Keys: {'x1', 'x2', 'y1', 'y2'}
#         The (x1, y1) position is at the top left corner,
#         the (x2, y2) position is at the bottom right corner
#     bb2 : dict
#         Keys: {'x1', 'x2', 'y1', 'y2'}
#         The (x, y) position is at the top left corner,
#         the (x2, y2) position is at the bottom right corner

#     Returns
#     -------
#     float
#         in [0, 1]
#     """
#     x_left = []
#     y_top = []
#     x_right = []
#     y_bottom = [] 
#     intersection_area = []
#     bb2_area = []
#     bb1_area = []
#     iou = []
#     for i in range(len(bb2)):
     
#       # determine the coordinates of the intersection rectangle
#       x_left[i] = max(bb1.iloc[i]['x1'], bb2.iloc[i]['x1'])
#       y_top[i] = max(bb1.iloc[i]['y1'], bb2.iloc[i]['y1'])
#       x_right[i] = min(bb1.iloc[i]['x2'], bb2.iloc[i]['x2'])
#       y_bottom[i] = min(bb1.iloc[i]['y2'], bb2.iloc[i]['y2'])

#       if x_right[i] < x_left[i] or y_bottom[i] < y_top[i]:
#           return 0.0

#     # The intersection of two axis-aligned bounding boxes is always an
#     # axis-aligned bounding box
#       intersection_area[i] = (x_right - x_left) * (y_bottom - y_top)

#     # compute the area of both AABBs
#       bb1_area[i] = (bb1.iloc[i]['x2'] - bb1.iloc[i]['x1']) * (bb1.iloc[i]['y2'] - bb1.iloc[i]['y1'])
#       bb2_area[i] = (bb2.iloc[i]['x2'] - bb2.iloc[i]['x1']) * (bb2.iloc[i]['y2'] - bb2.iloc[i]['y1'])

#     # compute the intersection over union by taking the intersection
#     # area and dividing it by the sum of prediction + ground-truth
#     # areas - the interesection area
#       iou[i] = intersection_area / float(bb1_area + bb2_area - intersection_area)
    
#       return iou

#Compute IOU
from skimage.morphology import label
def iou_metric(y_true_in, y_pred_in, print_table=False):
    labels = label(y_true_in > 0.5)
    y_pred = label(y_pred_in > 0.5)
    
    true_objects = len(np.unique(labels))
    pred_objects = len(np.unique(y_pred))

    intersection = np.histogram2d(labels.flatten(), y_pred.flatten(), bins=(true_objects, pred_objects))[0]

    # Compute areas (needed for finding the union between all objects)
    area_true = np.histogram(labels, bins = true_objects)[0]
    area_pred = np.histogram(y_pred, bins = pred_objects)[0]
    area_true = np.expand_dims(area_true, -1)
    area_pred = np.expand_dims(area_pred, 0)

    # Compute union
    union = area_true + area_pred - intersection

    # Exclude background from the analysis
    intersection = intersection[1:,1:]
    union = union[1:,1:]
    union[union == 0] = 1e-9

    # Compute the intersection over union
    iou = intersection / union

# def iou_metric_batch(y_true_in, y_pred_in):
#     batch_size = y_true_in.shape[0]
#     metric = []
#     for batch in range(batch_size):
#         value = iou_metric(y_true_in[batch], y_pred_in[batch])
#         metric.append(value)
#     return np.array(np.mean(metric), dtype=np.float32)

# def my_iou_metric(label, pred):
#     metric_value = tf.py_func(iou_metric_batch, [label, pred], tf.float32)
#     return metric_value

import numpy as np
arr = np.ndarray([2,3])
arr.shape

!python detect.py --source /content/gdrive/MyDrive/potholes3/images/test/ --img 416 --weights /content/gdrive/MyDrive/yolov3/runs/train/potlholenewyolov3/weights/best.pt

# Commented out IPython magic to ensure Python compatibility.
# %%time
# !python detect.py --source /content/gdrive/MyDrive/potholes3/images/test/ --img 416 --weights /content/gdrive/MyDrive/yolov3/runs/train/potlholenewyolov3/weights/best.pt

import os
import pandas as pd
#list the files
filelist = os.listdir('/content/gdrive/MyDrive/potholes1/images/test') 
dftest = pd.DataFrame(filelist, columns=['filename'])
dftest.head()

import os
import glob
import pandas as pd
import argparse
import xml.etree.ElementTree as ET
#Now create the masks using the bounding rects which are present in the annotations folder
#loop into each image name and get its xml file and prepare the mask png
xml_list = []
for pngname in dftest['filename']:
  xmlname = pngname.replace('.png','.xml')
  tree = ET.parse('/content/gdrive/MyDrive/potholes1/labels/test/'+xmlname)
  root = tree.getroot()
  size = root.find('size')
  if (len(root.findall('object')) == 0):
    value = ('/content/gdrive/MyDrive/potholes1/images/test/' + root.find('filename').text,
              int(size.find('width').text),
              int(size.find('height').text),
              'No',
              int(0),
              int(0),
              int(0),
              int(0)
              )
    xml_list.append(value)
  else:
    for member in root.findall('object'):
        #try:
        bndbox = member.find('bndbox')
        #print(len(bndbox))
        value = ('/content/gdrive/MyDrive/potholes1/images/test/' + root.find('filename').text,
                    int(size.find('width').text),
                    int(size.find('height').text),
                    'Yes',
                    int(bndbox.find('xmin').text),
                    int(bndbox.find('ymin').text),
                    int(bndbox.find('xmax').text),
                    int(bndbox.find('ymax').text)
                    )
        xml_list.append(value)
      #except Exception as e:
      #    pass          
column_name = ['filename', 'width', 'height',
                'class', 'xmin', 'ymin', 'xmax', 'ymax']
xml_df = pd.DataFrame(xml_list, columns=column_name)
xml_df.head()
xml_df.to_csv('orginaldata.csv',index=False)

#!python detect.py --source /content/gdrive/MyDrive/potholes1/images/test/ --weights /content/gdrive/MyDrive/yolov3/runs/train/potlholenewyolov3/weights/best.pt

#!python detect.py --source /content/gdrive/MyDrive/potholes1/images/test/ --weights /content/gdrive/MyDrive/yolov3/runs/train/potlholenewyolov3/weights/best.pt