import os


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


if __name__ == '__main__':
    menu()
