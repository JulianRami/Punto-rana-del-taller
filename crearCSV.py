import csv
import random

def crear_csv_numeros_aleatorios(nombre_archivo, cantidad_datos):
    with open(nombre_archivo, 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)

        for _ in range(cantidad_datos):
            numero_aleatorio = round(random.uniform(0, 1), 5)
            escritor_csv.writerow([numero_aleatorio])

# Reemplaza 'numeros_aleatorios.csv' con el nombre que desees para el archivo CSV
archivo_csv = 'numeros_aleatorios3.csv'
cantidad_datos = 10000000  # Puedes ajustar la cantidad de datos que deseas generar
crear_csv_numeros_aleatorios(archivo_csv, cantidad_datos)

print(f'Se ha creado el archivo "{archivo_csv}" con {cantidad_datos} números aleatorios.')

def contar_valores(nombre_archivo):
    menores_05 = 0
    mayores_05 = 0

    with open(nombre_archivo, 'r') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        for fila in lector_csv:
            numero = float(fila[0])
            if numero < 0.5:
                menores_05 += 1
            else:
                mayores_05 += 1

    return menores_05, mayores_05

archivo_csv = 'numeros_aleatorios3.csv'
menores, mayores = contar_valores(archivo_csv)

print(f'Cantidad de valores menores a 0.5: {menores}')
print(f'Cantidad de valores mayores o iguales a 0.5: {mayores}')