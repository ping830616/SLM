# Author | Eduardo Ortega
import pandas as pd
import numpy as np
import tensorflow as tf
import random, sys
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer, MinMaxScaler
from sklearn.pipeline import Pipeline
from datetime import datetime
RANDOM_SEED = 42
VALIDATE_SIZE = 0.2
BATCH = 512
EPOCHS = 100
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)

class autoencoder():
    def __init__(self, x_train, summ=True):
        self.batch_size = BATCH
        self.epochs = EPOCHS
        self.train = x_train
        train, validate = train_test_split(self.train, 
                                test_size=VALIDATE_SIZE,
                                random_state=RANDOM_SEED)
        self.train_split = train
        self.valid_split = validate
        self.pipeline = Pipeline([('normalizer', Normalizer()), 
                                ('scaler', MinMaxScaler())])
        self.pipeline.fit(self.train_split)
        train_transform = self.pipeline.transform(self.train_split)
        valid_transform = self.pipeline.transform(self.valid_split)
        self.train_trans = train_transform
        self.valid_trans = valid_transform
        self.input_dim = self.train_trans.shape[1]
        self.autoencoder = tf.keras.models.Sequential([
                                tf.keras.layers.Dense(self.input_dim, activation='elu', input_shape=(self.input_dim, )),
                                tf.keras.layers.Dense(64, activation='elu'),
                                tf.keras.layers.Dense(32, activation='elu'),
                                tf.keras.layers.Dense(16, activation='elu'),
                                tf.keras.layers.Dense(8, activation='elu'),
                                tf.keras.layers.Dense(4, activation='elu'),
                                tf.keras.layers.Dense(2, activation='elu'),
                                tf.keras.layers.Dense(4, activation='elu'),
                                tf.keras.layers.Dense(8, activation='elu'),
                                tf.keras.layers.Dense(16, activation='elu'),
                                tf.keras.layers.Dense(32, activation='elu'),
                                tf.keras.layers.Dense(64, activation='elu'),
                                tf.keras.layers.Dense(self.input_dim, activation='elu')
                                ])
        self.autoencoder.compile(optimizer="adam",
                                    loss="mse",
                                    metrics=["acc"])
        if summ: self.autoencoder.summary()
        yyyymmddHHMM = datetime.now().strftime('%Y%m%d%H%M')
        log_subdir = f"{yyyymmddHHMM}_batch{BATCH}_layers{len(self.autoencoder.layers)}"
        early_stop = tf.keras.callbacks.EarlyStopping(
                        monitor='val_loss',
                        min_delta=0.0001,
                        patience=10,
                        verbose=1,
                        mode='min',
                        restore_best_weights=True)
        save_model = tf.keras.callbacks.ModelCheckpoint(
                        filepath='autoencoder_best_weights.hdf5',
                        save_best_only=True,
                        monitor='val_loss',
                        verbose=0,
                        mode='min')
        tensorboard = tf.keras.callbacks.TensorBoard(
                        f'logs/{log_subdir}',
                        batch_size=BATCH,
                        update_freq='batch')
        self.cb = [early_stop, save_model, tensorboard]

    def fit(self):
        self.history = self.autoencoder.fit(
                    self.train_trans, 
                    self.train_trans,
                    shuffle=True,
                    epochs=EPOCHS,
                    batch_size=BATCH, # callbacks=self.cb,
                    validation_data=(self.valid_trans, 
                                    self.valid_trans)) 
        return self

    def predict(self, test_data):
        test_trans = self.pipeline.transform(test_data)
        reconstructions = self.autoencoder.predict(test_trans)
        mse = np.mean(np.power(test_trans - reconstructions, 2), axis=1)
        return mse

    def get_memory_size(self):
        #profile = model_profiler(self.autoencoder, BATCH)
        #print(profile)
        '''
        shapes_count = int(np.sum([np.prod(np.array([s if isinstance(s, int) else 1 for s in l.output_shape])) for l in self.autoencoder.layers]))
        memory = 4 * shapes_count
        from keras import backend as K
        trainable_count = int(np.sum([K.count_params(p) for p in set(self.autoencoder.trainable_weights)]))
        non_trainable_count = int(np.sum([K.count_params(p) for p in set(self.autoencoder.non_trainable_weights)]))
        float_type = K.floatx()
        print(float_type)
        quit()
        '''
        bytes_used = get_model_memory_usage(BATCH, self.autoencoder)
        return bytes_used

def get_model_memory_usage(batch_size, model):
    import numpy as np
    try:
        from keras import backend as K
    except:
        from tensorflow.keras import backend as K

    shapes_mem_count = 0
    internal_model_mem_count = 0
    for l in model.layers:
        layer_type = l.__class__.__name__
        if layer_type == 'Model':
            internal_model_mem_count += get_model_memory_usage(batch_size, l)
        single_layer_mem = 1
        out_shape = l.output_shape
        if type(out_shape) is list:
            out_shape = out_shape[0]
        for s in out_shape:
            if s is None:
                continue
            single_layer_mem *= s
        shapes_mem_count += single_layer_mem

    trainable_count = np.sum([K.count_params(p) for p in model.trainable_weights])
    non_trainable_count = np.sum([K.count_params(p) for p in model.non_trainable_weights])

    number_size = 4.0
    if K.floatx() == 'float16':
        number_size = 2.0
    if K.floatx() == 'float32':
        number_size = 4.0
    if K.floatx() == 'float64':
        number_size = 8.0
    total_memory = number_size * (batch_size * shapes_mem_count + trainable_count + non_trainable_count)
    return total_memory + internal_model_mem_count

