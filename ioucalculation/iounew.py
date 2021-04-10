# -*- coding: utf-8 -*-
"""IOUnew.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iEZ7DVrc3GuNGAS-rCWRLvPM03ryyeCJ
"""

import pandas as pd

from google.colab import drive
drive.mount('/content/gdrive')

import os
os.chdir('/content/gdrive/My Drive/moredatayolov3')

#Compute IOU
def iou_metric(y_true_in, y_pred_in, print_table=False):
    labels = y_true_in
    y_pred = y_pred_in
    #print('labels-->',labels)
    #print('y_pred-->',y_pred)
    true_objects = len(np.unique(labels))
    pred_objects = len(np.unique(y_pred))
    #print('true_objects',true_objects)
    #print('pred_objects',pred_objects)
    intersection = np.histogram2d(labels.flatten(), y_pred.flatten(), bins=(true_objects, pred_objects))[0]
    #print('intersection->',intersection)
    # Compute areas (needed for finding the union between all objects)
    area_true = np.histogram(labels, bins = true_objects)[0]
    area_pred = np.histogram(y_pred, bins = pred_objects)[0]
    area_true = np.expand_dims(area_true, -1)
    area_pred = np.expand_dims(area_pred, 0)
    #print('area_true',area_true)
    #print('area_pred',area_pred)
    # Compute union
    union = area_true + area_pred - intersection
    #print('union',union)
    # Exclude background from the analysis
    intersection = intersection[1:,1:]
    #print('intersection',intersection)
    union = union[1:,1:]
    union[union == 0] = 1e-9
    #print('union-->',union)
    # Compute the intersection over union
    iou = intersection / union
    
    return iou

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

df_predmore = pd.read_csv('finalyolov3.csv')

df_predmore.head()

df_predv5 = pd.read_csv('dfyolov51.csv')

df_predv5.head()

df_predmoreyolov5 = pd.read_csv('dfmoreyolov5.csv')

df_true = pd.read_csv('dftrue.csv')

df_true109 = pd.read_csv('y_true_109.csv')

df_true109

df_true109.head()

df_predv5.shape

df_predmore.shape,df_true109.shape,

df_predmore.shape,df_truemore.shape,

df_true_unique_imgs = df_true109[['filename', 'height', 'width']].drop_duplicates()
df_true109.shape, df_true_unique_imgs.shape

# df_true_more_unique_imgs = df_truemore[['filename', 'height', 'width']].drop_duplicates()
# df_truemore.shape, df_true_more_unique_imgs.shape

int(df_predmore['Size'][0].split(',')[0]), int(df_predmore['Size'][0].split(',')[1])

newpredSSDdf = df_predSSD[df_predSSD['Path'].isin(df_true109['filename'])]

newpredSSDdf[~(newpredSSDdf['Path'].isin(df_true109['filename']))]

df_true_unique_imgs[~(df_true_unique_imgs['filename'].isin(newpredSSDdf['Path']))]

missingssd = df_true_unique_imgs[~(df_true_unique_imgs['filename'].isin(newpredSSDdf['Path']))]

missingssd

missingssd.to_csv('missingssd1.csv',index=False)

newpreddf = df_predmore[df_predmore['Path'].isin(df_true109['filename'])]

df_predmore[~(df_predmore['Path'].isin(df_true109['filename']))]

df_true_unique_imgs[~(df_true_unique_imgs['filename'].isin(df_predv5['Path']))]

missingdfyolov5 = df_true_unique_imgs[~(df_true_unique_imgs['filename'].isin(df_predv5['Path']))]

missingdfyolov3 = df_true_unique_imgs[~(df_true_unique_imgs['filename'].isin(df_predmore['Path']))]

missingdfyolov5.to_csv('missingdfyolov5latest.csv',index=False)

df = pd.read_csv('newssddffinal.csv')

df.head()

import numpy as np
filenames = []
for idx, iter_rows in df_true_unique_imgs.iterrows():
    filename = iter_rows['filename']
    #filenames.append(filename)
    image_height = iter_rows['height']
    #print('image_height-->',image_height)
    image_width = iter_rows['width']
    #print('image_width-->',image_width)
    true_img_msk = np.zeros((image_width, image_height))
    #print(true_img_msk)
    pred_img_msk = np.zeros((image_width, image_height))
    #print(pred_img_msk)

    df_true_relevant = df_true109[df_true109['filename']==filename]
    #print('df_true_relevant',df_true_relevant)
    for idx, row in df_true_relevant.iterrows():
        x1 = int(row['x1'])
        y1 = int(row['y1'])
        x2 = int(row['x2'])
        y2 = int(row['y2'])
        true_img_msk[x1:x2, y1:y2] = 1
        #print(true_img_msk)
        
    # print(filenames)
    # k = 0
    # for k , file  in enumerate(filenames):
    #   print('file',file)
    #   if k < len(file):
    #     df_pred_relevant = df_predmore[df_predmore['Path']==file]
    #     k = k+1
      

    #df_pred_relevant = df_predmore[df_predmore['Path']!= filename]   
    # df_predmore.loc[df_predmore['Path'] == filename]:
    #   df_pred_relevant['Path'] = filename
    #   df_pred_relevant['x1'] = 0
    #   df_pred_relevant['y1'] = 0
    #   df_pred_relevant['x2'] = 0
    #   df_pred_relevant['y2'] = 0
    #   df_pred_relevant['ob_score']=0
    #   df_pred_relevant['Size'] = 0
    # #print('df_pred_relevant',df_pred_relevant)
    # print('filename----->',filename)
    # print('df_predmore[Path]',df_predmore['Path'])
    df_pred_relevant = df[df['Path'] == filename]   
    for idx, row in df_pred_relevant.iterrows():

        pred_img_width = int(row['Size'].split(',')[1])
        #print('pred_img_width',pred_img_width)
        pred_img_height = int(row['Size'].split(',')[0])
        #print('pred_img_height',pred_img_height)

        x1 = int(row['x1'] * image_width / pred_img_width)
        y1 = int(row['y1'] * image_height / pred_img_height)
        x2 = int(row['x2'] * image_width / pred_img_width)
        y2 = int(row['y2'] * image_height / pred_img_height)
        
        pred_img_msk[x1:x2, y1:y2] = 1
    
    print(filename, iou_metric(true_img_msk, pred_img_msk))
    
    if( iou_metric(true_img_msk, pred_img_msk )>0.10):
      print(filename,iou_metric(true_img_msk, pred_img_msk ))

import numpy as np
filenames = []
for idx, iter_rows in df_true_unique_imgs.iterrows():
    filename = iter_rows['filename']
    #filenames.append(filename)
    image_height = iter_rows['height']
    #print('image_height-->',image_height)
    image_width = iter_rows['width']
    #print('image_width-->',image_width)
    true_img_msk = np.zeros((image_width, image_height))
    #print(true_img_msk)
    pred_img_msk = np.zeros((image_width, image_height))
    #print(pred_img_msk)

    df_true_relevant = df_true109[df_true109['filename']==filename]
    #print('df_true_relevant',df_true_relevant)
    for idx, row in df_true_relevant.iterrows():
        x1 = int(row['x1'])
        y1 = int(row['y1'])
        x2 = int(row['x2'])
        y2 = int(row['y2'])
        true_img_msk[x1:x2, y1:y2] = 1
       
        
    # print(filenames)
    # k = 0
    # for k , file  in enumerate(filenames):
    #   print('file',file)
    #   if k < len(file):
    #     df_pred_relevant = df_predmore[df_predmore['Path']==file]
    #     k = k+1
      

    #df_pred_relevant = df_predmore[df_predmore['Path']!= filename]   
    # df_predmore.loc[df_predmore['Path'] == filename]:
    #   df_pred_relevant['Path'] = filename
    #   df_pred_relevant['x1'] = 0
    #   df_pred_relevant['y1'] = 0
    #   df_pred_relevant['x2'] = 0
    #   df_pred_relevant['y2'] = 0
    #   df_pred_relevant['ob_score']=0
    #   df_pred_relevant['Size'] = 0
    # #print('df_pred_relevant',df_pred_relevant)
    # print('filename----->',filename)
    # print('df_predmore[Path]',df_predmore['Path'])
    df_pred_relevant = df_predmore[df_predmore['Path'] == filename]   
    for idx, row in df_pred_relevant.iterrows():

        pred_img_width = int(row['Size'].split(',')[1])
        #print('pred_img_width',pred_img_width)
        pred_img_height = int(row['Size'].split(',')[0])
        #print('pred_img_height',pred_img_height)

        x1 = int(row['x1'] * image_width / pred_img_width)
        y1 = int(row['y1'] * image_height / pred_img_height)
        x2 = int(row['x2'] * image_width / pred_img_width)
        y2 = int(row['y2'] * image_height / pred_img_height)
        
        pred_img_msk[x1:x2, y1:y2] = 1
    
    #print(filename, iou_metric(true_img_msk, pred_img_msk))
    
    if( iou_metric(true_img_msk, pred_img_msk )>0.30):
      print(filename,iou_metric(true_img_msk, pred_img_msk ))

missingdfyolov3.to_csv('missingdfyolov3latest.csv',index=False)

import numpy as np
filenames = []
for idx, iter_rows in df_true_unique_imgs.iterrows():
    filename = iter_rows['filename']
    #filenames.append(filename)
    image_height = iter_rows['height']
    #print('image_height-->',image_height)
    image_width = iter_rows['width']
    #print('image_width-->',image_width)
    true_img_msk = np.zeros((image_width, image_height))
    #print(true_img_msk)
    pred_img_msk = np.zeros((image_width, image_height))
    #print(pred_img_msk)

    df_true_relevant = df_true109[df_true109['filename']==filename]
    #print('df_true_relevant',df_true_relevant)
    for idx, row in df_true_relevant.iterrows():
        x1 = int(row['x1'])
        y1 = int(row['y1'])
        x2 = int(row['x2'])
        y2 = int(row['y2'])
        true_img_msk[x1:x2, y1:y2] = 1
       
        
    # print(filenames)
    # k = 0
    # for k , file  in enumerate(filenames):
    #   print('file',file)
    #   if k < len(file):
    #     df_pred_relevant = df_predmore[df_predmore['Path']==file]
    #     k = k+1
      

    #df_pred_relevant = df_predmore[df_predmore['Path']!= filename]   
    # df_predmore.loc[df_predmore['Path'] == filename]:
    #   df_pred_relevant['Path'] = filename
    #   df_pred_relevant['x1'] = 0
    #   df_pred_relevant['y1'] = 0
    #   df_pred_relevant['x2'] = 0
    #   df_pred_relevant['y2'] = 0
    #   df_pred_relevant['ob_score']=0
    #   df_pred_relevant['Size'] = 0
    # #print('df_pred_relevant',df_pred_relevant)
    # print('filename----->',filename)
    # print('df_predmore[Path]',df_predmore['Path'])
    df_pred_relevant = df_predmore[df_predmore['Path'] == filename]   
    for idx, row in df_pred_relevant.iterrows():

        pred_img_width = int(row['Size'].split(',')[1])
        #print('pred_img_width',pred_img_width)
        pred_img_height = int(row['Size'].split(',')[0])
        #print('pred_img_height',pred_img_height)

        x1 = int(row['x1'] * image_width / pred_img_width)
        y1 = int(row['y1'] * image_height / pred_img_height)
        x2 = int(row['x2'] * image_width / pred_img_width)
        y2 = int(row['y2'] * image_height / pred_img_height)
        
        pred_img_msk[x1:x2, y1:y2] = 1
    
    #print(filename, iou_metric(true_img_msk, pred_img_msk))
    
    if( iou_metric(true_img_msk, pred_img_msk )>0.30):
      print(filename,iou_metric(true_img_msk, pred_img_msk ))

import numpy as np
filenames = []
for idx, iter_rows in df_true_unique_imgs.iterrows():
    filename = iter_rows['filename']
    #filenames.append(filename)
    image_height = iter_rows['height']
    #print('image_height-->',image_height)
    image_width = iter_rows['width']
    #print('image_width-->',image_width)
    true_img_msk = np.zeros((image_width, image_height))
    #print(true_img_msk)
    pred_img_msk = np.zeros((image_width, image_height))
    #print(pred_img_msk)

    df_true_relevant = df_true109[df_true109['filename']==filename]
    #print('df_true_relevant',df_true_relevant)
    for idx, row in df_true_relevant.iterrows():
        x1 = int(row['x1'])
        y1 = int(row['y1'])
        x2 = int(row['x2'])
        y2 = int(row['y2'])
        true_img_msk[x1:x2, y1:y2] = 1
       
        
    # print(filenames)
    # k = 0
    # for k , file  in enumerate(filenames):
    #   print('file',file)
    #   if k < len(file):
    #     df_pred_relevant = df_predmore[df_predmore['Path']==file]
    #     k = k+1
      

    #df_pred_relevant = df_predmore[df_predmore['Path']!= filename]   
    # df_predmore.loc[df_predmore['Path'] == filename]:
    #   df_pred_relevant['Path'] = filename
    #   df_pred_relevant['x1'] = 0
    #   df_pred_relevant['y1'] = 0
    #   df_pred_relevant['x2'] = 0
    #   df_pred_relevant['y2'] = 0
    #   df_pred_relevant['ob_score']=0
    #   df_pred_relevant['Size'] = 0
    # #print('df_pred_relevant',df_pred_relevant)
    # print('filename----->',filename)
    # print('df_predmore[Path]',df_predmore['Path'])
    df_pred_relevant = df_predmore[df_predmore['Path'] == filename]   
    for idx, row in df_pred_relevant.iterrows():

        pred_img_width = int(row['Size'].split(',')[1])
        #print('pred_img_width',pred_img_width)
        pred_img_height = int(row['Size'].split(',')[0])
        #print('pred_img_height',pred_img_height)

        x1 = int(row['x1'] * image_width / pred_img_width)
        y1 = int(row['y1'] * image_height / pred_img_height)
        x2 = int(row['x2'] * image_width / pred_img_width)
        y2 = int(row['y2'] * image_height / pred_img_height)
        
        pred_img_msk[x1:x2, y1:y2] = 1
    
    #print(filename, iou_metric(true_img_msk, pred_img_msk))
    
    if( iou_metric(true_img_msk, pred_img_msk )>0.30):
      print(filename,iou_metric(true_img_msk, pred_img_msk ))

df_truemore[~(df_truemore['filename'].isin(df_predmoreyolov5['Path']))]

missingdfyolov5 = df_truemore[~(df_truemore['filename'].isin(df_predmoreyolov5['Path']))]

missingdfyolov5.to_csv('missingdfyolov5.csv',index=False)

missingdf = df_truemore[~(df_truemore['filename'].isin(df_predmore['Path']))]

missingdf.to_csv('missindf.csv',index=False)

missdf = pd.read_csv('missindf.csv')

newmissingdfyolov5  = pd.read_csv('missingdfyolov5.csv')

finaldfmoreyolov5 = pd.concat([newmissingdfyolov5,df_predmoreyolov5])

finaldfmoreyolov5.to_csv('finaldfmoreyolov5.csv',index=False)

finaldfmoreyolov5.shape

finaldf = pd.concat([missdf,df_predmore])

finaldf.to_csv('finaldf.csv',index=False)

finaldf1 = pd.read_csv('finaldf.csv')

finaldfv52 = pd.read_csv('finaldfmoreyolov5.csv')

import numpy as np
filenames = []
for idx, iter_rows in df_true_more_unique_imgs.iterrows():
    filename = iter_rows['filename']
    #filenames.append(filename)
    image_height = iter_rows['height']
    #print('image_height-->',image_height)
    image_width = iter_rows['width']
    #print('image_width-->',image_width)
    true_img_msk = np.zeros((image_width, image_height))
    #print(true_img_msk)
    pred_img_msk = np.zeros((image_width, image_height))
    #print(pred_img_msk)

    df_true_relevant = df_true109[df_true109['filename']==filename]
    #print('df_true_relevant',df_true_relevant)
    for idx, row in df_true_relevant.iterrows():
        x1 = int(row['x1'])
        y1 = int(row['y1'])
        x2 = int(row['x2'])
        y2 = int(row['y2'])
        true_img_msk[x1:x2, y1:y2] = 1
       
        
    # print(filenames)
    # k = 0
    # for k , file  in enumerate(filenames):
    #   print('file',file)
    #   if k < len(file):
    #     df_pred_relevant = df_predmore[df_predmore['Path']==file]
    #     k = k+1
      

    #df_pred_relevant = df_predmore[df_predmore['Path']!= filename]   
    # df_predmore.loc[df_predmore['Path'] == filename]:
    #   df_pred_relevant['Path'] = filename
    #   df_pred_relevant['x1'] = 0
    #   df_pred_relevant['y1'] = 0
    #   df_pred_relevant['x2'] = 0
    #   df_pred_relevant['y2'] = 0
    #   df_pred_relevant['ob_score']=0
    #   df_pred_relevant['Size'] = 0
    # #print('df_pred_relevant',df_pred_relevant)
    # print('filename----->',filename)
    # print('df_predmore[Path]',df_predmore['Path'])
    df_pred_relevant = df_predmore[df_predmore['Path'] == filename]   
    for idx, row in df_pred_relevant.iterrows():

        pred_img_width = int(row['Size'].split(',')[1])
        #print('pred_img_width',pred_img_width)
        pred_img_height = int(row['Size'].split(',')[0])
        #print('pred_img_height',pred_img_height)

        x1 = int(row['x1'] * image_width / pred_img_width)
        y1 = int(row['y1'] * image_height / pred_img_height)
        x2 = int(row['x2'] * image_width / pred_img_width)
        y2 = int(row['y2'] * image_height / pred_img_height)
        
        pred_img_msk[x1:x2, y1:y2] = 1
    
    print(filename, iou_metric(true_img_msk, pred_img_msk))

import numpy as np
filenames = []
for idx, iter_rows in df_true_more_unique_imgs.iterrows():
    filename = iter_rows['filename']
    #filenames.append(filename)
    image_height = iter_rows['height']
    #print('image_height-->',image_height)
    image_width = iter_rows['width']
    #print('image_width-->',image_width)
    true_img_msk = np.zeros((image_width, image_height))
    #print(true_img_msk)
    pred_img_msk = np.zeros((image_width, image_height))
    #print(pred_img_msk)

    df_true_relevant = df_truemore[df_truemore['filename']==filename]
    #print('df_true_relevant',df_true_relevant)
    for idx, row in df_true_relevant.iterrows():
        x1 = int(row['x1'])
        y1 = int(row['y1'])
        x2 = int(row['x2'])
        y2 = int(row['y2'])
        true_img_msk[x1:x2, y1:y2] = 1
       
        
    # print(filenames)
    # k = 0
    # for k , file  in enumerate(filenames):
    #   print('file',file)
    #   if k < len(file):
    #     df_pred_relevant = df_predmore[df_predmore['Path']==file]
    #     k = k+1
      

    #df_pred_relevant = df_predmore[df_predmore['Path']!= filename]   
    # df_predmore.loc[df_predmore['Path'] == filename]:
    #   df_pred_relevant['Path'] = filename
    #   df_pred_relevant['x1'] = 0
    #   df_pred_relevant['y1'] = 0
    #   df_pred_relevant['x2'] = 0
    #   df_pred_relevant['y2'] = 0
    #   df_pred_relevant['ob_score']=0
    #   df_pred_relevant['Size'] = 0
    # #print('df_pred_relevant',df_pred_relevant)
    # print('filename----->',filename)
    # print('df_predmore[Path]',df_predmore['Path'])
    df_pred_relevant = finaldf1[finaldf1['Path'] == filename]   
    for idx, row in df_pred_relevant.iterrows():

        pred_img_width = int(row['Size'].split(',')[1])
        #print('pred_img_width',pred_img_width)
        pred_img_height = int(row['Size'].split(',')[0])
        #print('pred_img_height',pred_img_height)

        x1 = int(row['x1'] * image_width / pred_img_width)
        y1 = int(row['y1'] * image_height / pred_img_height)
        x2 = int(row['x2'] * image_width / pred_img_width)
        y2 = int(row['y2'] * image_height / pred_img_height)
        
        pred_img_msk[x1:x2, y1:y2] = 1
    
    print(filename, iou_metric(true_img_msk, pred_img_msk))

df_truemore[df_truemore['filename']=='/content/gdrive/MyDrive/potholes3/images/test/India_000587.jpg']

df_predmoreyolov5[df_predmoreyolov5['Path']=='/content/gdrive/MyDrive/potholes3/images/test/India_000587.jpg']

df_pred = pd.read_csv('dfPred.csv')

df_true = pd.read_csv('dftrue.csv')

df_pred.head(1)

df_true.head(1)

df_true_unique_imgs = df_true[['filename', 'height', 'width']].drop_duplicates()
df_true.shape, df_true_unique_imgs.shape

df_true_unique_imgs.head(1)

int(df_pred['Size'][0].split(',')[0]), int(df_pred['Size'][0].split(',')[1])

import numpy as np
filenames = []
for idx, iter_rows in df_true_unique_imgs.iterrows():
    filename = iter_rows['filename']
    #filenames.append(filename)
    image_height = iter_rows['height']
    #print('image_height-->',image_height)
    image_width = iter_rows['width']
    #print('image_width-->',image_width)
    true_img_msk = np.zeros((image_width, image_height))
    #print(true_img_msk)
    pred_img_msk = np.zeros((image_width, image_height))
    #print(pred_img_msk)

    df_true_relevant = df_true[df_true['filename']==filename]
    #print('df_true_relevant',df_true_relevant)
    for idx, row in df_true_relevant.iterrows():
        x1 = int(row['x1'])
        y1 = int(row['y1'])
        x2 = int(row['x2'])
        y2 = int(row['y2'])
        true_img_msk[x1:x2, y1:y2] = 1
       
        
    # print(filenames)
    # k = 0
    # for k , file  in enumerate(filenames):
    #   print('file',file)
    #   if k < len(file):
    #     df_pred_relevant = df_predmore[df_predmore['Path']==file]
    #     k = k+1
      

    #df_pred_relevant = df_predmore[df_predmore['Path']!= filename]   
    # df_predmore.loc[df_predmore['Path'] == filename]:
    #   df_pred_relevant['Path'] = filename
    #   df_pred_relevant['x1'] = 0
    #   df_pred_relevant['y1'] = 0
    #   df_pred_relevant['x2'] = 0
    #   df_pred_relevant['y2'] = 0
    #   df_pred_relevant['ob_score']=0
    #   df_pred_relevant['Size'] = 0
    # #print('df_pred_relevant',df_pred_relevant)
    # print('filename----->',filename)
    # print('df_predmore[Path]',df_predmore['Path'])
    df_pred_relevant = df_predv5[df_predv5['Path'] == filename]   
    for idx, row in df_pred_relevant.iterrows():

        pred_img_width = int(row['Size'].split(',')[1])
        #print('pred_img_width',pred_img_width)
        pred_img_height = int(row['Size'].split(',')[0])
        #print('pred_img_height',pred_img_height)

        x1 = int(row['x1'] * image_width / pred_img_width)
        y1 = int(row['y1'] * image_height / pred_img_height)
        x2 = int(row['x2'] * image_width / pred_img_width)
        y2 = int(row['y2'] * image_height / pred_img_height)
        
        pred_img_msk[x1:x2, y1:y2] = 1
    
    print(filename, iou_metric(true_img_msk, pred_img_msk))

# from PIL import Image
import numpy as np

for idx, iter_rows in df_true_unique_imgs.iterrows():
    filename = iter_rows['filename']
    image_height = iter_rows['height']
    #print('image_height-->',image_height)
    image_width = iter_rows['width']
    #print('image_width-->',image_width)
    true_img_msk = np.zeros((image_width, image_height))
    #print(true_img_msk)
    pred_img_msk = np.zeros((image_width, image_height))
    #print(pred_img_msk)

    df_true_relevant = df_true[df_true['filename']==filename]
    #print('df_true_relevant',df_true_relevant)
    for idx, row in df_true_relevant.iterrows():
        x1 = int(row['x1'])
        y1 = int(row['y1'])
        x2 = int(row['x2'])
        y2 = int(row['y2'])
        true_img_msk[x1:x2, y1:y2] = 1
       
        
    df_pred_relevant = df_pred[df_pred['Path']==filename]
    #print('df_pred_relevant',df_pred_relevant)
    for idx, row in df_pred_relevant.iterrows():
        pred_img_width = int(row['Size'].split(',')[1])
        #print('pred_img_width',pred_img_width)
        pred_img_height = int(row['Size'].split(',')[0])
        #print('pred_img_height',pred_img_height)

        x1 = int(row['xmin'] * image_width / pred_img_width)
        y1 = int(row['ymin'] * image_height / pred_img_height)
        x2 = int(row['xmax'] * image_width / pred_img_width)
        y2 = int(row['ymax'] * image_height / pred_img_height)
        pred_img_msk[x1:x2, y1:y2] = 1
    
    print(filename, iou_metric(true_img_msk, pred_img_msk))

df_pred[df_pred['Path']=='/content/gdrive/MyDrive/potholes1/images/test/potholes99.png']

df_true[df_true['filename']=='/content/gdrive/MyDrive/potholes1/images/test/potholes99.png']

df_yolov3_kaggle = pd.read_csv('finalyolov3.csv')

df_yolov5_kaggle = pd.read_csv('dfyolov51_kaggle.csv')

df_true_kaggle = pd.read_csv('y_true_kaggle.csv')

df_true_kaggle.shape , df_yolov3_kaggle.shape

df_true_unique_imgs_kaggle = df_true_kaggle[['filename', 'height', 'width']].drop_duplicates()
df_true_kaggle.shape, df_true_unique_imgs_kaggle.shape

#missingdfyolov3 = df_true_unique_imgs_kaggle[~(df_true_unique_imgs_kaggle['filename'].isin(df_yolov3_kaggle['Path']))]

df_true_unique_imgs_kaggle[~(df_true_unique_imgs_kaggle['filename'].isin(df_yolov5_kaggle['Path']))]

import numpy as np
filenames = []
for idx, iter_rows in df_true_unique_imgs_kaggle.iterrows():
    filename = iter_rows['filename']
    #filenames.append(filename)
    image_height = iter_rows['height']
    #print('image_height-->',image_height)
    image_width = iter_rows['width']
    #print('image_width-->',image_width)
    true_img_msk = np.zeros((image_width, image_height))
    #print(true_img_msk)
    pred_img_msk = np.zeros((image_width, image_height))
    #print(pred_img_msk)

    df_true_relevant = df_true_kaggle[df_true_kaggle['filename']==filename]
    #print('df_true_relevant',df_true_relevant)
    for idx, row in df_true_relevant.iterrows():
        x1 = int(row['x1'])
        y1 = int(row['y1'])
        x2 = int(row['x2'])
        y2 = int(row['y2'])
        true_img_msk[x1:x2, y1:y2] = 1
       
        

    df_pred_relevant = df_yolov3_kaggle[df_yolov3_kaggle['Path'] == filename]   
    for idx, row in df_pred_relevant.iterrows():

        pred_img_width = int(row['Size'].split(',')[1])
        #print('pred_img_width',pred_img_width)
        pred_img_height = int(row['Size'].split(',')[0])
        #print('pred_img_height',pred_img_height)

        x1 = int(row['x1'] * image_width / pred_img_width)
        y1 = int(row['y1'] * image_height / pred_img_height)
        x2 = int(row['x2'] * image_width / pred_img_width)
        y2 = int(row['y2'] * image_height / pred_img_height)
        
        pred_img_msk[x1:x2, y1:y2] = 1
    
    #print(filename, iou_metric(true_img_msk, pred_img_msk))
    
    if( iou_metric(true_img_msk, pred_img_msk )>0.30):
      print(filename,iou_metric(true_img_msk, pred_img_msk ))

import numpy as np
filenames = []
for idx, iter_rows in df_true_unique_imgs_kaggle.iterrows():
    filename = iter_rows['filename']
    #filenames.append(filename)
    image_height = iter_rows['height']
    #print('image_height-->',image_height)
    image_width = iter_rows['width']
    #print('image_width-->',image_width)
    true_img_msk = np.zeros((image_width, image_height))
    #print(true_img_msk)
    pred_img_msk = np.zeros((image_width, image_height))
    #print(pred_img_msk)

    df_true_relevant = df_true_kaggle[df_true_kaggle['filename']==filename]
    #print('df_true_relevant',df_true_relevant)
    for idx, row in df_true_relevant.iterrows():
        x1 = int(row['x1'])
        y1 = int(row['y1'])
        x2 = int(row['x2'])
        y2 = int(row['y2'])
        true_img_msk[x1:x2, y1:y2] = 1
       
        

    df_pred_relevant = df_yolov5_kaggle[df_yolov5_kaggle['Path'] == filename]   
    for idx, row in df_pred_relevant.iterrows():

        pred_img_width = int(row['Size'].split(',')[1])
        #print('pred_img_width',pred_img_width)
        pred_img_height = int(row['Size'].split(',')[0])
        #print('pred_img_height',pred_img_height)

        x1 = int(row['x1'] * image_width / pred_img_width)
        y1 = int(row['y1'] * image_height / pred_img_height)
        x2 = int(row['x2'] * image_width / pred_img_width)
        y2 = int(row['y2'] * image_height / pred_img_height)
        
        pred_img_msk[x1:x2, y1:y2] = 1
    
    #print(filename, iou_metric(true_img_msk, pred_img_msk))
    
    if( iou_metric(true_img_msk, pred_img_msk )>0.30):
      print(filename,iou_metric(true_img_msk, pred_img_msk ))

df_predSSD = pd.read_csv('newssddffinal.csv')

df_predSSD.head()

df_predSSD.shape

