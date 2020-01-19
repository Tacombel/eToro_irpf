# eToro_irpf
script para calcular el irpf de las operaciones en eToro, teniendo en cuenta el cambio €/$ en la fecha de compra y de venta.
Para descargar los datos necesario ir a portfolio/history en la web de eToro y en el engranaje que hay a la derecha elegir estado de la cuenta, seleccionando el período deseado.
Nos presentara en pantalla un documento de multiples páginas. En la parte de arriba pulsar el icono de excel para descargar la información.
A continuación abrir el fichero descargado en Google docs. Tenemos 4 pestañas. Abrir la que se llama Closed positions. Seleccionar todos los valores, incluyendo la primera fila y en el menu Archivo|Descargar elegir Valores separados por comas
Renombrar el fichero descargado a data-elnombre_que_queramos, por ejemplo data-2020.csv o data-202001-csv y moverlo al directorio app.
Ejecutar irpf.py y elegir el fichero correspondiente del menu.
La aplicación descarga automaticamente el cambio €/$ desde la API del BCE. Si no se ha ejecutado nunca o hay datos nuevos que descargar, veremos en pantalla lo que está descargando.
A continuación nos dice:
  La fecha de cierre de la primera y última operación para que verifiquemos que los datos son los que queremos examinar.
  El número de transaccioness, beneficio, comisiones y beneficio neto en dolares ordenado por trader, incluyendo las nuestras que aparecen bajo "Yo"
  Los totales, tanto en dolar como en euro.
