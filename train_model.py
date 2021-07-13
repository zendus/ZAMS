from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import argparse
import pickle

#construct the argument parser and parse the argument
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--embeddings", required=True, help="path to serialized db of facial embeddings")
ap.add_argument("-r", "--recognizer", required=True, help="path to output model trained to recognize faces")
ap.add_argument("-l", "--le", required=True, help="path to output label encoder")
args = vars(ap.parse_args())

#load face embeddings
print("[INFO] loading face embeddings ...")
data = pickle.loads(open(args["embeddings"], "rb").read())

#encode the labels
print("[INFO] encoding labels ...")
le = LabelEncoder()
labels = le.fit_transform(data["names"])

#training svm model
print("[INFO] training model ...")
recognizer = SVC(kernel="linear", probability=True)
recognizer.fit(data["embeddings"], labels)
print("[INFO] training done.")

#write the actual face recognition model to disk
print(["[INFO] writing model to disk ..."])
f = open(args["recognizer"], "wb")
f.write(pickle.dumps(recognizer))
f.close()
print("[INFO] writing done.")

#write the label encoder to disk
print("[INFO] writing label encoder to disk ...")
f = open(args["le"], "wb")
f.write(pickle.dumps(le))
f.close()
print("DONE !!!")