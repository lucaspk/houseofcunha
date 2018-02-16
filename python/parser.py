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

header =  'tipo,num_pro,ano,id_votacao,resumo,data,hora,objetivo,sessao,nome,id_dep,partido,uf,voto,orientacao_partido,orientacao_gov,cunha'
fileToWrite.write(header + '\n')

total_num_votacoes = 0
for file in files:

    try:
        xmldoc = minidom.parse(file)
    except:
        txt = open(file)
        if ("xml") not in txt.readline():
            print "ERROR: NOT AN XML >>> " + file
            continue
        else:
            print "ERROR: >>>" + file
            continue

    sigla = xmldoc.getElementsByTagName('Sigla')[0].firstChild.nodeValue
    n_prop = xmldoc.getElementsByTagName('Numero')[0].firstChild.nodeValue
    ano = xmldoc.getElementsByTagName('Ano')[0].firstChild.nodeValue

    votacoes = xmldoc.getElementsByTagName('Votacao')

    i = 0
    for votacao in votacoes:
        i += 1
        resumo = votacao.attributes['Resumo'].value.strip().replace(',','.').replace("\r\n",'')
        data_prop = votacao.attributes['Data'].value.strip()
        hora_prop = votacao.attributes['Hora'].value.strip()
        objetivo = votacao.attributes['ObjVotacao'].value.strip().replace(',','.')
        sessao = votacao.attributes['codSessao'].value.strip()

        votacao_infos = [sigla, n_prop, ano, str(i), resumo, data_prop, hora_prop, objetivo, sessao]

        bancada = votacao.getElementsByTagName('bancada')
        map_bancada = {}

        for b in bancada:

            content = b.attributes.get('orientacao','NA')

            if content != 'NA':
                content = content.value.strip().lower()

            map_bancada[b.attributes['Sigla'].value.lower()] = content

        reg_votos = votacao.getElementsByTagName('votos')[0]

        for dep in reg_votos.getElementsByTagName('Deputado'):
            to_print_dep = []
            nome = dep.attributes['Nome'].value.strip()
            id_dep = dep.attributes['ideCadastro'].value.strip()
            partido = dep.attributes['Partido'].value.strip().lower()
            uf = dep.attributes['UF'].value.strip()
            voto = dep.attributes['Voto'].value.strip().lower()

            orientacao = map_bancada.get(partido, 'NA')
            if orientacao == 'NA':
                for key in map_bancada.keys():
                    if len(key) > 8:
                        if partido in key:
                            orientacao = map_bancada.get(key)

            deputado_infos = [nome, id_dep, partido, uf, voto, orientacao, map_bancada.get('gov.','NA')]

            for key in map_bancada:
                if 'pmdb' in key:
                    deputado_infos.append(map_bancada.get(key,'NA'))
                    break

            if len(votacao_infos + deputado_infos) == 17:
                to_print_final =  ','.join(votacao_infos + deputado_infos)
                fileToWrite.write(to_print_final + "\n")

    total_num_votacoes += i

print "total_num_votacoes: ", total_num_votacoes
        


fileToWrite.close()
