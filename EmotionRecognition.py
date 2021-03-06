'''
Data set introduction
The data consists of 48x48 pixel grayscale images of faces
0=Angry, 1=Disgust, 2=Fear, 3=Happy, 4=Sad, 5=Surprise, 6=Neutral
The faces have been automatically registered so that the face is more or less centered
and occupies about the same amount of space in each image
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

print("\n-----DATASET INFO-----")
''' ### Read csv data '''
df = pd.read_csv('datasets/fer2013/train.csv')
print("There are total ", len(df), " sample in the loaded dataset.")
print("The size of the dataset is: ", df.shape)
# get a subset of the whole data for now
df = df.sample(frac=0.1, random_state=46)
print("The size of the dataset subset is: ", df.shape)
#get our test set
our_df = pd.read_csv('datasets/fer2013/our_test.csv')

''' Extract images and label from the dataframe df '''
width, height = 48, 48
images = df['pixels'].tolist()
our_images = our_df['pixels'].tolist()
faces = []
our_faces = []
for sample in images:
    face = [int(pixel) for pixel in sample.split(' ')]  # Splitting the string by space character as a list
    face = np.asarray(face).reshape(width*height)       # convert pixels to images and # Resizing the image
    faces.append(face.astype('float32') / 255.0)       # Normalization
faces = np.asarray(faces)
for sample in our_images:
    face = [int(pixel) for pixel in sample.split(' ')]  # Splitting the string by space character as a list
    face = np.asarray(face).reshape(width*height)       # convert pixels to images and # Resizing the image
    our_faces.append(face.astype('float32') / 255.0)       # Normalization
our_faces = np.asarray(our_faces)

# Get labels
y = df['emotion'].values

class_names = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
# Visualization a few sample images
plt.figure(figsize=(5, 5))
for i in range(30):
    plt.subplot(5, 6, i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(np.squeeze(faces[i].reshape(width, height)), cmap='gray')
    plt.xlabel(class_names[y[i]])
plt.show()

print("\n-----TRAINING AND TEST SET SHAPES-----")
## Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(faces, y, test_size=0.4, random_state=46)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

#Train Naive Bayes Classifier
gnb = GaussianNB()
y_pred = gnb.fit(X_train, y_train).predict(X_test)

print("\n-----GAUSSIAN BAYES CONFUSION MATRIX AND CLASSIFICATION REPORT-----")
# For classification tasks some commonly used metrics are confusion matrix, precision, recall, and F1 score.
# These are calculated by using sklearn's metrics library contains the classification_report and confusion_matrix methods
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred, labels=np.unique(y_pred)))

#our test Naive Bayes
y_pred = gnb.predict(our_faces)

print("\n-----GAUSSIAN BAYES OUR TEST-----")
# For classification tasks some commonly used metrics are confusion matrix, precision, recall, and F1 score.
# These are calculated by using sklearn's metrics library contains the classification_report and confusion_matrix methods
print(confusion_matrix(our_df['emotion'].values, y_pred))
print(classification_report(our_df['emotion'].values, y_pred, labels=np.unique(y_pred)))

#Train SVC Classifier
svclassifier = SVC(kernel='linear')
svclassifier.fit(X_train, y_train)

# Now that our classifier has been trained, let's make predictions on the test data. To make predictions, the predict method of the DecisionTreeClassifier class is used.
y_pred = svclassifier.predict(X_test)

print("\n-----SVC CONFUSION MATRIX AND CLASSIFICATION REPORT-----")
# For classification tasks some commonly used metrics are confusion matrix, precision, recall, and F1 score.
# These are calculated by using sklearn's metrics library contains the classification_report and confusion_matrix methods
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred, labels=np.unique(y_pred)))

#our test prototype
y_pred = svclassifier.predict(our_faces)

print("\n-----SVC OUR TEST-----")
# For classification tasks some commonly used metrics are confusion matrix, precision, recall, and F1 score.
# These are calculated by using sklearn's metrics library contains the classification_report and confusion_matrix methods
print(confusion_matrix(our_df['emotion'].values, y_pred))
print(classification_report(our_df['emotion'].values, y_pred, labels=np.unique(y_pred)))

#Train Neural Net Classifier
clf = MLPClassifier(solver='lbfgs', max_iter=10000, alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
y_pred = clf.fit(X_train, y_train).predict(X_test)

print("\n-----NEURAL NETWORK CONFUSION MATRIX AND CLASSIFICATION REPORT-----")
# For classification tasks some commonly used metrics are confusion matrix, precision, recall, and F1 score.
# These are calculated by using sklearn's metrics library contains the classification_report and confusion_matrix methods
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred, labels=np.unique(y_pred)))

#our test Neural Net
y_pred = clf.predict(our_faces)

print("\n-----NEURAL NETWORK OUR TEST-----")
# For classification tasks some commonly used metrics are confusion matrix, precision, recall, and F1 score.
# These are calculated by using sklearn's metrics library contains the classification_report and confusion_matrix methods
print(confusion_matrix(our_df['emotion'].values, y_pred))
print(classification_report(our_df['emotion'].values, y_pred, labels=np.unique(y_pred)))
