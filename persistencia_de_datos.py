import psycopg2
from psycopg2.extras import RealDictCursor
#Funcion Para ingresar los datos basicos del firmante a la base de datos en caso de que sea exixtoso la validadcion biometrica
def insertar_registro(data_base_url,nombre,tipo_documento,documento,correo):
 with psycopg2.connect(data_base_url) as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(" insert into registro_validacion_biometrica (nombre, tipo_documento, documento,correo_electronico) values(%s,%s,%s,%s)  ;" ,(nombre,tipo_documento,documento,correo))
            print("Consulta ejecutada correctamente")
            
            
