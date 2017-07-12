
import sys
import string
import os
import foma

HOME=os.environ['HOME']
FST=foma.FST()
FSM=FST.load(HOME+"/fsttresnak/stemmer.fst")
def analyzeWord (w):
    res=FSM.apply_down(w)
    li=[el for el in res]
    if li==[]:
        return w
    else:
        return max(li, key=len)


def removePunct (st):
  return ''.join([char for char in st if char not in string.punctuation])

legeFonetikoak = [("s","S"),
                  ("z","S"),
                  ("x","S"),
                  ("p","P"),
                  ("t","P"),
                  ("k","P"),
                  ("b","B"),
                  ("d","B"),
                  ("g","B"),
                  ("r","B"),
                  ("m","N"),
                  ("n","N")]
bukaerak="a ak an ean ian ez ik k ko koak n ra rat rik ta tik tzen z".decode("utf8").split(" ")
tartekoak="ai e i l n m o oi r u s z ts tz tx R".decode("utf8").split(" ")
aurrekoak="a ai b d g r alb ald alg e eb ed eg er i is iz o oi op ot ok osp ost osk ozp ozt ozk t k R s z x ts tz tx st sk zt zk u".decode("utf8").split(" ")


#HORRELA DEITU: for i in bertsoa*; do cat $i; python sailkatzaileKlase.py "$i"; done

def legeFonetikoakAplikatu(w):
    for lege in legeFonetikoak:
      w=  w.replace(lege[0],lege[1])
    return w


def legeFonetikoakAplikatuLista(lista):
    return [legeFonetikoakAplikatu(w) for w in lista]



def ikusiErrimaWeb(bertsoa, aurrekoakZerr, tartekoakZerr, bukaerakZerr, legeFonetikoakZerr=legeFonetikoak):
  aurrekoak=aurrekoakZerr.decode("utf8").split(" ")
  tartekoak=tartekoakZerr.decode("utf8").split(" ")
  bukaerak=bukaerakZerr.decode("utf8").split(" ")
  return ikusiErrima (bertsoa, legeFonetikoak, aurrekoak, tartekoak, bukaerak)


def ikusiErrima(bertsoa, legeFonetikoak=legeFonetikoak, aurrekoak=aurrekoak, tartekoak=tartekoak, bukaerak=bukaerak):
  lines=[removePunct(line.replace("rr","R")) for line in bertsoa.split("\n")]

  #print "aurrekoak:",aurrekoak
  #print "tartekoak:",tartekoak
  #print "bukaerak:",bukaerak

#  for line in lines:
#    print line
#  raw_input()

  bikoitiak=[line for indline,line in enumerate(lines) if indline %2 !=0]

  #print bukaerak

  #print "Bukaera bilatu..."
  puntuBukaerak=[]
  for puntubuk in bikoitiak:
#    print puntubuk
    azkenhitza=puntubuk.split(" ")[-1]
    azkenlema=analyzeWord(azkenhitza)
    lerrokoBukaerak = [bukaerak[indbukaera] for indbukaera, bukaera in enumerate(bukaerak) if puntubuk.endswith(bukaera)]
    puntuBukaerak.append(set(lerrokoBukaerak))
#    print azkenhitza, azkenlema
#    print

  #print "Zein da komunean duten bukaera?"
  resultingSet=set(puntuBukaerak[-1])
  #print puntuBukaerak
  for i in xrange(len(puntuBukaerak)-1):
    resultingSet=resultingSet.intersection(puntuBukaerak[i])

  if list(resultingSet)==[]:
    bukaeraluzeena=""
  else:
    bukaeraluzeena= max(resultingSet, key=len)
  #print "Hona bukaera luzeena: ",bukaeraluzeena


  #print "Orain tarteko elementuak bilatzera!"
  tartekoTopatuak=[]
  for puntubuk in bikoitiak:
#    print puntubuk
    if len(bukaeraluzeena)!=0:
      puntuBukgabe=puntubuk[:-len(bukaeraluzeena)]
    else:
      puntuBukgabe=puntubuk
#    print puntuBukgabe
    tartekoa = puntubuk[-len(bukaeraluzeena)-1:-len(bukaeraluzeena)]
    tartekoPosibleak = [tartekoak[indtartekoa] for indtartekoa, tartekoa in enumerate(tartekoak) if puntuBukgabe.endswith(tartekoa)]
    tartekoTopatuak.append(set(legeFonetikoakAplikatuLista(tartekoPosibleak)))
#    print tartekoTopatuak
#    print

  #print "Zein da komunean duten tartekoa?"
  resultingTartekoa=set(tartekoTopatuak[-1])
  #print tartekoTopatuak
  for i in xrange(len(tartekoTopatuak)-1):
    resultingTartekoa=resultingTartekoa.intersection(tartekoTopatuak[i])


  #print "Orain aurreko elementuak bilatzera!"
  aurrekoTopatuak=[]
  for puntubuk in bikoitiak:
#    print puntubuk,(len(bukaeraluzeena)+len(resultingTartekoa))
    if len(bukaeraluzeena)+len(resultingTartekoa)!=0:
      puntuBukgabe=puntubuk[:-(len(bukaeraluzeena)+len(resultingTartekoa))]
    else:
      puntuBukgabe=puntubuk
#    print puntuBukgabe
    tartekoa = puntubuk[-(len(bukaeraluzeena)+len(resultingTartekoa))-1:-(len(bukaeraluzeena)+len(resultingTartekoa))]
    tartekoPosibleak = [aurrekoak[indtartekoa] for indtartekoa, tartekoa in enumerate(aurrekoak) if puntuBukgabe.endswith(tartekoa)]
    aurrekoTopatuak.append(set(legeFonetikoakAplikatuLista(tartekoPosibleak)))
#    print aurrekoTopatuak
#    print

  #print "Zein da komunean duten aurrekoa?"
  resultingAurrekoa=set(aurrekoTopatuak[-1])
  #print aurrekoTopatuak
  for i in xrange(len(aurrekoTopatuak)-1):
    resultingAurrekoa=resultingAurrekoa.intersection(aurrekoTopatuak[i])


  #print "Hona bukaera luzeena: ",bukaeraluzeena
  if list(resultingTartekoa)==[]:
    tartekoluzeena="0"
  else:
    tartekoluzeena= max(resultingTartekoa, key=len)
  #print "Hona tarteko luzeena: ",tartekoluzeena


  if bukaeraluzeena=='':
    bukaeraluzeena='0'
  if resultingAurrekoa==[]:
    aurrekoLuzeena="0"
  else:
    aurrekoLuzeena=max(resultingAurrekoa, key=len)
#  print aurrekoLuzeena + " " + tartekoluzeena + " " + bukaeraluzeena

  return (aurrekoLuzeena,tartekoluzeena,bukaeraluzeena)


if __name__=='__main__':
  try:
    f=open (sys.argv[1])
    rawlines="\n".join([line.decode("utf8").rstrip() for line in f])
    f.close()
    result=ikusiErrima(rawlines, legeFonetikoak=legeFonetikoak, aurrekoak=aurrekoak, tartekoak=tartekoak, bukaerak=bukaerak)
    print "---"+" ".join(result)
    print
  except ValueError:
    print "---"+"kaka"
    print 

