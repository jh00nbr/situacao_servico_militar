#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests,sys,re,random
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
from unicodedata import normalize

"""
jdavi@insightsecurity.com.br
Insightl4b - http://lab.insightsecurity.com.br 
Blog: lab.insightsecurity.com.br
Github: http://github.com/jh00nbr
Packetstorm: https://packetstormsecurity.com/users/jh00nbr
Twitter @jh00nbr
"""

"""
Simples script para acompanhamento de situação no serviço militar através do CPF ou RA.
RA - Registro de Alistamento
"""
__author__ = "Jhonathan Davi A.K.A jh00nbr"
__email__ = "jdavi@insightsecurity.com.br"

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def carregar_useragents():
    uas = []
    with open("user-agents.txt", 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[0:-1-0])
    random.shuffle(uas)
    return uas        

def remover_acentos(string, codif='utf-8'):
    return normalize('NFKD', string.decode(codif)).encode('ASCII','ignore')        

def remover_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def remover_palavras_chatas(worlds):
    return str(worlds).replace('Data Nasc: ','').replace('RA: ','').replace('Nome: ','').replace('Situação: ','')

def formatar_dataNascimento(data_char):
    meses = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    data_n = str(data_char).split()
    return data_n[2]+'/'+meses[data_n[1]]+'/'+data_n[5]

ra,cpf = '',''

if len(sys.argv[1]) == 11:
    cpf = str(sys.argv[1])
elif len(sys.argv[1]) ==12:
    ra = str(sys.argv[1])
else:
    print "[!] Ops, você esqueceu do cpf(11 chars) ou o ra(12 chars), Ex: python situacao_militar.py 00000000000 ou 111111111111"
    sys.exit()


config = {'url':'http://www.alistamento.eb.mil.br/cidadao/situacao.action'}
payload = {'cidadao.ra':ra,'cidadao.cpf':cpf}
header = {'Referer':'http://www.alistamento.eb.mil.br/cidadao/situacao.action','User-Agent':random.choice(carregar_useragents())}
dados = ['RA','nome','dataNascimento','situacao']

req = requests.post(config['url'],data=payload,headers=header)

try:
    soup = BeautifulSoup(req.content,'html.parser')
    result = soup.find('div',{'class':'panel panel-primary'})
    conteudo = [remover_palavras_chatas(remover_tags(str(b))) for b in result.findAll('li')]
    dados = dict(zip(dados,conteudo))
    dados_retorno = {'dataNascimento': formatar_dataNascimento(dados['dataNascimento']), 'situacao': dados['situacao'],'RA': dados['RA'],'nome':dados['nome']}
    print dados_retorno
except Exception:
    print "[!] Registros não encontrados!"
