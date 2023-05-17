#!/usr/bin/env python

import pika
import requests
import os
import sys
import time
from bs4 import BeautifulSoup


def connect_to_rabbitmq():
    credentials = pika.PlainCredentials('jousney', 'alan123')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='172.20.0.4', credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare('Temperatura Local')
    channel.queue_declare('Condicao Local')
    return channel, connection


def get_temperature(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    temperatura = soup.find("span", class_="dato-temperatura changeUnitT")
    if temperatura is not None:
        temperatura = temperatura.get('data')
        return temperatura.replace("|0|", "")
    else:
        print(f"Bloco Vazio! (temperatura)")
        return None

def get_condicao(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    span = soup.find("span", class_="descripcion")
    if span is not None:
        strong = span.find("strong")
        if strong is not None:
            condicao = strong.text
            return condicao.replace("Períodos", "Periodos")
    print(f"Bloco vazio! (condição)")
    return None

    
def main():
    channel, connection = connect_to_rabbitmq()
    url = 'https://www.tempo.com/campestre-do-maranhao.htm'
    print("[x] Inciando Busca por temperatura em Campestre-MA\nTente CTRL+C para sair")
    try:
        while True:
            temperatura = get_temperature(url)
            condicao = get_condicao(url)
            if temperatura is not None:
                channel.basic_publish(exchange="", routing_key="Temperatura Local", body=temperatura)
            else:
                print("Temperatura não encontrada!")
            if condicao is not None:
                channel.basic_publish(exchange="", routing_key="Condicao Local", body=condicao)
            else:
                print("Condição não encontrada!")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Interrompido!")
        connection.close()
        sys.exit(0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrompido!")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
