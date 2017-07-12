#!/usr/bin/env python

import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "<mezua><bertsoa>Batetikan korrozka|bestetik herrena|ohea okupatu du|hori da txarrena|ez da pinta kabala|honek dakarrena|kaltzontzilorik gabe|ohean barrena|pixkat gutxigo edan|ezazu hurrena</bertsoa><aur>a ai b d g r alb ald alg e eb ed eg er i is iz o oi op ot ok osp ost osk ozp ozt ozk t k R s z x ts tz tx st sk zt zk u</aur><tart>ai e i l n m o oi r u s z ts tz tx R</tart><buk>a ak an ean ian ez ik k ko koak n ra rat rik ta tik tzen z</buk></mezua>\n"

import socket




TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
#MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print "received data:", data

