from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sys

from sailkatzaileKlase import legeFonetikoakAplikatu

goldf=open(sys.argv[1])
goldlines = [legeFonetikoakAplikatu(line.rstrip().lower()) for line in goldf]
goldf.close()

predf=open(sys.argv[2])
predlines = [line.rstrip() for line in predf]
predf.close()

labels=list(set(goldlines))

print (classification_report(goldlines, predlines))
print (accuracy_score(goldlines, predlines))

#for indl, l in enumerate(labels):
#	print (indl, l)

#confmat = confusion_matrix(goldlines, predlines, labels=labels)

#print (np.argmax(np.sum(confmat, axis=0))) #Harrapatu gehienetan egiten dugun errorea. Hasieran 'E-R-R-O-R-E-A'
#print (confmat[:,49])
#print (np.argmax(confmat[:,49])) #Zein da itzuli beharkogenukeen balioa, hau da, urre patroian dagoena?

#plt.imshow(confmat)
#plt.colorbar()
#plt.show()

