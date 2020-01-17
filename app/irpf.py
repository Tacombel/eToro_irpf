import csv

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
    rollover_fees_and_dividends = 0.00
    profit = 0.00
    for e in datos:
        rollover_fees_and_dividends = rollover_fees_and_dividends + round(float(e[13]), 2)
        profit = profit + round(float(e[8]), 2)
    rollover_fees_and_dividends = round(rollover_fees_and_dividends, 2)
    profit = round(profit, 2)
    print(len(datos), 'transacciones')
    print('Rollover Fees And Dividends =', str(rollover_fees_and_dividends) + '$')
    print('Profit', str(profit) + '$')
