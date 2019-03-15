import pickle
import numpy
import time
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
f = open('rawdata.pkl','rb')
a = pickle.load(f)
f.close()
fig=plt.figure()
ax1=fig.add_subplot(111,projection='3d')
features=[]
classes=[]
for e in a:
    asplit=map(int,e.split(",")[0:15])
    features.append(asplit[1:])
    classes.append(asplit[0])
X=TSNE(n_components=3).fit_transform(features)
classified={1:[],2:[],3:[],4:[]}
#classified={1:[],2:[],3:[]}
color=('g','b','r','c')
for i in range(len(classes)):
    if classes[i]==1:
        classified[1].append(X[i])
    elif classes[i]==2:
        classified[2].append(X[i])
    elif classes[i]==3:
        classified[3].append(X[i])
    elif classes[i]==4:
        classified[4].append(X[i])
for i in classified.iterkeys():
    x=[]
    y=[]
    z=[]
    for e in classified[i]:
        x.append(e[0])
        y.append(e[1])
        z.append(e[2])
    ax1.scatter(x,y,z,c=color[i-1])
plt.show()

