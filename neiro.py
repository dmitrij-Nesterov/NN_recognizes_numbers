from time import perf_counter
import numpy as np
from tensorflow.keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Dropout
from tensorflow import keras


x_train, y_train = np.load('Traning_inputs.npz').values()

x_train = np.expand_dims(x_train, axis=3)
y_train = keras.utils.to_categorical(y_train, 10)

model = keras.Sequential([
    Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(25, 25, 1)),
    Conv2D(32, (3, 3), padding='same', activation='relu'),
    MaxPooling2D((2, 2), strides=2),
    Flatten(),
    Dense(125 , activation='relu'),
    Dense(10, activation='softmax')
])
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

his = model.fit(x_train, y_train, batch_size=30, epochs=9, validation_split=0.1)

model.save('model')