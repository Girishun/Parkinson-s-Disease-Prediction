# Parkinsons' Disease Prediction


## Objective
**The major objectives of the project are as follows:**
• Early classification Parkinson’s disease of from magnetic resonance imaging (MRI)
plays an important role in the diagnosis of such diseases. There are many diagnostic
imaging methods used to identify Parkinson’s disease.
• MRI is commonly used for such tasks because of its unmatched image quality. The
relevance of artificial intelligence (AI) in the form of deep learning (DL) has
revolutionized new methods of automated medical image diagnosis. This study aimed
to develop a robust and efficient method based on transfer learning technique for
classifying Parkinson’s disease using MRI. In this article, the popular deep learning
architectures are utilized to develop Parkinson’s disease diagnostic system..
• The experiment was performed using two benchmark datasets that are openly
accessible from the web. Images from the dataset were first cropped, preprocessed,
and augmented for accurate and fast training.
• The performance of the transfer learning models is evaluated using performance
metrics of accuracy. From the experimental results, our proposed CNN model is using
ADAM optimizer. The proposed method is superior to the existing literature,
indicating that it can be used to quickly and accurately classify Parkinson’s diseases.

## Existing System
• In the first stage, there is a computer based procedures to detect PD and classify the
type of PD using Artificial Neural Network Algorithm for MRI images of different
patients. The second stage involves the use of different image processing techniques
such as histogram equalization, image segmentation, image enhancement,
morphological operations and feature extraction are used for Parkinson’s disease
detection in the MRI images for the PD affected patients.
• This work is introduced one automatic Parkinson’s disease detection method to
increase the accuracy and decrease the diagnosis time.
• As input for this system is MRI, scanned image and it contain noise. Therefore, our
first aim is to remove noise from input image. As explained in system flow we are
using high pass filter for noise removal and image preprocessing.
• The feature extraction is used for edge detection of the images. It is the process of
collecting higher level information of image such as shape, texture, color, and
contrast.

## Proposed System
• The proposed system has mainly five modules. Dataset, Pre-processing, Split the
data, Build CNN model train Deep Neural network for epochs, and classification.
• In dataset we can take multiple MRI images and take one as input image. In preprocessing image to encoded the label and resize the image. In split the data we set
the image as 80% Training Data and 20% Testing Data.
• Then build CNN model train deep neural network for epochs. Then classified the
image as yes or no if PD is positive then it returns yes and the PD is negative the it
returns no. The proposed framework model includes four stages.
• First, the input MR image is preprocessed (brain cropping and resizing, data
splitting and normalization). Second, the data augmentation technique is used to
increase the size of the dataset and extract the features.
• The features extracted by the CNN models are classified using the softmax layer
