import csv
from collections import defaultdict

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

    for e in datos:
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

    for key in estructura:
        if key == '':
            print('Yo')
        else:
            print(key)
        print(' Transacciones =', estructura[key]['transacciones'])
        print(' Profit        =', '{:.2f}'.format(estructura[key]['profit']) + '$')
        print(' Fees          =', '{:.2f}'.format(estructura[key]['fees']) + '$')
        print(' Neto          =', '{:.2f}'.format((estructura[key]['profit'] - estructura[key]['fees'])) + '$')
        total_transacciones = total_transacciones + estructura[key]['transacciones']
        total_profit = total_profit + round(estructura[key]['profit'], 2)
        total_fees = total_fees + round(estructura[key]['fees'], 2)
    print('-----------------------------')
    print('Transacciones totales =', total_transacciones)
    print('Profit total          =', '{:.2f}'.format(total_profit) + '$')
    print('Fees totales          =', '{:.2f}'.format(total_fees) + '$')
    print('Neto total            =', '{:.2f}'.format(total_profit - total_fees) + '$')
