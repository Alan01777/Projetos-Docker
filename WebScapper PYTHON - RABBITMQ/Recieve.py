#!/usr/bin/env python

import pika
import sys
import os


def main():
    credentials = pika.PlainCredentials('jousney', 'alan123')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='172.20.0.4', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='Temperatura Local')
    channel.queue_declare('Condicao Local')

    def callback_Temperatura(ch, method, properties, body):
        print(f'[x] Temperatura: {body}ºC')

    def callback_Condicao(ch, method, properties, body):
        print(f'[x] Condicao: {body}\n\n')

    channel.basic_consume(queue='Temperatura Local',
                          on_message_callback=callback_Temperatura, auto_ack=True)
    
    channel.basic_consume(queue='Condicao Local',
                          on_message_callback=callback_Condicao, auto_ack=True)

    print(" [*] Aguardadando mensagem. Para sair tente CTRL+C... ")

    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Saindo...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
