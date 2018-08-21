# -*- coding: utf-8 -*-
import sqlite3 # biblioteca necessária para trabalhar com sqlite3
import gzip # bilioteca para trabalhar com arquivos compactados
import os
import sys

"""
Script de importação de dados

Como funciona:
1 - Servidor de dados do órgão público é acessado e os arquivos são baixados
2 - Os arquivos baixados são transformados em bases de dados sqlite3 http://sqlite.org

@author Diego Nobre <dcnobre@gmail.com>
@since 20/08/2018

# Órgãos implementados
## Órgão: TCE-PB (Tribunal de Contas do Estado da Paraiba)
##-> Origem: http://portal.tce.pb.gov.br/dados-abertos-do-sagres-tcepb/
"""

import os
from subprocess import call

os.system('cls' if os.name == 'nt' else 'clear')

"""
Classe utilizada para colorir saída do terminal
@see http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
"""
class bcolor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

'''
Devolve cópia de uma str substituindo os caracteres
acentuados pelos seus equivalentes não acentuados.

ATENÇÃO: carateres gráficos não ASCII e não alfa-numéricos,
tais como bullets, travessões, aspas assimétricas, etc.
são simplesmente removidos!

    >>> remover_acentos('[ACENTUAÇÃO] ç: áàãâä! éèêë? íì&#297;îï, óòõôö; úù&#361;ûü.')
    '[ACENTUACAO] c: aaaaa! eeee? iiiii, ooooo; uuuuu.'

'''
def remover_acentos(txt, codif='utf-8'):
    return normalize('NFKD', txt.decode(codif)).encode('ASCII','ignore')

def conectar(path_banco):
    # abrindo conexão com o banco de Dados
    conexao = sqlite3.connect(path_banco)
    # configuração necessária para trabalhar com unicode
    conexao.text_factory = str

    return conexao

def transformar(conexao, esfera, arquivo, tabela):
    print bcolor.OKBLUE + "###-> TRANSFORMANDO ARQUIVO" + bcolor.ENDC, arquivo
    print "# O arquivo irá gerar a tabela", tabela

    print "# criando cursor para manipulação do banco de dados"
    cursor = conexao.cursor()

    print "# criando estrutura da tabela", tabela
    cursor.executescript(open('./ddl/'+tabela+'.sql').read())

    # lendo quantidade de colunas da tabela
    # @see https://pagehalffull.wordpress.com/2012/11/14/python-script-to-count-tables-columns-and-rows-in-sqlite-database/
    tableInfo = "PRAGMA table_info(%s)" % tabela
    cursor.execute(tableInfo)
    qt_colunas_tabela = len(cursor.fetchall()) - 1

    # texto do INSERT na tabela
    # exemplo: INSERT INTO estorno VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    tx_insert = 'INSERT INTO '+tabela+' VALUES (NULL, '
    for i in range(qt_colunas_tabela):
        if i != max(range(qt_colunas_tabela)):
            tx_insert = tx_insert + '?, '
        else:
            tx_insert = tx_insert + '?)'

    print bcolor.UNDERLINE + "# iniciando leitura do arquivo..." + bcolor.ENDC
    cont_linhas = 1
    for linha in gzip.open('./'+arquivo, 'rb'):
        if cont_linhas > 1: # pulando o cabeçalho do arquivo
            # transformando linhas em lista de valores para inserir no banco
            colunas = linha.strip().split("|")

            # inserindo dados no banco
            cursor.executemany(tx_insert, (colunas, ))
        # incrementando contador de linhas
        cont_linhas = cont_linhas + 1

    # salvando alterações
    conexao.commit()

    linhas_lidas = cont_linhas - 2 # remove cabeçalho e ultimo add do loop
    #print "Total de linhas lidas:", linhas_lidas
    cursor.execute('SELECT count(1) FROM '+tabela)
    qt_linhas = cursor.fetchone()
    #print "Total de linhas inseridas:", qt_linhas[0]

    if qt_linhas[0] != linhas_lidas:
        print bcolor.WARNING + "#-> O total de linhas lidas ("+linhas_lidas+") não bate com as inseridas ("+qt_linhas[0]+")" + bcolor.ENDC + '\n'
    else:
        print bcolor.OKGREEN + "#-> Arquivo transformando com sucesso!" + bcolor.ENDC + '\n'

# parâmetro passado via linha de comando
esfera = sys.argv[1]
if esfera not in ['municipal', 'estadual']:
    print "Esfera invalida! Informe esfera estadual ou municipal em letras minusculas"
    exit()

# conectando ao banco de dados
try:
    conexao = conectar('./esfera-'+esfera+'.db')
except Exception as e:
    print "Erro ao conectar:", e
    exit()

list_esfera_municipal = [
    ['TCE-PB-SAGRES-Folha_Pessoal_Esfera_Municipal.txt.gz', 'folha_pessoal_municipal']
]

list_esfera_estadual = [
    ['TCE-PB-SAGRES-Folha_Pessoal_Esfera_Estadual.txt.gz', 'folha_pessoal_estadual']
]

# iniciando transformação dos arquivos
try:
    if esfera == 'municipal':
        print bcolor.UNDERLINE + "###########################################################" + bcolor.ENDC
        print bcolor.UNDERLINE + "###-> ESFERA MUNICIPAL - Iniciando download de arquivos ###" + bcolor.ENDC
        print bcolor.UNDERLINE + "###########################################################" + bcolor.ENDC
        path_esfera_municipal = './'

        if not os.path.exists(path_esfera_municipal):
            os.mkdirs(path_esfera_municipal)

        for arquivo in list_esfera_municipal:
            print bcolor.BOLD + "#-> " + arquivo[0] + bcolor.ENDC
            call(["wget", "http://dados.tce.pb.gov.br/"+arquivo[0], "-P", path_esfera_municipal])

        for arquivo in list_esfera_municipal:
            transformar(conexao, esfera, arquivo[0], arquivo[1])
    else:
        # ESFERA ESTADUAL
        print bcolor.UNDERLINE + "##########################################################" + bcolor.ENDC
        print bcolor.UNDERLINE + "###-> ESFERA ESTADUAL - Iniciando download de arquivos ###" + bcolor.ENDC
        print bcolor.UNDERLINE + "##########################################################" + bcolor.ENDC
        path_esfera_estadual = './'

        if not os.path.exists(path_esfera_estadual):
            os.mkdirs(path_esfera_estadual)

        for arquivo in list_esfera_estadual:
            print bcolor.BOLD + "#-> " + arquivo[0] + bcolor.ENDC
            call(["wget", "http://dados.tce.pb.gov.br/"+arquivo[0], "-P", path_esfera_estadual])

        for arquivo in list_esfera_estadual:
            transformar(conexao, esfera, arquivo[0], arquivo[1])
        
        #cursor = conexao.cursor()
        #print "# criando indices da folha de pessoal estadual"
        #cursor.executescript(open('./ddl/folha_pessoal_estadual_index.sql').read())

        #print "# criando slug para nome do poder (Ex: poder-executivo)"
        #cursor_insert = conexao.cursor()
        #for poder in (cursor.execute('SELECT DISTINCT de_poder FROM folha_pessoal_estadual')):
        #    ds_link = poder[0].replace(',', ' ').replace('.', ' ').replace('-', ' ')
        #    ds_link = " ".join(ds_link.split()).replace(' ', '-')
        #    ds_link = remover_acentos(ds_link).lower()
        #    cursor_insert.execute('UPDATE folha_pessoal_estadual SET de_poder = ? WHERE de_poder = ?', (ds_link, poder[1], ))
        #cursor_insert.close()
except Exception as e:
    print "Erro ao transformar arquivo:", e
    exit()

# fechando conexão ao banco
conexao.close()
