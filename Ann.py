from keras import models
from keras import layers
import numpy as np
import matplotlib.pyplot as plt

def build_model():

    model = models.Sequential()
    model.add(layers.Dense(128, activation='relu', input_shape=(32,)))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(1,activation='sigmoid'))
    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
    return model

train_data=np.genfromtxt("C:\dataset\data\\train_data.csv",delimiter=",")
train_lable=np.genfromtxt("C:\dataset\data\\train_lable.csv",delimiter=",")
test_data=np.genfromtxt("C:\dataset\data\\test_data.csv",delimiter=",")
test_lable=np.genfromtxt("C:\dataset\data\\test_lable.csv",delimiter=",")

k = 3
num_val_samples = len(train_data) // k
num_epochs = 100
all_scores = []
for i in range(k):
    print('processing fold #', i)
    val_data = train_data[i * num_val_samples: (i + 1) * num_val_samples]
    val_targets = train_lable[i * num_val_samples: (i + 1) * num_val_samples]

    partial_train_data = np.concatenate(
        [train_data[:i * num_val_samples],
         train_data[(i + 1) * num_val_samples:]],
        axis=0)
    partial_train_targets = np.concatenate(
        [train_lable[:i * num_val_samples],
         train_lable[(i + 1) * num_val_samples:]],
        axis=0)
    model = build_model()
    history=model.fit(partial_train_data, partial_train_targets,
              epochs=num_epochs, batch_size=20,validation_data=(val_data,val_targets), verbose=0)
    history_dict = history.history
    #print(history_dict.keys())
    #print(history_dict['accuracy'])

    history_dict = history.history
    acc = history.history['accuracy']
    loss_values = history_dict['loss']
    val_loss_values = history_dict['val_loss']
    epochs = range(1, len(acc)+1)
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
    epochs = range(1, len(acc)+1)
    plt.plot(epochs, acc_values, 'bo', label='Training accuracy')
    plt.plot(epochs, val_acc_values, 'b', label='Validation accuracy')
    plt.title('Training and validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()

   # all_scores.append(result)
test_result = model.evaluate(test_data, test_lable, verbose=0)
print((test_result,"------------"))










