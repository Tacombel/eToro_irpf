# eToro_irpf
Script para calcular el irpf de las operaciones en eToro, teniendo en cuenta el cambio €/$ en la fecha de compra y de venta.

Para descargar los datos necesarios ir a portfolio/history en la web de eToro y en el engranaje que hay arriba a la derecha elegir estado de la cuenta, seleccionando el período deseado.
Nos presentara en pantalla un documento de multiples páginas. En la parte de arriba pulsar el icono de excel para descargar la información en este formato. Mover el fichero descargado dentro del directorio donde hemos puesto la aplicación.
Hacer doble click sobre irpf.exe y elegir del menu el fichero que queremos procesar.
La aplicación descarga automaticamente el cambio €/$. Es necesario tener una cuenta en https://currencylayer.com/ de al menos nivel free. Este nivel tiene una limitación de 250 consultas al mes, por lo que pueden darse situaciones en las que excedamos ese límite y el programa dará error.
Si no se ha ejecutado nunca o hay datos nuevos que descargar, veremos en pantalla lo que está descargando.
En la salida por pantalla hay varios apartados:
  Resumen de las operaciones desglosado por trader.
  Resumen de operaciones.
  IRPF
