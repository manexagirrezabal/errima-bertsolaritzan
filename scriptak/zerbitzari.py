#!/usr/bin/env python

import socket
import sailkatzaileKlase
from lxml import etree

stri="<mezua><bertsoa>Batetikan korrozka|bestetik herrena|ohea okupatu du|hori da txarrena|ez da pinta kabala|honek dakarrena|kaltzontzilorik gabe|ohean barrena|pixkat gutxigo edan|ezazu hurrena</bertsoa><aur>a ai b d g r alb ald alg e eb ed eg er i is iz o oi op ot ok osp ost osk ozp ozt ozk t k R s z x ts tz tx st sk zt zk u</aur><tart>ai e i l n m o oi r u s z ts tz tx R</tart><buk>a ak an ean ian ez ik k ko koak n ra rat rik ta tik tzen z</buk></mezua>"
tree = etree.fromstring(stri)
#print tree
bertsoa=tree.find("bertsoa").text.replace("|","\n")
aur=tree.find("aur").text
tart=tree.find("tart").text
buk=tree.find("buk").text
#print bertsoa
#print aur
#print tart
#print buk
#raw_input()




TCP_IP = '158.227.112.22'
TCP_PORT = 5005
BUFFER_SIZE = 4096  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))


s.listen(1)
print "The server is on, and waiting requests"
print "IP address:", TCP_IP
print "Port:", TCP_PORT

#https://ruslanspivak.com/lsbaws-part1/   FINALLY!!!
while 1:
  conn, addr = s.accept()
  print 'Connection address:', addr
  data = conn.recv(BUFFER_SIZE)

  print data
  tree = etree.fromstring(data)
  bertsoa=tree.find("bertsoa").text.replace("|","\n")
  aur=tree.find("aur").text
  tart=tree.find("tart").text
  buk=tree.find("buk").text
  try:
    result='-'.join(sailkatzaileKlase.ikusiErrimaWeb(bertsoa, aur, tart, buk))
  except ValueError:
    result="kaka"
  print result

  conn.sendall(result)  # echo
  conn.close()
  print "Closed!"



