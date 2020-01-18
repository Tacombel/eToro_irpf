import csv
from collections import defaultdict
import sqlite3

conn = sqlite3.connect('app.db')
c = conn.cursor()

# saco los datos de cambio

c.execute('SELECT * FROM cotizacion WHERE activo_id=?', ('10',))
query = c.fetchall()
cambios = {}
for e in query:
    cambios[e[1]] = e[2]
# Para crear el data.csv descargo de eToro el fichero del periodo que interesa, lo abro en Google Docs
# y descargo la pestaña Closed Positions como csv, incluyendo la fila de títulos
# Proceso los datos

datos = []

with open('data.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    primera = True
    for row in spamreader:
        if primera:
            primera = False
            continue

        linea = []
        for e in row:
            e = e.replace(',', '.', 1)
            linea.append(e)
        datos.append(linea)

    estructura = defaultdict(dict)

    total_profit_euros = 0
    total_fees_euros = 0

    for e in datos:
        inicial_dolar = float(e[3])
        final_dolar = float(e[3]) + float(e[8])
        inicial_fecha = e[9].split(" ")[0]
        inicial_fecha = inicial_fecha.split("/")
        inicial_fecha = inicial_fecha[2] + '-' + inicial_fecha[1] + '-' + inicial_fecha[0]
        final_fecha = e[9].split(" ")[0]
        final_fecha = final_fecha.split("/")
        final_fecha = final_fecha[2] + '-' + final_fecha[1] + '-' + final_fecha[0]
        inicial_euro = inicial_dolar * cambios[inicial_fecha]
        final_euro = final_dolar * cambios[final_fecha]
        total_profit_euros = total_profit_euros + final_euro - inicial_euro
        total_fees_euros = total_fees_euros + float(e[13]) * cambios[final_fecha]

        if e[2] == '':
            e[2] = 'Yo'
        if not e[2] in estructura:
            estructura[e[2]]['profit'] = round(float(e[8]), 2)
            estructura[e[2]]['fees'] = round(float(e[13]), 2)
            estructura[e[2]]['transacciones'] = 1
        else:
            estructura[e[2]]['profit'] = estructura[e[2]]['profit'] + round(float(e[8]), 2)
            estructura[e[2]]['fees'] = estructura[e[2]]['fees'] + round(float(e[13]), 2)
            estructura[e[2]]['transacciones'] += 1

    total_transacciones = 0
    total_profit = 0
    total_fees = 0

    print()
    print('Fecha cierre primera operación', datos[len(datos) - 1][10])
    print('Fecha cierre última operación', datos[1][10])
    print()

    # Lista de los trader copiados por orden alfabetico
    copiados = []
    for key in estructura:
        copiados.append(key)
    copiados = sorted(copiados, key=str.casefold)

    # Formateo los valores para imprimir
    print_total_profit = '{:.2f}'.format(total_profit) + '$'

    for e in copiados:
        print(e)
        print(' Transacciones =', estructura[e]['transacciones'])
        print(' Profit        =', '{:.2f}'.format(estructura[e]['profit']) + '$')
        print(' Fees          =', '{:.2f}'.format(estructura[e]['fees']) + '$')
        print(' Neto          =', '{:.2f}'.format((estructura[e]['profit'] - estructura[key]['fees'])) + '$')
        total_transacciones = total_transacciones + estructura[e]['transacciones']
        total_profit = total_profit + round(estructura[e]['profit'], 2)
        total_fees = total_fees + round(estructura[e]['fees'], 2)

    width = 5
    print('-----------------------------')
    print('Transacciones totales =', total_transacciones)
    print('Profit total          =', '{:>8}'.format('{:.2f}'.format(total_profit) + '$'), '{:>8}'.format('{:.2f}'.format(total_profit_euros) + '€'))
    print('Fees totales          =', '{:>8}'.format('{:.2f}'.format(total_fees) + '$'), '{:>8}'.format('{:.2f}'.format(total_fees_euros) + '€'))
    print('Neto total            =', '{:>8}'.format('{:.2f}'.format(total_profit - total_fees) + '$'), '{:>8}'.format('{:.2f}'.format(total_profit_euros - total_fees_euros) + '€'))
