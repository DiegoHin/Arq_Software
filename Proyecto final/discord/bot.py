import os, discord, pika
from os import environ
from discord import message
from discord.ext import commands
from dotenv import load_dotenv

########################## CONEXION RABBITMQ ########################################
HOST = os.environ['RABBITMQ_HOST']
connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST,heartbeat=0))
channelMQ = connection.channel()
#Creamos el exchange 'cartero' de tipo 'fanout'
channelMQ.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)
#####################################################################################

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.command(name='play', help='Inicia una partida!\n\nEjemplo: !play <FILA> <COLUMNA>; FILA y COLUMNA valores {1,2,3}')
async def tictac(ctx):
    message =  ctx.message.content
    channelMQ.basic_publish(exchange='cartero', routing_key="ttt", body=message)

@bot.command(name='play again', help='Nuevo juego')
async def tictac(ctx):
    message =  ctx.message.content
    channelMQ.basic_publish(exchange='cartero', routing_key="ttt", body=message)        
    
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

import threading

#producer
def writer(bot):
    print('Worker')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST,heartbeat=0))
    channelMQ = connection.channel()
    #Creamos el exchange 'cartero' de tipo 'fanout'
    channelMQ.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)
    #Se crea un cola temporaria exclusiva para este consumidor (búzon de correos)
    result = channelMQ.queue_declare(queue="discord_writer", exclusive=True, durable=True)
    queue_name = result.method.queue
    #La cola se asigna a un 'exchange'
    channelMQ.queue_bind(exchange='cartero', queue=queue_name, routing_key="discord_writer")
    print(' [*] Waiting for messages. To exit press CTRL+C')
    
    async def write(message):
        channel = bot.get_channel(924004215179853874)
        await channel.send(message)
        
    def callback(ch, method, properties, body):
        message=body.decode("UTF-8")
        print(message)
        bot.loop.create_task(write(message)) #publica en discord el player
    
    channelMQ.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channelMQ.start_consuming()
t = threading.Thread(target=writer, args=[bot])
t.start()
bot.run(TOKEN)