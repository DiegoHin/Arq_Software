import pymysql

conectar = pymysql.connect(host = 'localhost',user = 'root',password = '')
cur = conectar.cursor()

tabla_NEWS = '''CREATE TABLE news(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, 
                                title TEXT, 
                                date DATE, 
                                url TEXT, 
                                media_outlet VARCHAR(255),
                                category VARCHAR(255));'''

datos_NEWS = '''INSERT INTO news(title, date, url, media_outlet, category) VALUES
    ('El noble y aplaudido gesto de Cereceda tras error del joven portero de Colo Colo y el elogio de Claudio Bravo al jugador de Audax',
    '2021-10-29',
    'https://www.emol.com/noticias/Deportes/2021/10/29/1036824/noble-gesto-cereceda-colo-colo.html',
    'emol','Deporte'),
    
    ('Senadores dejan fuera de la tabla de la próxima semana cuarto retiro e indulto: Acuerdo volverá a ser revisado el martes',
    '2021-10-29',
    'https://www.emol.com/noticias/Nacional/2021/10/29/1036864/senado-acuerdo-tabla-indulto-10.html',
    'emol','Politica'),
    
    ('Escuelas de Nueva York prohibieron disfraces de "El juego del calamar" para Halloween',
    '2021-10-28',
    'https://www.emol.com/noticias/Tendencias/2021/10/28/1036787/nueva-york-escuelas-disfraces-halloween.html',
    'emol','Tendencias');'''

def crear_db(cur):
    cur.execute('''CREATE DATABASE sun;''')
    cur.execute('''USE sun;''')
    cur.execute(tabla_NEWS)

def insertar_db(cur):
    cur.execute('''USE sun;''')
    cur.execute(datos_NEWS)
    cur.execute('''COMMIT;''')
    cur.close()
    
crear = crear_db(cur)
insertar = insertar_db(cur)