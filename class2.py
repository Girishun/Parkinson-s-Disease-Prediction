import tensorflow as tf

from keras_preprocessing.image import ImageDataGenerator
from keras_preprocessing import image
import numpy as np
import easygui
import os
import serial
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)
print(tf.__version__)


train_datagen = ImageDataGenerator(

        
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

train_set = train_datagen.flow_from_directory(
        'Class2/training_set',
       
        target_size=(64, 64),
        
        batch_size=32,
       
        class_mode='binary')



test_datagen = ImageDataGenerator(rescale=1./255)

test_set = test_datagen.flow_from_directory(
        'Class2/test_set',
        target_size=(64, 64),
        batch_size=32,
        class_mode='binary')

print(test_set)


cnn = tf.keras.models.Sequential()


cnn.add(tf.keras.layers.Conv2D(filters = 32, kernel_size = 3, activation = 'relu', input_shape=[64,64,3]))


cnn.add(tf.keras.layers.MaxPool2D(pool_size=2 ,strides=2))

cnn.add(tf.keras.layers.Conv2D(filters = 32, kernel_size = 3, activation = 'relu'))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2 ,strides=2))


cnn.add(tf.keras.layers.Flatten())


cnn.add(tf.keras.layers.Dense(units = 128, activation = 'relu'))


cnn.add(tf.keras.layers.Dense(units = 1, activation = 'sigmoid'))


cnn.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

cnn.fit(x = train_set, validation_data = test_set, epochs = 25)
cnn.save('model/save1',overwrite=True,
    include_optimizer=True,
    save_format=None,
    signatures=None,
    options=None,
    save_traces=True,)
cnn.save('model/Class2/model_Class2.h5')

from sklearn.metrics import classification_report

y_pred = cnn.predict(test_set)
y_pred = (y_pred > 0.5)
y_true = test_set.classes
print(classification_report(y_true, y_pred))

a="continue"
while a=="continue":
   image11 = easygui.fileopenbox()
   test_image2 = image.load_img(image11, target_size = (64, 64))
   test_image2 = image.img_to_array(test_image2)
   test_image2 = np.expand_dims(test_image2, axis = 0)
   
   result2 = cnn.predict(test_image2)
   print(result2)
   if result2[0][0] == 0:
      prediction2 = 'Idiopathic Parkinson'
   else:
      prediction2 = 'other Category'


   print(prediction2)
   print("Type your ans")
   b=str(input("continue or  exit ; "))
   a=b.lower()
