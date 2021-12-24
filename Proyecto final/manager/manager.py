from logging import exception
import os, time, pika, sys
from typing import Tuple
from tictactoe import TicTacToe

t = TicTacToe()
t.create_board()
player = 'X' if t.get_random_first_player() == 1 else 'O'

########### CONNEXIÓN A RABBIT MQ #######################
HOST = os.environ['RABBITMQ_HOST']      
connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST,heartbeat=0))
channel = connection.channel()
#El consumidor utiliza el exchange 'cartero'
channel.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)
#Se crea un cola temporaria exclusiva para este consumidor (búzon de correos)
result = channel.queue_declare(queue="ttt", exclusive=True, durable=True)
queue_name = result.method.queue
#La cola se asigna a un 'exchange'
channel.queue_bind(exchange='cartero', queue=queue_name, routing_key="ttt")

#####################################################################
########## ESPERA Y HACE ALGO CUANDO RECIBE UN MENSAJE ##############
#####################################################################

print(' [*] Waiting for messages. To exit press CTRL+C ')

#consumer
def callback(ch, method, properties, body):
        print(body.decode("UTF-8"))
        arguments = body.decode("UTF-8").split(" ")
        global player
        if (arguments[0] == "!play" and arguments[1] == "again"):
                print(f"NUEVO TABLERO") ## es un error forzado para que manager se reinicie
        if (arguments[0] == "!play"):
                i = int(arguments[1])
                j = int(arguments[2])
                print(f"Juega '{player}'; Columna: {i}, Fila: {j}.")
                t.fix_spot(i-1, j-1, player)
        
                ########################## MOSTRAR TABLERO EN DISCORD ############################################
                lista = t.board[0] + t.board[1] + t.board[2]
                line1 = f"----------------Turn of '{player}' player-----------------------\n"
                line2 = f"----------------Next turn '{t.swap_player_turn(player)}' player-----------------------\n"
                line = f"--------\n"
                row1 = f"{str(lista[0])} | {str(lista[1])} | {str(lista[2])}\n"
                row2 = f"{str(lista[3])} | {str(lista[4])} | {str(lista[5])}\n"
                row3 = f"{str(lista[6])} | {str(lista[7])} | {str(lista[8])}\n"
                tablero1 = line1 + row1 + line + row2 + line + row3 + line2
                channel.basic_publish(exchange='cartero', routing_key="discord_writer", body = tablero1)
                ##################################################################################################
                
                if t.is_player_win(player):
                        a = f"-----------------------Player '{player}' wins the game!-----------------------\n"
                        channel.basic_publish(exchange='cartero', routing_key="discord_writer", body = a) #publica el ganador
                        return t.board.clear() #reset tablero?
                
                if t.is_board_filled():
                        a = f"-----------------------Match Draw!-----------------------\n"
                        channel.basic_publish(exchange='cartero', routing_key="discord_writer", body = a)
                        return t.board.clear()
                
                player = t.swap_player_turn(player)
        
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()