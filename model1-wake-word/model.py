from tensorflow.keras import models, layers
import tensorflow as tf

#create the CNN
def buildModel():
    model = models.Sequential()
    #build the first conv layer
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 1)))
    model.add(layers.MaxPooling2D(2, 2))

    # second convolutional layer
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D(2, 2))

    # third convolutional layer 
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))

    # from 2D to 1D vector for the dense layer
    model.add(layers.Flatten())  # Create an instance of Flatten

    # dense layers
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=[
            tf.keras.metrics.Recall(),
            tf.keras.metrics.Precision(),
            'accuracy'
        ]
    )

    model.summary()
    
    return model