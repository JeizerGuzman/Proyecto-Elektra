import mysql.connector

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="davidlaid",
            database="dbelektra",
            port="3306"
        )
        print("Conexión exitosa a MySQL")
        return conexion
    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None