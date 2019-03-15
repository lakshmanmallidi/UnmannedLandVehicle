import pickle
import numpy
import time
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
f = open('rawdata.pkl','rb')
a = pickle.load(f)
f.close()
features=[]
classes=[]
for e in a:
    asplit=map(int,e.split(",")[0:15])
    features.append(asplit[1:])
    classes.append(asplit[0])
    
X=TSNE(n_components=2).fit_transform(features)
classified={1:[],2:[],3:[],4:[]}
color=('g','b','r','c')
for i in range(len(classes)):
    if classes[i]==1:
        classified[1].append(X[i])
    elif classes[i]==2:
        classified[2].append(X[i])
    elif classes[i]==3:
        classified[3].append(X[i])
    elif classes[i]==4:
        classified[4].apppend(X[i])

for i in classified.iterkeys():
    x=[]
    y=[]
    for e in classified[i]:
        x.append(e[0])
        y.append(e[1])
    plt.scatter(x,y,c=color[i-1])
plt.show()

