
import sys
import re
import sailkatzaileKlase

f=open(sys.argv[1])
txt=f.read().decode("utf8")
txt = re.sub(r'\n\s*\n\s*\n', '\n\n', txt).rstrip()
lines = txt.split("\n")
f.close()

of = sys.argv[2] #Irteera fitxategia

#print lines

#print [line.rstrip()=="" for line in lines]

bertsoak = []
bertsoa  = []
for line in lines:
  if line.rstrip()=="":
    bertsoak.append(bertsoa)
    bertsoa=[]
  else:
    bertsoa.append(line.rstrip())
bertsoak.append(bertsoa)
print str(len(bertsoak)) + " bertso ditugu!"
print "eta bertso bakoitzean ",[len(bertso) for bertso in bertsoak], " lerro"

ofw = open(of, 'w')
for bertso in bertsoak:
  try:
#    emaitza = sailkatzaileKlase.ikusiErrima("\n".join(bertso))
    emaitza = sailkatzaileKlase.ikusiErrimaBerria("\n".join(bertso))
  except ValueError:
    emaitza = "ERROREA"
  for lerro in bertso:
    print lerro.encode("utf8")
  print "Analisia: "+"-".join(emaitza)
  print
  ofw.write("-".join(emaitza)+"\n")
  
ofw.close()
