# model 제작 프로그램 예제
# mask 폴더와 nomask 폴더에 직접 테스트셋 분류 후 실행하면 model 파일 생성됨 

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Flatten, BatchNormalization
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array

path_mask = './TestDetector/mask/'
path_nomask = './TestDetector/nomask/'

file_mask = os.listdir(path_mask)   # path에 존재하는 파일 목록 가져오기
file_nomask = os.listdir(path_nomask)

file_num = len(file_mask) + len(file_nomask)

# 이미지 전처리
num = 0
all_img = np.float32(np.zeros((file_num, 224, 224, 3))) 
all_label = np.float64(np.zeros((file_num, 1)))

for idx in file_mask:
    img_path = path_mask + idx
    img = load_img(img_path, target_size=(224, 224))    # resizing
    
    x = img_to_array(img)   # Preprocessing
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    all_img[num, :, :, :] = x
    
    all_label[num] = 1 # mask dataset
    num = num + 1

for idx in file_nomask:
    img_path = path_nomask + idx
    img = load_img(img_path, target_size=(224, 224))    # resizing
    
    x = img_to_array(img)   # Preprocessing
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    all_img[num, :, :, :] = x
    
    all_label[num] = 0 # nomask dataset
    num = num + 1

# 데이터셋 섞기 
n_elem = all_label.shape[0]
indices = np.random.choice(n_elem, size=n_elem, replace=False)

all_label = all_label[indices]
all_img = all_img[indices]

# 훈련셋 테스트셋 분할
num_train = int(np.round(all_label.shape[0]*0.8))
num_test = int(np.round(all_label.shape[0]*0.2))

train_img = all_img[0:num_train, :, :, :]
test_img = all_img[num_train:, :, :, :] 

train_label = all_label[0:num_train]
test_label = all_label[num_train:]

# 전처리 모델 생성
IMG_SHAPE = (224, 224, 3)

base_model = ResNet50(input_shape=IMG_SHAPE, weights='imagenet', include_top=False)
base_model.trainable = False
base_model.summary()
print("Number of layers in the base model: ", len(base_model.layers))

flatten_layer = Flatten()
dense_layer1 = Dense(128, activation='relu')
bn_layer1 = BatchNormalization()
dense_layer2 = Dense(1, activation=tf.nn.sigmoid)

model = Sequential([
        base_model,
        flatten_layer,
        dense_layer1,
        bn_layer1,
        dense_layer2,
        ])

base_learning_rate = 0.001
model.compile(optimizer=tf.keras.optimizers.Adam(lr=base_learning_rate),
              loss='binary_crossentropy',
              metrics=['accuracy'])
model.summary()

model.fit(train_img, train_label, epochs=10, batch_size=16, validation_data = (test_img, test_label))

model.save("TestDetector/Testmodel.h5")
print("모델이 성공적으로 생성되었습니다.")  