# eToro_irpf
Script para calcular el irpf de las operaciones en eToro, teniendo en cuenta el cambio €/$ en la fecha de compra y de venta.
Descargar el fichero eToro_parser-xx.7z del apartado de releases y descomprimirlo en un directorio.

Para descargar los datos necesarios ir a portfolio/history en la web de eToro y en el engranaje que hay a la derecha elegir estado de la cuenta, seleccionando el período deseado.
Nos presentara en pantalla un documento de multiples páginas. En la parte de arriba pulsar el icono de excel para descargar la información. Mover el fichero descargado dentro del directorio donde hemos puesto la aplicación.
Hacer doble click sobre irpf.exe y elegir del menu el fichero que queremos procesar.
La aplicación descarga automaticamente el cambio €/$ desde la API del BCE. Si no se ha ejecutado nunca o hay datos nuevos que descargar, veremos en pantalla lo que está descargando.
A continuación nos dice, referente a las operaciones cerradas en dicho período:
  La fecha de cierre de la primera y última operación para que verifiquemos que los datos son los que queremos examinar.
  El número de transaccioness, beneficio, comisiones y beneficio neto en dolares ordenado por trader, incluyendo las nuestras que aparecen bajo "Yo"
  Los totales, tanto en dolar como en euro.
Como es posible que tengamos operaciones pendientes de cerrar, en la última parte procesa las transacciones realizadas en el período, detallando los gastos atribuidos a estas, así como los fondos aportados a la cuenta en dicho período.
