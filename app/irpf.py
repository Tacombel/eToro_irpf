import csv
from collections import defaultdict
import requests


def rate_dolar(fecha):
    address = 'https://api.exchangeratesapi.io/' + fecha + '?symbols=USD'
    r = requests.get(address).json()
    rate = r['rates']['USD']
    print('Tipo de cambio para el', fecha, '=', rate)
    return rate


def adaptar_fecha(fecha):
    fecha_modificada = fecha.split(" ")[0]
    fecha_modificada = fecha_modificada.split("/")
    fecha_modificada = fecha_modificada[2] + '-' + fecha_modificada[1] + '-' + fecha_modificada[0]
    return fecha_modificada


# Para crear el data.csv descargo de eToro el fichero del periodo que interesa, lo abro en Google Docs
# y descargo la pestaña Closed Positions como csv, incluyendo la fila de títulos
# Proceso los datos

datos = []
cambio_euro_dolar = {}

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
        inicial_fecha = adaptar_fecha(e[9])
        final_fecha = adaptar_fecha(e[10])
        if inicial_fecha not in cambio_euro_dolar:
            cambio_euro_dolar[inicial_fecha] = rate_dolar(inicial_fecha)
        inicial_cambio = cambio_euro_dolar[inicial_fecha]
        if final_fecha not in cambio_euro_dolar:
            cambio_euro_dolar[final_fecha] = rate_dolar(final_fecha)
        final_cambio = cambio_euro_dolar[final_fecha]
        inicial_euro = inicial_dolar * inicial_cambio
        final_euro = final_dolar * final_cambio
        total_profit_euros = total_profit_euros + final_euro - inicial_euro
        total_fees_euros = total_fees_euros + float(e[13]) * final_cambio

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
        print('Trader:', e)
        print(' Transacciones =', estructura[e]['transacciones'])
        print(' Profit =', '{:>8}'.format('{:.2f}'.format(estructura[e]['profit']) + '$'))
        print(' Fees   =', '{:>8}'.format('{:.2f}'.format(estructura[e]['fees']) + '$'))
        print(' Neto   =', '{:>8}'.format('{:.2f}'.format((estructura[e]['profit'] - estructura[e]['fees'])) + '$'))
        total_transacciones = total_transacciones + estructura[e]['transacciones']
        total_profit = total_profit + round(estructura[e]['profit'], 2)
        total_fees = total_fees + round(estructura[e]['fees'], 2)

    print('-----------------------------')
    print('Transacciones totales =', total_transacciones)
    print('Profit total =', '{:>8}'.format('{:.2f}'.format(total_profit) + '$'), '{:>8}'.format('{:.2f}'.format(total_profit_euros) + '€'))
    print('Fees totales =', '{:>8}'.format('{:.2f}'.format(total_fees) + '$'), '{:>8}'.format('{:.2f}'.format(total_fees_euros) + '€'))
    print('Neto total   =', '{:>8}'.format('{:.2f}'.format(total_profit - total_fees) + '$'), '{:>8}'.format('{:.2f}'.format(total_profit_euros - total_fees_euros) + '€'))
