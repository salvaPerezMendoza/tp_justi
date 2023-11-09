import matplotlib.pyplot as plt
from datetime import datetime

def leer_nombres(archivo):
        # Lee la primera linea 
    lineaNombres = archivo.readline()
        # Divide la linea en palabras usando split()
    return lineaNombres.split()

def inicializar_deudas(nombres):
        # Iniccializo el diccionario de deudas en 0
    return {nombre: 0 for nombre in nombres}

def agregar_nuevo_nombre(datos, nombres, deudas):
        # Agrega un nuevo nombre
    nombres.append(datos[2])
        # Inicializa la deuda del nuevo en 0
    deudas[datos[2]] = 0 
    
def comparar_fechas(fecha, fechaLimite):
        # Usando la libreria datetime convierto las fechas a objeto de fecha
    fecha1 = datetime.strptime(fecha, '%Y-%m-%d')
    fecha2 = datetime.strptime(fechaLimite, '%Y-%m-%d')
    
        # Comparar si la fecha ya ha pasado y devuelvo 0/1 para saber el resultado
    if fecha1 <= fecha2:
        return 0
    else:
        return 1
    

def analisar_agregar(datos, nombres, deudas):
    # Si es "~", puede haberse dividido entre todos o todos menos alguien
    if datos[3] == "~":
            # Si tiene solo 4 datos, se dividi— entre todos
        if len(datos) == 4:
            
                # Se distribuye entre todos
            for nombre in nombres:
                deudas[nombre] += int(datos[2]) / len(nombres)
                
                # Busco quien pago para restarle lo que puso
            if datos[1] in deudas:
                deudas[datos[1]] -= int(datos[2])
                
        else:
            
                # Si se distribuye entre todos menos algunos
            if datos[3] == "~":
                    # Buscar quien pago
                pagador = datos[1]
                
                    # Buscar quiŽnes son los que no pagan
                excluidos = datos[4:]
                
                    # Calcula la cantidad que se divide entre todos menos los excluidos
                plataPagada = int(datos[2])
                pagan = [inquilino for inquilino in nombres if inquilino not in excluidos]
                plataPagar = plataPagada / len(pagan)
                
                    # Distribuye el gasto entre los que pagan
                for inquilino in pagan:
                    deudas[inquilino] += plataPagar
                
                    # Restale el valor al que pago
                deudas[pagador] -= plataPagada
            
        # Como el tercer dato es diferente de "~", solo queda la posibilidad de que se distribuya entre algunos
    else:
            
        if datos[3] != "~":
                # Buscar quien pago
            pagador = datos[1]
            
                # Buscar quiŽnes son los que pagan
            pagan = datos[3:]
            
                # Calcula la cantidad que se divide entre los que pagan
            plataPagada = int(datos[2])
            plataPagar = plataPagada / len(pagan)
            
                # Distribuye el gasto entre los que pagan
            for inquilino in pagan:
                deudas[inquilino] += plataPagar
            
                # Restale el valor al que pago
            deudas[pagador] -= plataPagada
            

    # No es usado nunca pero si se quiere mostrar por pantalla sirve
def mostrar_datos(deudas):
    print(deudas)
    
def analisarFecha(nombre_archivo, fechaLimite):
        # Abro el archivo
    archivo = open(nombre_archivo)
        # Me salteo la linea de nombre
    linea = archivo.readline()
        # Guardo primer linea con informacion
    linea = archivo.readline()
        # Separo las palabras de la primera linea
    datos = linea.split()
        # Cierro el archivo
    archivo.close()
        
        # Analizo si la fecha a estudiar tiene sentido
    if comparar_fechas(datos[0], fechaLimite) == 1:
        return 1
    

def procesar_archivo(nombre_archivo, fechaLimite):
    
    with open(nombre_archivo, 'r') as archivo: 
                
            # Almaceno las palabras de la primer fila en un vector nombres mandandole a la funcion leer_nombres mi archivo para que lo "desarme"
        nombres = leer_nombres(archivo)
            # Iniccializo el diccionario de deudas en 0
        deudas = inicializar_deudas(nombres)
            # Nuevo diccionario para registrar la evolucion de las deudas
        evolucionDeudas = {}
            
            # Comenzar a leer linea por linea, salteando la primera que son los nombres
        for linea in archivo:
                
                # Guardar los datos en un vector datos
            datos = linea.split()
                
                  # Si es distinto de * significa que no agrego un nuevo nombre
            if datos[1] != '*':
                    #Sabiendo que se trata de alguna "agregacion" a las deudas, le paso la informacion a la funcion analisar para que me agregue al diccionario la informacion
                analisar_agregar(datos, nombres, deudas)
                       
            else:
                    # Paso la informacion para que agreguen un nuevo nombre con deuda en 0
                agregar_nuevo_nombre(datos, nombres, deudas) 
        
                # Almaceno en la variable fecha la fecha que este en esa linea
            fecha = datos[0]
                # Almacena una copia del diccionario de deudas en cada fecha
            evolucionDeudas[fecha] = dict(deudas)  
                
                # Como nesesito saber hasta que fecha del archivo es la que alcanza la fecha introducida, lo puedo saber haciendo esto para luego inroducirlo en evolucionDeudas y lograr saber la deuda en ese momento 
            if comparar_fechas(fecha, fechaLimite) == 0:
                fechaLimiteArchivo = fecha
                    
            # Devuelvo las deudas fecha a fecha para poder graficar y tambien las deudas hasta la fecha pedida para poder hacer los graficos circulares
        return evolucionDeudas, fechaLimiteArchivo
  
        
                

def graficar_evolucion_deudas(evolucionDeudas):
    
        # Lista almacena todas las claves fechas del diccionario evolucionDeudas, cada fecha se convierte en un elemento de la lista
    fechas = list(evolucionDeudas.keys())
        # Lista almacena todas los valores deudas fecha a fecha del diccionario evolucionDeudas, cada deuda se convierte en un elemento de la lista.
    deudas = list(evolucionDeudas.values())
    
        # Lista de deudores actuales como una lista vacia
    deudoresAgregar = []
    
    for registro in deudas:
        # Actualiza la lista de deudores actuales con los nombres que aparecen en este registro
        for nombre in registro.keys():
            if nombre not in deudoresAgregar:
                deudoresAgregar.append(nombre)
    
    
    for nombre in deudoresAgregar:
            # Lista que contiene la deuda de cada persona en cada fecha
            # Lo que logro con esta lista, es que si el nombre de la persona no aparece todavia -> no se agrego todavia -> no se va a graficar, recien cuando aparezca se empieza
       deuda_por_persona = [registro.get(nombre, None) for registro in deudas]
           # El eje x, el primero, representa las fechas, el eje y, el segundo, representa la deuda en pesos, y label=nombre se utiliza para etiquetar la l’nea con el nombre de la persona
           # Al estar en un bucle este va armando el grafico fecha a fecha modificando el valor de deuda
       plt.plot(fechas, deuda_por_persona, label=nombre)
        
        # Titulo x
    plt.xlabel("Fecha")
        # Titulo y
    plt.ylabel("Deuda")
        # Me especifica que color es cada deudor
    plt.legend() 
        #Para que solo muestre la primera y ultima fecha
    plt.xticks([fechas[0], fechas[-1]])
        # Mostrar en pantalla
    plt.show()
    
def graficar_pagan_cobran(evolucionDeudas, fechaLimiteArchivo):
    
    # Obtener las deudas en la fecha limite
    deudas_en_fecha = evolucionDeudas.get(fechaLimiteArchivo, {})

    # Separar las personas a las que se les debe plata y las que deben plata
    cobradores = {nombre: deuda for nombre, deuda in deudas_en_fecha.items() if deuda > 0}
    pagadores = {nombre: -deuda for nombre, deuda in deudas_en_fecha.items() if deuda < 0}

    if pagadores:
            # Crear el primer grafico para aquellos a los que se les debe plata
        plt.figure(1, figsize=(5, 6))
            # Titulo
        plt.title("A esta gente le deben plata")
        plt.pie(pagadores.values(), labels=[f"{nombre}: '{deuda}'" for nombre, deuda in pagadores.items()])        
            # Mostrar en pantalla
        plt.show()

    if cobradores:
            # Crear el segundo grafico para aquellos que deben plata
        plt.figure(2, figsize=(5, 6))
            # Titulo
        plt.title("Esta gente debe plata")
        plt.pie(cobradores.values(), labels=[f"{nombre}: '{deuda}'" for nombre, deuda in cobradores.items()])             
            # Mostrar en pantalla
        plt.show()


 

nombre_archivo = 'transacciones_largo.txt'

# El ususario ingresa la fecha hasta la cual analizar
fechaLimite = input("Ingrese una fecha limite en formato AAAA-MM-DD: ")

#Si la fecha es anterior a la primer fecha del archivo, debe imprimir por pantalla que la fecha ingresada no es válida
if analisarFecha(nombre_archivo, fechaLimite) != 1:

    # Procesar el archivo para obtener la evolucion de las deudas
    evolucionDeudas, fechaLimiteArchivo = procesar_archivo(nombre_archivo, fechaLimite)
    
    # Llamar a la funcion para graficar la evolucion de las deudas
    graficar_evolucion_deudas(evolucionDeudas)
    
    # Llamar a la funcion para graficar quienes deben y quienes cobran en la fecha especificada
    graficar_pagan_cobran(evolucionDeudas, fechaLimiteArchivo)
    
    print(evolucionDeudas[fechaLimiteArchivo])
    print(evolucionDeudas["2022-01-03"])
    print(evolucionDeudas["2022-01-08"])
else:
    print("Fecha ingresada no es válida")


