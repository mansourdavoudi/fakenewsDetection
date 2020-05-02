import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
import random
from keras import models
from keras import layers
import matplotlib.pyplot as plt


STEP=14

def build_model():

    model = models.Sequential()
    model.add(
        layers.Bidirectional(
            layers.LSTM(
                units=128,
                input_shape=[X.shape[1], X.shape[2]]
            )
        )
    )
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1,activation='sigmoid'))
    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def createee_dataset(fx,tx,step):
  Xs, ys = [], []
  lst = fx.shape[0] + tx.shape[0]
  f_index=0
  t_index=0
  for i in range(0,lst,step):
    rnd=random.randint(0,100)
    if (rnd >= 50 and f_index < fx.shape[0]) or (rnd < 50 and t_index >= tx.shape[0]):
        v = fx.iloc[f_index:(f_index + step)].values
        Xs.append(v)
        ys.append(1)
        f_index+=step

    elif(rnd < 50 and t_index < tx.shape[0]) or (rnd >= 50 and f_index >=f_df.shape[0]):
        v = tx.iloc[t_index:(t_index + step)].values
        Xs.append(v)
        ys.append(0)
        t_index+=step
  return np.array(Xs), np.array(ys)

f_df=pd.read_csv('C:\dataset\lstm\\temp_fake.csv')
t_df=pd.read_csv('C:\dataset\lstm\\temp_real.csv')

scale_column=['TotalNode','Tweets','Retweets','Replies','Height','Frequency','VrfUser','Normal','Leader','Tscore']
scaler = RobustScaler()
scaler = scaler.fit(f_df[scale_column])
f_df.loc[:,scale_column] = scaler.transform(f_df[scale_column].to_numpy())

scale_column=['TotalNode','Tweets','Retweets','Replies','Height','Frequency','VrfUser','Normal','Leader','Tscore']
scaler = RobustScaler()
scaler = scaler.fit(t_df[scale_column])
t_df.loc[:,scale_column] = scaler.transform(t_df[scale_column].to_numpy())

X,y = create_dataset(f_df,t_df,STEP)

x_train=X[0:200,:,:]
y_train=y[0:200]
x_valid=X[200:300,:,:]
y_valid=y[200:300]
x_test=X[300:584,:,:]
y_test=y[300:584]

model = build_model()
history = model.fit(x_train, y_train,
                    epochs=60, batch_size=64, validation_data=(x_valid, y_valid), verbose=0)
history_dict = history.history
# print(history_dict.keys())
# print(history_dict['accuracy'])

history_dict = history.history
acc = history.history['accuracy']
loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']
epochs = range(1, len(acc) + 1)
plt.plot(epochs, loss_values, 'bo', label='Training loss')
plt.plot(epochs, val_loss_values, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()
plt.clf()
acc_values = history_dict['accuracy']
val_acc_values = history_dict['val_accuracy']
epochs = range(1, len(acc) + 1)
plt.plot(epochs, acc_values, 'bo', label='Training accuracy')
plt.plot(epochs, val_acc_values, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

test_result = model.evaluate(x_test, y_test, verbose=0)
print(test_result)







