# coding: utf-8
import sys
from xml.dom import minidom
import glob

###################################
#
#To run:
#python parser.py folder/*.xml file_to_write.csv
#
###################################

reload(sys)
sys.setdefaultencoding('utf8')

files = glob.glob(sys.argv[1])
fileToWrite = open(sys.argv[2],'w')

header =  'ideCadastro\tcondicao\tmatricula\tidParlamentar\tnome\tnomeParlamentar\turlFoto\tsexo\tuf\tpartido\tgabinete\tfone\temail\tnone'
fileToWrite.write(header + '\n')

for file in files:

    try:
        xmldoc = minidom.parse(file)
    except:
        txt = open(file)
        if ("xml") not in txt.readline():
            print "ERROR: NOT A XML >>> " + file
            continue
        else:
            print "ERROR: >>>" + file
            continue

    deputados = xmldoc.getElementsByTagName('deputado')

    for deputado in deputados:
       ideCadastro = deputado.getElementsByTagName('ideCadastro')[0].firstChild.nodeValue
       condicao = deputado.getElementsByTagName('condicao')[0].firstChild.nodeValue
       matricula = deputado.getElementsByTagName('matricula')[0].firstChild.nodeValue
       idParlamentar = deputado.getElementsByTagName('idParlamentar')[0].firstChild.nodeValue
       nome = deputado.getElementsByTagName('nome')[0].firstChild.nodeValue
       nomeParlamentar = deputado.getElementsByTagName('nomeParlamentar')[0].firstChild.nodeValue
       urlFoto = deputado.getElementsByTagName('urlFoto')[0].firstChild.nodeValue
       sexo = deputado.getElementsByTagName('sexo')[0].firstChild.nodeValue
       uf = deputado.getElementsByTagName('uf')[0].firstChild.nodeValue
       partido = deputado.getElementsByTagName('partido')[0].firstChild.nodeValue
       gabinete = deputado.getElementsByTagName('gabinete')[0].firstChild.nodeValue
       fone = deputado.getElementsByTagName('fone')[0].firstChild.nodeValue
       email = deputado.getElementsByTagName('email')[0].firstChild.nodeValue

       deputado_infos = [ideCadastro, condicao, matricula, idParlamentar, nome, nomeParlamentar, urlFoto, sexo, uf,
                         partido, gabinete, fone, email]

       for _print in deputado_infos:
            fileToWrite.write(_print + "\t")
       
       fileToWrite.write("\n")


fileToWrite.close()
