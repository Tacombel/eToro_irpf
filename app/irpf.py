# python 3.6
# Pueden aparecer pequeñas discrepancias entre este listado y los de eToro, ya que este solo considera operaciones
# cerradas. Los rollover/dividends liquidados en el periodo no se tienen en cuen ta aqui, pero si en el script de
# transacciones. En buena ley se deberían considerar aquí como parte del período, y restarlos como ya aplicados en el
# período siguiente, pero dado que los importes son pequeños por ahora no me complico. Por ejemplo, en el años 2019
# faltaría por aplicar 6 centimos con lo que el neto total serian 437$ en lugar de 436.94$, difiriendo esos 6 centimos
# de gastos al momento en que se cierren las correspondientes ordenes.

from collections import defaultdict
import requests
import json
import os.path
from openpyxl import load_workbook

import elegir_fichero


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


if __name__ == '__main__':
    # Aqui almaceno los tipos de cambio que voy a necesitar. Para forzar la descarga, borrarlo
    if os.path.isfile('cambio_euro_dolar.json'):
        with open('cambio_euro_dolar.json', 'r') as f:
            cambio_euro_dolar = json.load(f)
    else:
        cambio_euro_dolar = {}

    file = elegir_fichero.menu()

    # cargo datos desde el excel
    workbook = load_workbook(filename=file)
    sheet = workbook['Closed Positions']

    # proceso los datos
    estructura = defaultdict(dict)
    total_profit_euros = 0
    total_fees_euros = 0
    for e in sheet.iter_rows(min_row=2,
                             max_col=15,
                             values_only=True):
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
        final_cambio = cambio_euro_dolar[final_fecha]
        inicial_euro = inicial_dolar * inicial_cambio
        final_euro = final_dolar * final_cambio
        total_profit_euros = total_profit_euros + final_euro - inicial_euro
        total_fees_euros = total_fees_euros + float(e[13].replace(',', '.')) * final_cambio

        # aqui monto el diccionario con los resultados para cada trader copiado
        if e[2] is None:
            trader = 'Yo'
        else:
            trader = e[2]
        if trader not in estructura:
            estructura[trader]['profit'] = round(float(e[8].replace(',', '.')), 2)
            estructura[trader]['fees'] = round(float(e[13].replace(',', '.')), 2)
            estructura[trader]['transacciones'] = 1
        else:
            estructura[trader]['profit'] = estructura[trader]['profit'] + round(float(e[8].replace(',', '.')), 2)
            estructura[trader]['fees'] = estructura[trader]['fees'] + round(float(e[13].replace(',', '.')), 2)
            estructura[trader]['transacciones'] += 1

    # creo la lista de los trader copiados por orden alfabetico
    copiados = []
    for key in estructura:
        copiados.append(key)
    copiados = sorted(copiados, key=str.casefold)

    # inicio la impresion de resultados
    posicion_fecha_cierre_primera_operacion = 'K' + str(sheet.max_row)
    posicion_fecha_apertura_primera_operacion = 'J' + str(sheet.max_row)
    print()
    print('Fecha apertura primera operación', sheet[posicion_fecha_apertura_primera_operacion].value)
    print('Fecha cierre primera operación  ', sheet[posicion_fecha_cierre_primera_operacion].value)
    print('Fecha cierre última operación   ', sheet['K2'].value)
    print()

    total_transacciones = 0
    total_profit = 0
    total_fees = 0
    for e in copiados:
        print('Trader:', e)
        print(' Transacciones =', estructura[e]['transacciones'])
        print(' Profit =', '{:>8}'.format('{:.2f}'.format(estructura[e]['profit']) + '$'))
        print(' Fees   =', '{:>8}'.format('{:.2f}'.format(estructura[e]['fees']) + '$'))
        print(' Neto   =', '{:>8}'.format('{:.2f}'.format((estructura[e]['profit'] + estructura[e]['fees'])) + '$'))
        total_transacciones = total_transacciones + estructura[e]['transacciones']
        total_profit = total_profit + round(estructura[e]['profit'], 2)
        total_fees = total_fees + round(estructura[e]['fees'], 2)

    print('-----------------------------')
    print('Transacciones totales =', total_transacciones)
    print('Profit total =', '{:>8}'.format('{:.2f}'.format(total_profit) + '$'),
          '{:>8}'.format('{:.2f}'.format(total_profit_euros) + '€'))
    print('Fees totales =', '{:>8}'.format('{:.2f}'.format(total_fees) + '$'),
          '{:>8}'.format('{:.2f}'.format(total_fees_euros) + '€'))
    print('Neto total   =', '{:>8}'.format('{:.2f}'.format(total_profit + total_fees) + '$'),
          '{:>8}'.format('{:.2f}'.format(total_profit_euros + total_fees_euros) + '€'))
