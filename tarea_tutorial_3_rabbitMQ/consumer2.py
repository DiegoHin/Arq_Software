import pika, sys, os
import pageviewapi.period

#   un componente 'consumidor' realiza búsqueda en wikipedia e imprime el resumen de la pagina.
#   pageviewapi.period.sum_last('fr.wikipedia', 'Paris', last=30, access='all-access', agent='all-agents')
def main():
    #Conexión al servidor RabbitMQ   
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    #Nos aseguramos que existe una cola 'hello'
    channel.queue_declare(queue='hello')

    # Recibir mensajes de la cola es más complejo. Funciona suscribiendo una función de devolución de llamada ("callback"). 
    # Cada vez que recibimos un mensaje, esta función "callback" es llamada por la libreria Pika. En nuestro caso, 
    # esta función imprimirá en la pantalla el contenido del mensaje.
    def callback(ch, method, properties, body):
        count = pageviewapi.period.sum_last('es.wikipedia', body.decode(), last=30)
        print(" [x] Received %s" % count)

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

    #Bocle infinita
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)