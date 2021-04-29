# eToro_irpf
Script para calcular el irpf de las operaciones en eToro, teniendo en cuenta el cambio €/$ en la fecha de compra y de venta. El ECB no define cambio oficial los fines de semana ni los festivos, así que en caso de hacer una operación en uno de estos días se utilizará el primer dato anterior disponible.

Para descargar los datos necesarios ir a portfolio/history en la web de eToro y en el engranaje que hay arriba a la derecha elegir estado de la cuenta, seleccionando el período deseado.
Nos presentará en pantalla un documento de multiples páginas. En la parte de arriba pulsar el icono de excel para descargar la información en este formato. Mover el fichero descargado dentro del directorio donde está la aplicación.
Hacer doble click sobre irpf.exe y elegir del menu el fichero que queremos procesar.

La aplicación descarga automaticamente el cambio €/$ de la API del Banco Central Europeo. Si no se ha ejecutado nunca o hay datos nuevos que descargar, veremos en pantalla lo que está descargando.

Por defecto solo se descargan cambios desde el 31-12-2019. Si hay operaciones anteriores el programa dará error. Para corregirlo, editar el fichero config.ini y poner una fecha adecuada como fecha inicial. A continuación, borrar cambio_euro_dolar.txt y volver a ejecutar el programa.

En la salida por pantalla hay varios apartados:

  - Resumen de las operaciones desglosado por trader.

  - Resumen de operaciones.

  - IRPF

Puede haber una discrepancia entre las fees totales y los gastos, ya que el primero son las fees correspondientes a órdenes cerradas, con lo que puede haber fees que correspondan a un periodo anterior al contemplado. Por otro lado, los gastos contemplados en el apartado IRPF son gastos en el período, por lo que puede haber apuntes correspondientes a órdenes que no se han cerrado todavía.
