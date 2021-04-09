# python 3.6

import os
from collections import defaultdict
import requests
import json
import os.path
from openpyxl import load_workbook


def menu():
    path = './'
    counter = 1
    opciones = []
    # r=root, d=directories, f = files
    for f in os.walk(path):
        for file in f[2]:
            if 'eToro' in file:
                opciones.append(file)
                print(counter, ': ', file)
                counter += 1
        opcion_menu = input("Elije un fichero >> ")
        print('Procesaremos el fichero:', opciones[int(opcion_menu) - 1])
        return opciones[int(opcion_menu) - 1]

def rate_dolar(fecha):
    address = 'http://api.currencylayer.com/historical?access_key=' + config['API_CURRENCYLAYER'] + '&date=' + fecha + '&currencies=EUR&format=1'
    r = requests.get(address).json()
    rate = r['quotes']['USDEUR']
    print('Tipo de cambio para el', fecha, '=', rate)
    return rate


def adaptar_fecha(fecha):
    fecha_modificada = fecha.split(" ")[0]
    fecha_modificada = fecha_modificada.split("/")
    fecha_modificada = fecha_modificada[2] + '-' + fecha_modificada[1] + '-' + fecha_modificada[0]
    return fecha_modificada


if __name__ == '__main__':
    # configuracion
    if os.path.isfile('config.json'):
        with open('config.json', 'r') as f:
            config = json.load(f)
    else:
        config = {}
        API_KEY = input('Falta la API_KEY. Introducela y pulsa ENTER >> ')
        config['API_CURRENCYLAYER'] = API_KEY
        with open('config.json', 'w') as f:
            json.dump(config, f)

    # Aqui almaceno los tipos de cambio que voy a necesitar. Para forzar la descarga, borrarlo
    if os.path.isfile('cambio_euro_dolar.json'):
        with open('cambio_euro_dolar.json', 'r') as f:
            cambio_euro_dolar = json.load(f)
    else:
        cambio_euro_dolar = {}

    file = menu()

    # cargo datos desde el excel
    workbook = load_workbook(filename=file)
    sheet_1 = workbook['Closed Positions']

    # proceso los datos de posiciones cerradas
    estructura = defaultdict(dict)
    adquisiciones = 0
    transmisiones = 0
    total_profit_euros = 0
    total_fees_euros = 0
    ID_operaciones_cerradas = []
    for e in sheet_1.iter_rows(min_row=2,
                             max_col=15,
                             values_only=True):
        # creo una lista de operaciones cerradas
        ID_operaciones_cerradas.append(e[0])
        # este bloque calcula el total en euros
        inicial_dolar = float(e[3].replace(',', '.'))
        final_dolar = inicial_dolar + float(
            e[8].replace(',', '.'))  # calculo el valor final de la operacion sumando el beneficio al valos inicial
        inicial_fecha = adaptar_fecha(e[9])
        final_fecha = adaptar_fecha(e[10])
        if inicial_fecha not in cambio_euro_dolar:
            cambio_euro_dolar[inicial_fecha] = rate_dolar(inicial_fecha)
            # guardo los tipos de cambio en un fichero para reutilizarlo
            with open('cambio_euro_dolar.json', 'w') as f:
                json.dump(cambio_euro_dolar, f)
        inicial_cambio = cambio_euro_dolar[inicial_fecha]
        if final_fecha not in cambio_euro_dolar:
            cambio_euro_dolar[final_fecha] = rate_dolar(final_fecha)
            # guardo los tipos de cambio en un fichero para reutilizarlo
            with open('cambio_euro_dolar.json', 'w') as f:
                json.dump(cambio_euro_dolar, f)
        final_cambio = cambio_euro_dolar[final_fecha]
        inicial_euro = inicial_dolar * inicial_cambio
        adquisiciones = adquisiciones + inicial_euro
        final_euro = final_dolar * final_cambio
        transmisiones = transmisiones + final_euro
        total_profit_euros = total_profit_euros + final_euro - inicial_euro
        # Puesto así estoy calculando en euros al cambio del dia de la venta, en lugar de cuando se produce el gasto.
        total_fees_euros = total_fees_euros + float(e[13].replace(',', '.')) * final_cambio

        # aqui monto el diccionario con los resultados para cada trader copiado
        if e[2] is None:
            trader = 'Yo'
        else:
            trader = e[2]
        if trader not in estructura:
            estructura[trader]['profit'] = round(float(e[8].replace(',', '.')), 2)
            estructura[trader]['spread'] = round(float(e[7].replace(',', '.')), 2)
            estructura[trader]['fees'] = round(float(e[13].replace(',', '.')), 2)
            estructura[trader]['transacciones'] = 1
        else:
            estructura[trader]['profit'] += round(float(e[8].replace(',', '.')), 2)
            estructura[trader]['spread'] += round(float(e[7].replace(',', '.')), 2)
            estructura[trader]['fees'] += round(float(e[13].replace(',', '.')), 2)
            estructura[trader]['transacciones'] += 1

    # creo la lista de los trader copiados por orden alfabetico
    copiados = []
    for key in estructura:
        copiados.append(key)
    copiados = sorted(copiados, key=str.casefold)

    # proceso las transacciones realizadas
    sheet_2 = workbook['Transactions Report']
    equity_change_cerradas = 0
    equity_change_abiertas = 0
    fondos_aportados = 0
    gastos_deducibles_dolar = 0
    gastos_deducibles_euro = 0
    tipos_de_gastos_deducibles = ['Rollover Fee']

    for e in sheet_2.iter_rows(min_row=2,
                             max_col=9,
                             values_only=True):
        if e[2] in tipos_de_gastos_deducibles:
            fecha = e[0].strip()[:10]
            if fecha not in cambio_euro_dolar:
                cambio_euro_dolar[fecha] = rate_dolar(fecha)
                with open('cambio_euro_dolar.json', 'w') as f:
                    json.dump(cambio_euro_dolar, f)
            gastos_deducibles_dolar = gastos_deducibles_dolar + e[5]
            gastos_deducibles_euro = gastos_deducibles_euro + e[5] * cambio_euro_dolar[fecha]
        if e[4] in ID_operaciones_cerradas:
            equity_change_cerradas += e[6]
        else:
            if e[2] == 'Deposit':
                fondos_aportados += e[5]
            else:
                equity_change_abiertas += e[6]

    # inicio la impresion de resultados
    posicion_fecha_cierre_primera_operacion = 'K' + str(sheet_1.max_row)
    posicion_fecha_apertura_primera_operacion = 'J' + str(sheet_1.max_row)
    print()
    print('--- Desglose por trader')
    print()

    total_transacciones = 0
    total_profit = 0
    total_fees = 0
    total_spread = 0
    for e in copiados:
        print('Trader:', e)
        print(' Operaciones cerradas =', estructura[e]['transacciones'])
        print(' Profit =', '{:>8}'.format('{:.2f}'.format(estructura[e]['profit']) + '$'))
        print(' Fees   =', '{:>8}'.format('{:.2f}'.format(estructura[e]['fees']) + '$'))
        print(' Neto   =', '{:>8}'.format('{:.2f}'.format((estructura[e]['profit'] + estructura[e]['fees'])) + '$'))
        print(' Spread =', '{:>8}'.format('{:.2f}'.format(estructura[e]['spread'] * (-1)) + '$'))
        total_transacciones = total_transacciones + estructura[e]['transacciones']
        total_profit += round(estructura[e]['profit'], 2)
        total_fees += round(estructura[e]['fees'], 2)
        total_spread += round(estructura[e]['spread'], 2)
    print()
    print('--- Resumen operaciones')
    print()
    print('Fondos aportados: ', '{:>8}'.format('{:.2f}'.format(fondos_aportados) + '$'))
    print('Operaciones cerradas =', total_transacciones)
    print('Fecha apertura/cierre primera operación:', sheet_1[posicion_fecha_apertura_primera_operacion].value, '-',
          sheet_1[posicion_fecha_cierre_primera_operacion].value)
    print('Fecha cierre última operación:                             ', sheet_1['K2'].value)
    print('Profit total   =', '{:>8}'.format('{:.2f}'.format(total_profit) + '$'))
    print('Fees totales   =', '{:>8}'.format('{:.2f}'.format(total_fees) + '$'))
    print('Neto total     =', '{:>8}'.format('{:.2f}'.format(total_profit + total_fees) + '$'))
    print('Spread total   =', '{:>8}'.format('{:.2f}'.format(total_spread * (-1)) + '$'))
    print()
    print('--- IRPF')
    print('Total adquisiciones =', '{:>8}'.format('{:.2f}'.format(adquisiciones) + '€'))
    print('Total transmisiones =', '{:>8}'.format('{:.2f}'.format(transmisiones) + '€'))
    print('Ganancia Patrimonial =', '{:>8}'.format('{:.2f}'.format(transmisiones - adquisiciones) + '€'))
    print('Gastos =', '{:>8}'.format('{:.2f}'.format(gastos_deducibles_euro) + '€'))
    print()
    input('Pulsa Enter para cerrar...')
