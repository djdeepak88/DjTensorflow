#!/usr/bin/env python
# coding: utf-8

# # Object Detection Demo
# Welcome to the object detection inference walkthrough!  This notebook will walk you step by step through the process of using a pre-trained model to detect objects in an image. Make sure to follow the [installation instructions](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md) before you start.

# # Imports

# In[1]:

import numpy as np
import os

import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from distutils.version import StrictVersion
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
import json 
from prompt_toolkit import output

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append(".")
from utils import ops as utils_ops

if StrictVersion(tf.__version__) < StrictVersion('1.9.0'):
  raise ImportError('Please upgrade your TensorFlow installation to v1.9.* or later!')


# ## Env setup

# In[2]:


# This is needed to display the images.
# get_ipython().magic(u'matplotlib inline')


# ## Object detection imports
# Here are the imports from the object detection module.

# In[ ]:


from utils import label_map_util

from utils import visualization_utils as vis_util


# # Model preparation

# ## Variables
#
# Any model exported using the `export_inference_graph.py` tool can be loaded here simply by changing `PATH_TO_FROZEN_GRAPH` to point to a new .pb file.
#
# By default we use an "SSD with Mobilenet" model here. See the [detection model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) for a list of other models that can be run out-of-the-box with varying speeds and accuracies.

# In[3]:


# What model to download.
MODEL_NAME = 'ssd_mobilenet_v1_coco_2018_01_28'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'
HELMET_MODEL_NAME = 'ssd_mobilenet_v1_coco_2018_01_28/Exported_Model'


# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_FROZEN_GRAPH_HELMET = HELMET_MODEL_NAME + '/frozen_inference_graph.pb'

PATH_TO_FROZEN_GRAPH = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
#PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
PATH_TO_LABELS_HELMET = os.path.join('data', 'Helmet_label_map.pbtxt')


# ## Download Model

# In[4]:

print "Stage1"
'''
opener = urllib.request.URLopener()
opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
tar_file = tarfile.open(MODEL_FILE)
for file in tar_file.getmembers():
  file_name = os.path.basename(file.name)
  if 'frozen_inference_graph.pb' in file_name:
    tar_file.extract(file, os.getcwd())
'''

# ## Load a (frozen) Tensorflow model into memory.

# In[ ]:

print "Loading the Frozen Inference Graph for all generic objects"

detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

print "Loading the Helmet Inference Graph for Helmet"

detection_graph2 = tf.Graph()
with detection_graph2.as_default():
  od_graph_def2 = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH_HELMET, 'rb') as fid:
    serialized_graph2 = fid.read()
    od_graph_def2.ParseFromString(serialized_graph2)
    tf.import_graph_def(od_graph_def2, name='')



# ## Loading label map
# Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine

# In[5]:


category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

category_index_helmet = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS_HELMET, use_display_name=True)

# ## Helper code

# In[ ]:


def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


# # Detection

# In[ ]:


# For the sake of simplicity we will use only 2 images:
# image1.jpg
# image2.jpg
# If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
PATH_TO_TEST_IMAGES_DIR = 'test_images'
TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, '[Biker]{}.jpg'.format(i)) for i in range(1,7) ]

print TEST_IMAGE_PATHS

# Output Directory
PATH_TO_OUTPUT_IMAGES_DIR = 'Output_images'

# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)


# In[ ]:

print "Stage 3"

def run_inference_for_single_image(image, graph):
  with graph.as_default():
    with tf.Session() as sess:
      # Get handles to input and output tensors
      ops = tf.get_default_graph().get_operations()
      all_tensor_names = {output.name for op in ops for output in op.outputs}
      tensor_dict = {}
      for key in [
          'num_detections', 'detection_boxes', 'detection_scores',
          'detection_classes', 'detection_masks'
      ]:
        tensor_name = key + ':0'
        if tensor_name in all_tensor_names:
          tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
              tensor_name)
      if 'detection_masks' in tensor_dict:
        # The following processing is only for single image
        detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
        detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
        # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
        real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
        detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
        detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            detection_masks, detection_boxes, image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(
            tf.greater(detection_masks_reframed, 0.5), tf.uint8)
        # Follow the convention by adding back the batch dimension
        tensor_dict['detection_masks'] = tf.expand_dims(
            detection_masks_reframed, 0)
      image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

      # Run inference
      output_dict = sess.run(tensor_dict,
                             feed_dict={image_tensor: np.expand_dims(image, 0)})

      # all outputs are float32 numpy arrays, so convert types as appropriate
      output_dict['num_detections'] = int(output_dict['num_detections'][0])
      output_dict['detection_classes'] = output_dict[
          'detection_classes'][0].astype(np.uint8)
      output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
      output_dict['detection_scores'] = output_dict['detection_scores'][0]
      if 'detection_masks' in output_dict:
        output_dict['detection_masks'] = output_dict['detection_masks'][0]
  return output_dict


# In[ ]:

print "Stage 4"

for image_path in TEST_IMAGE_PATHS:
  print image_path
  image = Image.open(image_path)
  # the array based representation of the image will be used later in order to prepare the
  # result image with boxes and labels on it.
  image_np = load_image_into_numpy_array(image)
  image_np_copy = np.array(image_np)
  
  # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
  image_np_expanded = np.expand_dims(image_np, axis=0)
  # Actual detection.
  print "Generic_Object_Detection"
  output_dict = run_inference_for_single_image(image_np, detection_graph)
  print "Helmet_Object_Detection"
  output_dict2 = run_inference_for_single_image(image_np_copy, detection_graph2)
  # Visualization of the results of a detection.
  #print "Output Dictionary."
  #print output_dict
  #print "##################"
  #print output_dict['detection_boxes']
  #print "$$$$$$$$$$$$$$$$$$"
  #print output_dict['detection_classes']
  #print "@@@@@@@@@@@@@@@@@@"
  #output_dict['detection_scores']
  
  print "Generating the Boundation boxes for the object detection."

  img,obj_arr,overlap_people,helmet_overlap=vis_util.visualize_boxes_and_labels_on_image_array(
      image_np,
      output_dict['detection_boxes'],
      output_dict['detection_classes'],
      output_dict['detection_scores'],
      category_index,
      instance_masks=output_dict.get('detection_masks'),
      use_normalized_coordinates=True,
      line_thickness=8)
  
  print "Detecting the Helmet overlay"
  print overlap_people
  print "----------------------------"
  
  
  img1,obj_array,overlp,helmet_detection_dict =vis_util.visualize_boxes_and_labels_on_image_array(
      image_np_copy,
      output_dict2['detection_boxes'],
      output_dict2['detection_classes'],
      output_dict2['detection_scores'],
      category_index_helmet,
      instance_masks=output_dict2.get('detection_masks'),
      use_normalized_coordinates=True,
      line_thickness=8,
      overlp_people=overlap_people,
      Phase=2)
  
  print "Detection Statistics"
  print "Helmet OVerlap"
  print helmet_detection_dict
  helmet_overlap = 0
  
  for hell in helmet_detection_dict:
      print hell
      helmet_overlap = helmet_overlap + 1
  print "The Helmet Overlap"    
  print helmet_overlap
  print obj_arr
  ele_dict={}
  
  for x in obj_arr:
        class_ele = x.split(":")[0]
        print class_ele
        if class_ele in ele_dict:
          ele_dict[class_ele]= ele_dict[class_ele] + 1
        elif class_ele=="Intersection":
          ele_dict[class_ele]=x.split(":")[1]
        else:    
          ele_dict[class_ele] =1
  
  print "helmet array"
  print obj_array
  
  for x in obj_array:
      print "helmet array"
      print x
      class_ele = x.split(":")[0]
      print class_ele
      if class_ele in ele_dict:
          ele_dict[class_ele]=ele_dict[class_ele] + 1
      else:    
          ele_dict[class_ele] =1    
  
  if(ele_dict['Intersection'] > helmet_overlap):
      print "Violation"
      ele_dict['Violation']="True"
  else:
      ele_dict['Violation']="False"
      
  print ele_dict
  
  with open('{}.json'.format(os.path.basename(image_path).split(".")[0]), 'w') as fp:
    json.dump(ele_dict, fp)      
        
  print "####################"
  
  plt.figure(figsize=IMAGE_SIZE)
  plt.imshow(image_np)
  plt.savefig("Output_images/"+os.path.basename(image_path))
  plt.show()

  plt.figure(figsize=IMAGE_SIZE)
  plt.imshow(image_np_copy)
  plt.savefig("Output_images/"+os.path.basename(image_path))
  plt.show()
# In[ ]:

print "Stage FINAL"

# In[ ]:
