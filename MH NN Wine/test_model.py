import numpy as np
from keras.callbacks import ModelCheckpoint
from sklearn import preprocessing
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD
from keras.optimizers import RMSprop
from keras.optimizers import Adagrad
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt

def import_file(filename):
    raw_data = open(filename, 'rb')
    data = np.loadtxt(raw_data, delimiter=";")
    return data

# Regularize columns of the data between 0-1.
def regularize_data(data):
    X_train = data
    min_max_scaler = preprocessing.MinMaxScaler()
    X_train_minmax = min_max_scaler.fit_transform(X_train)
    all_data = X_train_minmax
    return all_data

# Shuffle/Randomize data. Only rows shuffled.
def shuffled_data(data):
    # np.random.shuffle(data)
    # return data
    return np.random.shuffle(data)

# Splitting up data set into 3 descrete data sets of Training, Validation, and Testing data sets.
def data_sets(data, train_size, validation_size, test_size):
    # Number of rows for whole data set.
    rows = data.shape[0]

    # Number of rows for new data sets.
    rows_train = round(rows * train_size)
    rows_validation = round(rows * validation_size)
    rows_test = round(rows * test_size)

    # Parsing out the Training data from the original data set.
    train_data = data[0:rows_train]
    # Parsing out the Validation data from the original data set.
    validation_data = data[(rows_train):(rows_train + rows_validation)]
    # Parsing out the Test data from the original data set.
    test_data = data[(rows_train + rows_validation):(rows_train + rows_validation + rows_validation + rows_test)]
    # Return a 2n-dimensional array for each data set.
    return train_data, validation_data, test_data

def split_data(data):
    # ???????????????????????????????????????????????????????????????????????
    # Number of rows for whole data set.
    rows, columns = data.shape
    # Select out Features set (inputs, X).
    X = data[:,:columns-1]
    # Select out output (y).
    y = data[:,columns-1]
    return X, y

def modeling(data_set, train_size, validation_size, test_size, iterations, batch_size, checkpointer, nods_per_layer, plot_name):
    # treate data
    reg_data = regularize_data(data_set)
    shuf_data = shuffled_data(reg_data)

    # Parse out data sets.
    train_data, validation_data, test_data = data_sets(shuf_data, train_size, validation_size, test_size)

    # Split data sets into input(X) (matrix) and output(y) (single float)
    X_train, y_train = split_data(train_data)
    X_val, y_val = split_data(validation_data)
    X_test, y_test = split_data(test_data)

    # Building Nueral Net Model
    feature_input = X_train.shape[1]
    output_dim = 1
    # building a 2 layer NN
    model = Sequential()
    model.add(Dense(output_dim=nods_per_layer, input_dim=feature_input, activation="sigmoid"))
    model.add(Dense(output_dim=output_dim, input_dim=nods_per_layer, activation="sigmoid"))

    # List of optimizers
    adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
    ada = Adagrad(lr=0.01, epsilon=1e-08, decay=0.0)
    rms = RMSprop(lr=0.01, rho=0.9, epsilon=1e-08, decay=0.0)
    sgd = SGD(lr=0.1, momentum=0.01, decay=0.001, nesterov=False)

    # compile model
    model.compile(loss='mean_squared_error', optimizer=adam, metrics=['accuracy'])

    # train model
    history = model.fit(X_train, y_train, validation_data=(X_val, y_val), nb_epoch=iterations, batch_size=batch_size, callbacks=[checkpointer])

    # evaluate Model
    scores = model.evaluate(X_test, y_test, verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

    # secondary evaluation
    predictions = model.predict( X_test, batch_size=1, verbose=0)
    diff = np.divide(np.abs(np.subtract(predictions, y_test)),y_test)*100
    accuracy = 100 - np.mean(diff)
    print('Accuracy (%)', accuracy)

    # print cross-validation data loss and test data loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['Train Data', 'Cross-Validation Data'], loc='upper left')
    plt.savefig(plot_name, bbox_inches='tight')
    plt.clf()

    return accuracy, scores

def run(data_file, train_size, validation_size, test_size, iterations, batch_size, nods_per_layer, weight_file_name, plot_name):
    # import data
    data_set = import_file(data_file)

    # save best model in weight file
    checkpointer = ModelCheckpoint(filepath=weight_file_name, verbose=1, save_best_only=True)

    # run model off of data set
    model = modeling(data_set, train_size, validation_size, test_size, iterations, batch_size, checkpointer, nods_per_layer, plot_name)

    return model

if __name__ == '__main__':
    # Default Variables
    data_file = 'wine_data.csv'
    train_size = 0.60
    validation_size = 0.20
    test_size = 0.20
    iterations = 100
    batch_size = 20
    nods_per_layer = 30
    weight_file_name = "weights.hdf5"
    plot_name = "test.pdf"

    print(run(data_file, train_size, validation_size, test_size, iterations, batch_size, nods_per_layer, weight_file_name, plot_name))
