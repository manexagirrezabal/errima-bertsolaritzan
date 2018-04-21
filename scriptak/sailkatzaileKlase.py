
import sys
import string
import os
import foma
import re

#HOME=os.environ['HOME']
#FST=foma.FST()
#FSM=FST.load(HOME+"/fsttresnak/stemmer.fst")
# def analyzeWord (w):
#     res=FSM.apply_down(w)
#     li=[el for el in res]
#     if li==[]:
#         return w
#     else:
#         return max(li, key=len)


def removePunct (word):
    return re.sub ("[^\w\s\-\']", "", word)

legeFonetikoak = [("tx","S"),
                  ("ts","S"),
                  ("tz","S"),
                  ("rr","R"),
                  ("s","S"),
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
bukaerak="a ak an ean ian ez ik k ko koak n ra rat rik ta tik tzen z".decode("utf8").split(" ") #Orijinala
tartekoak="ai e i l n m o oi r u s z ts tz tx R".decode("utf8").split(" ") #Orijinala
aurrekoak="a ai b d g r alb ald alg e eb ed eg er i is iz o oi op ot ok osp ost osk ozp ozt ozk t k R s z x ts tz tx st sk zt zk u".decode("utf8").split(" ") #Orijinala

bukaerak="a ak an ean ian ez ik k ko koak n ra rat rik ta tik tzen z aino".decode("utf8").split(" ") #Osatua
tartekoak="ai e i l n m o oi r u s z ts tz tx R".decode("utf8").split(" ") #Osatua
aurrekoak="a ai b d g r alb ald alg e eb ed eg er i is iz o oi op ot ok osp ost osk ozp ozt ozk t k R s z x ts tz tx st sk zt zk u".decode("utf8").split(" ") #Osatua

#Urre patroiaren arabera:
bukaerak="a aino ak an ean etan ik ko n ta tan z".decode("utf8").split(" ")
tartekoak="oB B N P PS Pa Po R S TZ a a aino an e en etan i ko l n o ta tan tik to tu tz u".decode("utf8").split(" ")
aurrekoak="B N P PS Po R S SP ST Si TZ ZP a aB aP aS aZP ai aino aio e eB eP eT i iB iP iS itz n o oB ot te u uB".decode("utf8").split(" ")

#Urre patroi osatua:
bukaerak="a aino ak an ean etan ik ko n ta tan z ra".decode("utf8").split(" ")
tartekoak="oB B N P PS Pa Po R S a aino an e en etan i l n o tan tik tu tz u".decode("utf8").split(" ")
aurrekoak="B N P PS Po R S SP ST Si TZ ZP a aB aP aS aZP ai aino aio e eB eP eT i iB iP iS itz n o oB ot te u uB".decode("utf8").split(" ")

#Urre patroiaren eta genituen elementuen konbinazioa:

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
  lines=[removePunct(line) for line in bertsoa.split("\n")]

  bikoitiak=[line for indline,line in enumerate(lines) if indline %2 !=0]

  #print bukaerak

  #print "Bukaera bilatu..."
  puntuBukaerak=[]
  for puntubuk in bikoitiak:
    azkenhitza=puntubuk.split(" ")[-1]
    #azkenlema=analyzeWord(azkenhitza)
    lerrokoBukaerak = [bukaerak[indbukaera] for indbukaera, bukaera in enumerate(bukaerak) if puntubuk.endswith(bukaera)]
    puntuBukaerak.append(set(lerrokoBukaerak))

  print (puntuBukaerak)

  print "Zein da komunean duten bukaera?"
  resultingSet=set(puntuBukaerak[-1])
  for i in xrange(len(puntuBukaerak)-1):
    print (resultingSet)
    resultingSet=resultingSet.intersection(puntuBukaerak[i])

  if list(resultingSet)==[]:
    bukaeraluzeena=""
  else:
    bukaeraluzeena= max(resultingSet, key=len)
  print "Hona bukaera luzeena: ",bukaeraluzeena


  print "Orain tarteko elementuak bilatzera!"
  tartekoTopatuak=[]
  for puntubuk in bikoitiak:
    if len(bukaeraluzeena)!=0:
      puntuBukgabe=puntubuk[:-len(bukaeraluzeena)]
    else:
      puntuBukgabe=puntubuk
    tartekoa = puntubuk[-len(bukaeraluzeena)-1:-len(bukaeraluzeena)]
    tartekoPosibleak = [tartekoak[indtartekoa] for indtartekoa, tartekoa in enumerate(tartekoak) if puntuBukgabe.endswith(tartekoa)]
    tartekoTopatuak.append(set(legeFonetikoakAplikatuLista(tartekoPosibleak)))

  print "Zein da komunean duten tartekoa?"
  resultingTartekoa=set(tartekoTopatuak[-1])
  #print tartekoTopatuak
  for i in xrange(len(tartekoTopatuak)-1):
    print (resultingTartekoa)
    resultingTartekoa=resultingTartekoa.intersection(tartekoTopatuak[i])


  print "Orain aurreko elementuak bilatzera!"
  aurrekoTopatuak=[]
  for puntubuk in bikoitiak:
    if len(bukaeraluzeena)+len(resultingTartekoa)!=0:
      puntuBukgabe=puntubuk[:-(len(bukaeraluzeena)+len(resultingTartekoa))]
    else:
      puntuBukgabe=puntubuk
    tartekoa = puntubuk[-(len(bukaeraluzeena)+len(resultingTartekoa))-1:-(len(bukaeraluzeena)+len(resultingTartekoa))]
    tartekoPosibleak = [aurrekoak[indtartekoa] for indtartekoa, tartekoa in enumerate(aurrekoak) if puntuBukgabe.endswith(tartekoa)]
    aurrekoTopatuak.append(set(legeFonetikoakAplikatuLista(tartekoPosibleak)))

  #print "Zein da komunean duten aurrekoa?"
  resultingAurrekoa=set(aurrekoTopatuak[-1])
  for i in xrange(len(aurrekoTopatuak)-1):
    print (resultingAurrekoa)
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

def ikusiErrimaBerria(bertsoa, legeFonetikoak=legeFonetikoak, aurrekoak=aurrekoak, tartekoak=tartekoak, bukaerak=bukaerak):
  lines=[removePunct(line).replace(" ","") for line in bertsoa.split("\n")]
  linesFonetizatuak = [legeFonetikoakAplikatu(line) for line in lines]

  bikoitiak=[line for indline,line in enumerate(lines) if indline %2 !=0]
  bikoitiFonetizatuak=[line for indline,line in enumerate(linesFonetizatuak) if indline %2 !=0]

#  print (bikoitiak)
  #print (bikoitiFonetizatuak)

  bukaerakFonetizatuta = legeFonetikoakAplikatuLista(bukaerak)
  tartekoakFonetizatuta = legeFonetikoakAplikatuLista(tartekoak)
  aurrekoakFonetizatuta = legeFonetikoakAplikatuLista(aurrekoak)

  #BILATU BUKAERAK
  bertsokoBukaerak=set(bukaerakFonetizatuta)
  for line in bikoitiFonetizatuak:
  	#Egiaztatu ea uneko lerro bikoitiak adierazitako bukaera duen. Baldin badu, gorde!
    lerrokoBukaerak = [bukaera for bukaera in bukaerakFonetizatuta if line.endswith(bukaera)]
    bertsokoBukaerak = bertsokoBukaerak.intersection(set(lerrokoBukaerak))
  if len(bertsokoBukaerak)!=0:
    bukaeraKomunLuzeena = max(bertsokoBukaerak, key=len)
  else:
    bukaeraKomunLuzeena=""
#  print (bukaeraKomunLuzeena)
  bukaerarenLuzera=len(bukaeraKomunLuzeena)

  #KENDU BUKAERAK LERRO BIKOITI FONETIZATUEI
  for indline, line in enumerate(bikoitiFonetizatuak):
    bikoitiFonetizatuak[indline]=bikoitiFonetizatuak[indline][:len(bikoitiFonetizatuak[indline])-bukaerarenLuzera]
    #print (bikoitiFonetizatuak[indline])

  #BILATU TARTEKOAK
  bertsokoTartekoak=set(tartekoakFonetizatuta)
  for line in bikoitiFonetizatuak:
    lerrokoTartekoak = [tarteko for tarteko in tartekoakFonetizatuta if line.endswith(tarteko)]
    bertsokoTartekoak = bertsokoTartekoak.intersection(set(lerrokoTartekoak))
  if len(bertsokoTartekoak)!=0:
  	tartekoKomunLuzeena = max(bertsokoTartekoak, key=len)
  else:
  	tartekoKomunLuzeena=""
#  print (tartekoKomunLuzeena)
  tartekoarenLuzera=len(tartekoKomunLuzeena)

  #KENDU BUKAERAK LERRO BIKOITI FONETIZATUEI
  for indline, line in enumerate(bikoitiFonetizatuak):
    bikoitiFonetizatuak[indline]=bikoitiFonetizatuak[indline][:len(bikoitiFonetizatuak[indline])-tartekoarenLuzera]
#    print (bikoitiFonetizatuak[indline])


  #BILATU AURREKOAK
  bertsokoAurrekoak=set(aurrekoakFonetizatuta)
  for line in bikoitiFonetizatuak:
    lerrokoAurrekoak = [aurreko for aurreko in aurrekoakFonetizatuta if line.endswith(aurreko)]
    bertsokoAurrekoak = bertsokoAurrekoak.intersection(set(lerrokoAurrekoak))
  if len(bertsokoAurrekoak)!=0:
    aurrekoKomunLuzeena = max(bertsokoAurrekoak, key=len)
  else:
    aurrekoKomunLuzeena=""
#  print (aurrekoKomunLuzeena)
  aurrekoarenLuzera=len(aurrekoKomunLuzeena)

  if bukaeraKomunLuzeena=='':
    bukaeraKomunLuzeena='0'
  if tartekoKomunLuzeena=='':
    tartekoKomunLuzeena="0"
  if aurrekoKomunLuzeena=='':
    aurrekoKomunLuzeena='0'

  return [aurrekoKomunLuzeena,tartekoKomunLuzeena,bukaeraKomunLuzeena]

if __name__=='__main__':
  try:
    f=open (sys.argv[1])
    rawlines="\n".join([line.decode("utf8").rstrip() for line in f])
    f.close()
#    rawlines = sys.argv[1].replace(" ","\n")
    result=ikusiErrimaBerria(rawlines, legeFonetikoak=legeFonetikoak, aurrekoak=aurrekoak, tartekoak=tartekoak, bukaerak=bukaerak)
    print ("-".join(result), result)
    #print (legeFonetikoakAplikatu("etxera noa azkar, lagunak batera. txakurra eraman dut beterinariora"))
    print
  except ValueError:
    print "---"+"kaka"
    print 

