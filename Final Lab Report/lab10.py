import numpy as np
import pandas as pd
from keras import layers
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import tensorflow.keras.models as models
from sklearn.preprocessing import MinMaxScaler
import csv
from sklearn.metrics import confusion_matrix
from tensorflow import losses, optimizers

read_file = pd.read_csv('risk-train.csv')
data = pd.DataFrame(read_file)

dropping_list = []
for column in data.columns:
    count = 0
    for value in data[column]:
        if value == '?':
            count += 1
    if (count / len(data)) > 0.4:
        data.drop(columns=[column])
        dropping_list.append(column)
        print("Drop column" , column)

data_2 = data.drop(columns=dropping_list)

dropping_list = []
for column in data_2.columns:
    count = 0
    for value in data_2[column]:
        if value == '?':
            count += 1
    print(column, count)

data_3 = data_2.drop(columns=['B_BIRTHDATE'])
data_3['TIME_ORDER'] = data_3['TIME_ORDER'].replace('?', '00:00')

categorical = data_3.dtypes[data_3.dtypes == "object"].index

lb = preprocessing.LabelEncoder()

data_3['B_EMAIL'] = lb.fit_transform(data_3['B_EMAIL'])
data_3['B_TELEFON'] = pd.get_dummies(data_3['B_TELEFON'])
data_3['CLASS'] = pd.get_dummies(data_3['CLASS'])

numerical = data_3.dtypes[data_3.dtypes != "object"].index

x_data = np.array(data_3[numerical])
y_data = np.array(data_3['CLASS'])

x_data_train, x_data_test, y_data_train, y_data_test = train_test_split(x_data, y_data, test_size=0.3)

test_data_orderID = []
# extracting order ids
for arr in x_data_test:
    test_data_orderID.append(arr[0])
# normalizing data for better training and output
scalar = MinMaxScaler()
x_data_train = scalar.fit_transform(x_data_train)
x_data_test = scalar.fit_transform(x_data_test)

# loading the saved models
reconstructed_model1 = models.load_model("seqModel1")
reconstructed_model2 = models.load_model("seqModel2")

# making the predictions on test data
x_data_test = np.array(x_data_test)
predictions1 = reconstructed_model1.predict_classes(x_data_test)
predictions2 = reconstructed_model2.predict_classes(x_data_test)

# outputting predictions to csv file
with open("pred1.csv", 'w') as file:
    writer = csv.writer(file)
    writer.writerow(["ORDER-ID", "CLASS"])
    for i in range(0, len(predictions1)):
        if predictions1[i] == 1:
            writer.writerow([test_data_orderID[i], "no"])
        else:
            writer.writerow([test_data_orderID[i], "yes"])

with open("pred2.csv", 'w') as file:
    writer = csv.writer(file)
    writer.writerow(["ORDER-ID", "CLASS"])
    for i in range(0, len(predictions2)):
        if predictions2[i] == 1:
            writer.writerow([test_data_orderID[i], "no"])
        else:
            writer.writerow([test_data_orderID[i], "yes"])

# print accuracy of both models
acc = reconstructed_model1.evaluate(x_data_test, y_data_test)
print("Accuracy for model trained using a fixed learning rate", acc[1] * 100, "%")

acc1 = reconstructed_model2.evaluate(x_data_test, y_data_test)
print("Accuracy for model trained using the Adam optimizer (changing learning rate)", acc1[1] * 100, "%")

# model = models.Sequential([
#     layers.Input(shape=(11,)),
#     layers.Dense(1)
# ])
#
# model.compile(
#     metrics=['accuracy'],
#     loss=losses.BinaryCrossentropy(),
#     optimizer=optimizers.SGD(learning_rate=0.001)
# )
#
# model.fit(x_data_train, y_data_train, epochs=10)
#
# acc = model.evaluate(x_data_test, y_data_test)
#
# model.save("seqModel1")
# print(acc)

# model2 = models.Sequential([
#     layers.Input(shape=(11,)),
#     layers.Dense(1)
# ])
#
# model2.compile(
#     metrics=['accuracy'],
#     loss = losses.BinaryCrossentropy(),
#     optimizer=optimizers.Adam()
# )
#
# model2.fit(x_data_train, y_data_train, epochs=20)
#
# acc = model2.evaluate(x_data_test, y_data_test)
#
# model2.save("seqModel2")
# print(acc)

