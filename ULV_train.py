import pickle
from sklearn import svm,naive_bayes,ensemble
from sklearn.metrics import accuracy_score
import numpy
import time

f = open('rawdata.pkl','rb')
a = pickle.load(f)
f.close()
per=80
n=10
avgscore=0
fit_time=0
predict_time=0
lendset=len(a)
lentset=int(lendset*per)/100
maxclf=None
maxscore=0
print "length of training set:",lendset-lentset,"\nlength of testing set:",lentset
for _ in range(n):
    numpy.random.shuffle(a)
    features=[]
    classes=[]
    for e in a:
        asplit=map(int,e.split(",")[0:15])
        features.append(asplit[1:])
        classes.append(asplit[0])
    train_features,train_classes,test_features,test_classes=features[:-lentset],classes[:-lentset],features[-lentset:],classes[-lentset:]
    #clf=svm.SVC()
    clf=naive_bayes.GaussianNB()
    #clf=ensemble.RandomForestClassifier()
    t=time.time()
    clf.fit(train_features,train_classes)
    fit_time=fit_time+(time.time()-t)
    t=time.time()
    pred_classes=[]
    for e in test_features:
        pred_classes.append(clf.predict([e])[0])
    score = accuracy_score(pred_classes,test_classes)*100
    predict_time=predict_time+(time.time()-t)
    '''for i in range(len(test_classes)):
        print pred_classes[i]
        print test_classes[i]'''
    avgscore=avgscore+score
    if(score>maxscore):
        maxscore=score
        maxclf=clf
#print "\nfitting time :",fit_time,"\npredicting time :",predict_time
print "Average Accuracy:",avgscore/n,"\nfitting time :",fit_time,"\npredicting time :",predict_time
print "highest Accuracy:",maxscore
f = open("trainedclf.pkl",'wb')
pickle.dump(maxclf,f)
f.close()
