import wikipedia
import pika, sys

# un componente 'productor' envia mensajes de tipo: "wikipedia (Chile)"
# Conexión al servidor RabbitMQ

message = ' '.join(sys.argv[1:]) or "Wikipedia"

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

#Creación de la cola
channel.queue_declare(queue='hello')

#Publicación del mensaje
channel.basic_publish(exchange='', routing_key='hello', body = message)

print(" [x] Sent %r"  % message)

connection.close()