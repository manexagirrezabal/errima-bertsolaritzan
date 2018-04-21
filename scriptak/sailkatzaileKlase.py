#!/usr/bin/python
# -*- coding: utf-8 -*-

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


eine="ñ".decode("utf8")
def removePunct (word):
    return re.sub ("[^\w\s\-\']", "", word)

def removePunct_spaces (word):
    return re.sub ("[^\w\-\'"+eine+"]", "", word)

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
                  ("n","N"),
                  ("ñ","iN")]
legeFonetikoak = [(lege[0].decode("utf8"), lege[1]) for lege in legeFonetikoak]

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
  lines=[removePunct_spaces(line) for line in bertsoa.split("\n")]
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
  bertsokoTartekoakZerrenda_pos=[]
  for indline,line in enumerate(bikoitiFonetizatuak):
    lerrokoTartekoak_tupla = [(tarteko,indline) for tarteko in tartekoakFonetizatuta if line.endswith(tarteko)]
    lerrokoTartekoak = [t[0] for t in lerrokoTartekoak_tupla]

    #Honek lerro bakoitzean dauden tarteko posibleak itzuliko dizkigu.
    #Hauek zerrenda batean sartu behar ditugu gero horiekin jolastu ahal izateko.
    if (len(lerrokoTartekoak)==0):
      bertsokoTartekoakZerrenda_pos.extend([(line[-1],indline)])
    else:
      bertsokoTartekoakZerrenda_pos.extend(lerrokoTartekoak_tupla)
    tartekoBakanak= set(lerrokoTartekoak)

    bertsokoTartekoak = bertsokoTartekoak.intersection(set(lerrokoTartekoak))



  tartpos = set([buk[0] for buk in bertsokoTartekoakZerrenda_pos])
  bertsokoTartekoakZerrenda = [buk[0] for buk in bertsokoTartekoakZerrenda_pos]
  tarteko_maizt = [(tart, bertsokoTartekoakZerrenda.count(tart)) for tart in tartpos]
  kengarri = min(tarteko_maizt,  key= lambda t: t[1]) #Preszindiblea den letra eta bere lerro zenbakia bilatu
  kenezin = max(tarteko_maizt,  key= lambda t: t[1]) 

  #Kengarria eta kenezina kalkulatuta, ideia honakoa da.
  #Kengarria apeta, seka, gerta... bezalako kasuetan agertzen den "r" letra izango da
  #Kenezina, berriz, "e" letra. Orain, egingo duguna da "r" hori agertzen den bakoitzean,
  #hori kendu eta ea "e" bat lor dezakegun ikusi.
  #Nahiko ad-hoc soluzioa da, baina gure arazoa konpon dezakelakoan nago. Ikus dezagun!



  #Ondo! Orain kasuistikaren arabera jokatu behar dugu.
  #1.- Batetik, kasu arruntetan horrelakoak izango ditugu:
  #[[(u'B', 0)], [(u'B', 1)], [(u'B', 2)], [(u'B', 3)]]
# Zazpi neskatill eder
# aukera-maukeran
# Ortik pentsatu zuek
# nolakuak geran;
# Azpillaga, jarri bear
# neskatako eran,
# orain epoka dek eta
# ia saiatzen geran.
  #2.- Kasu berezixeagoa litzateke:
  #[[(u'a', 0)], [(u'Pa', 1), (u'a', 1)], [(u'a', 2)], [(u'Pa', 3), (u'a', 3)]]
# Ez dezu ondo gaurkoz dantzatu,
# aita, zeorren mingaina,
# amak umea maitatutzen du
# sarri aita batek aina;
# zuregandikan apartatzeko
# gogua badaukat baina,
# nik ere errez jaso niteke
# nere semetxo apaina.
  #3.-eta are bereziagoa, baina tratatu beharrekoa:
  #[[(u'e', 0)], [(u'B', 1)], [(u'e', 2)], [(u'e', 3)]]
  #Ez dauka zertan beharra izan
# izan liteke apeta
# nik azalpenik eman beharrik
# ez daukat baina zer gerta.
# Agur laztana joan egin behar dut
# agenda daukat beteta
# Strauss-Khan eta bere lagunak
# zerbitu behar ditut eta.


  if len(bertsokoTartekoak)!=0:
  	tartekoKomunLuzeena = max(bertsokoTartekoak, key=len)
  else:
  	tartekoKomunLuzeena=""

  if tartekoKomunLuzeena=="": #Ez badugu komunik topatu, badaezpada ere, errebisio malguago bat
      for buk,indline in bertsokoTartekoakZerrenda_pos:
        if (buk==kengarri[0]):
          unekoLerroGarbitua=bikoitiFonetizatuak[indline][:-len(kengarri[0])] #Aztertu uneko lerroa, kengarria kenduta.
          lerrokoTartekoak_tupla = [(tarteko,indline) for tarteko in tartekoakFonetizatuta if unekoLerroGarbitua.endswith(tarteko)]
          lerrokoTartekoak = [t[0] for t in lerrokoTartekoak_tupla]
          tartekoBakanak= list(set(lerrokoTartekoak))

          #Topatu dugun elementua kenezinaren berdina bada, bai!!
          #Hori da tarteko posible bat
          if (tartekoBakanak[0]==kenezin[0]):
            tartekoKomunLuzeena=tartekoBakanak[0]
            bikoitiFonetizatuak[indline]=bikoitiFonetizatuak[indline][:-len(kengarri[0])]






#  print (tartekoKomunLuzeena)
  tartekoarenLuzera=len(tartekoKomunLuzeena)

  #KENDU BUKAERAK LERRO BIKOITI FONETIZATUEI
  for indline, line in enumerate(bikoitiFonetizatuak):
    bikoitiFonetizatuak[indline]=bikoitiFonetizatuak[indline][:len(bikoitiFonetizatuak[indline])-tartekoarenLuzera]
#    print (bikoitiFonetizatuak[indline])


  #BILATU AURREKOAK
  bertsokoAurrekoak=set(aurrekoakFonetizatuta)
  bertsokoAurrekoakZerrenda_pos=[]
  for indline, line in enumerate(bikoitiFonetizatuak):
    lerrokoAurrekoak_tupla = [(aurreko, indline) for aurreko in aurrekoakFonetizatuta if line.endswith(aurreko)]
    lerrokoAurrekoak = [t[0] for t in lerrokoAurrekoak_tupla]
    bertsokoAurrekoak = bertsokoAurrekoak.intersection(set(lerrokoAurrekoak))


    #Honek lerro bakoitzean dauden tarteko posibleak itzuliko dizkigu.
    #Hauek zerrenda batean sartu behar ditugu gero horiekin jolastu ahal izateko.
    #Oraintxe arazo bat topatu dut, adibidez:
    #bertatik-faltik
    #"l" letra hori ez da aurrekoen zerrendan azaltzen, beraz, sistema ez da gai hori aurkitzeko
    #Soluzio merke bat, karaktere bat kendu, ea zer gertatzen den ikusteko
    #Kasu horretan funtzionatzen du
    if (len(lerrokoAurrekoak)==0):
      bertsokoAurrekoakZerrenda_pos.extend([(line[-1],indline)])
    else:
      bertsokoAurrekoakZerrenda_pos.extend(lerrokoAurrekoak_tupla)
    aurrekoBakanak = set(lerrokoAurrekoak)



    bertsokoAurrekoak = bertsokoAurrekoak.intersection(set(lerrokoAurrekoak))



#Orain tartekoaren eta aurrekoaren artean dauden elementu bereziak bilatuko ditugu,
#gerta-apeta bezalako kasuetan, baina azkenaurreko eta haren aurrekoaren artean.
#

  aurrpos = set([buk[0] for buk in bertsokoAurrekoakZerrenda_pos])
  bertsokoAurrekoakZerrenda = [buk[0] for buk in bertsokoAurrekoakZerrenda_pos]
  aurreko_maizt = [(aurr, bertsokoAurrekoakZerrenda.count(aurr)) for aurr in aurrpos]
  kengarri = min(aurreko_maizt,  key= lambda t: t[1]) #Preszindiblea den letra eta bere lerro zenbakia bilatu
  kenezin = max(aurreko_maizt,  key= lambda t: t[1]) 


  if len(bertsokoAurrekoak)!=0:
    aurrekoKomunLuzeena = max(bertsokoAurrekoak, key=len)
  else:
    aurrekoKomunLuzeena=""
#  print (aurrekoKomunLuzeena)
  aurrekoarenLuzera=len(aurrekoKomunLuzeena)

#  print (bertsokoAurrekoakZerrenda_pos)
  if aurrekoKomunLuzeena=="": #Ez badugu komunik topatu, badaezpada ere, errebisio malguago bat
      for buk,indline in bertsokoAurrekoakZerrenda_pos:
 #       print (buk, kengarri, indline)
        if (buk==kengarri[0]):
          unekoLerroGarbitua=bikoitiFonetizatuak[indline][:-len(kengarri[0])] #Aztertu uneko lerroa, kengarria kenduta.
          lerrokoAurrekoak_tupla = [(aurreko,indline) for aurreko in aurrekoakFonetizatuta if unekoLerroGarbitua.endswith(aurreko)]
          lerrokoAurrekoak = [t[0] for t in lerrokoAurrekoak_tupla]
          aurrekoBakanak= list(set(lerrokoAurrekoak))

          #Topatu dugun elementua kenezinaren berdina bada, bai!!
          #Hori da tarteko posible bat
          if (aurrekoBakanak[0]==kenezin[0]):
            aurrekoKomunLuzeena=aurrekoBakanak[0]
            bikoitiFonetizatuak[indline]=bikoitiFonetizatuak[indline][:-len(kengarri[0])]










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

