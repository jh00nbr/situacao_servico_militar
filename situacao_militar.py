#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import argparse

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

URL = 'http://www.alistamento.eb.mil.br/cidadao/situacao.action'


def check_value(value):
    length = len(value)
    if length < 11 or length > 12:
        return False
    return value.isdigit()


def make_request(value, cpf=True):

    payload = {
        'cidadao.ra': '' if cpf else value,
        'cidadao.cpf': value if cpf else ''
    }

    return requests.post(URL,
                         data=payload,
                         headers={'Accept-Language': 'pt-BR'})


def handle_response(request):

    soup = BeautifulSoup(request.content, 'html.parser')
    panel = soup.find('div', {'class': 'panel panel-primary'})
    list_items = panel.findAll('li')
    return [item.text for item in list_items]


def show_results(results):

    for result in results:
        print(result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-cpf', help='CPF para realizar a consulta')
    parser.add_argument('-ra', help='RA para realizar a consulta')
    args = parser.parse_args()

    if args.cpf or args.ra:
        value = args.cpf or args.ra
        if check_value(value):
            try:
                request = make_request(value, bool(args.cpf))
                results = handle_response(request)
                show_results(results[:-1])
            except (Exception) as e:
                print('Não possível obter resultados.')
        else:
            print('CPF ou RA inválido.')
    else:
        parser.print_help()
