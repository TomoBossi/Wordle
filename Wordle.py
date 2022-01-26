import datetime 
import random
import string
import os 
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# 1 Setear parámetros
abecedario = list(string.ascii_lowercase+'ñ') # excluye caracteres extraños/decorados/numéricos
nLetras    = 5 # largo de la palabra target y de todas las palabras que podrán ser input del jugador
nIntentos  = 6 # n° de intentos permitidos, incluyendo el primero
dificil    = False # Flase baja dificultad, True alta dificultad (requiere usar todas las pistas disponibles en adivinaciones sucesivas) (opcional)
diaria     = False # (opcional)
# Si diaria = True, se fija random.seed() con un identificador único del día actual. La palabra target es invariante durante el día entero
# Si diaria = False, la palabra target es elegida al azar en cada ejecución, independientemente de la fecha

# 2 Cargar el diccionario
diccionario = open('diccionario.txt').read().splitlines() # Debe estar en el mismo directorio que este archivo .py

# 3, 14 (optativo) Analizar si una palabra es formable (es de largo nLetras y se forma únicamente usando caracteres del abecedario)
def esFormable(palabra, abecedario, nLetras):
    return [(len(palabra) == nLetras), all([letra in abecedario for letra in palabra])]

# 4, 14 (optativo) Filtrar el diccionario para quedarse solo con las palabras de largo nLetras que excluyan caracteres extraños (palabras formables)
def generarSubdiccionario(diccionario, abecedario, nLetras):
    subdicc = []
    for palabra in diccionario:
        subdicc += [palabra] * all(esFormable(palabra, abecedario, nLetras))
    return subdicc

# tilde = []
# for palabra in diccionario:
#     for letra in ['á','é','í','ó','ú']:
#         tilde.append(letra in palabra)
# print(True in tilde)

# 5 Procesar una palabra cualquiera para compatibilizarla con las caracteristicas de diccionario.txt
def procesar(palabra):
    procesada  = palabra.lower() # Llevar a lowercase
    reemplazos = {'á': 'a',
                  'é': 'e',
                  'í': 'i',
                  'ó': 'o',
                  'ú': 'u'}
    for letraTildada in reemplazos.keys():
        procesada = procesada.replace(letraTildada, reemplazos[letraTildada]) # Eliminar tildes
    return procesada

# 6 Pedir input del jugador y procesarlo
def pedirPalabra():
    return procesar(str(input('Ingrese una palabra: ')))

# 7, 13 (optativo), 14 (optativo) Analizar si un input es válido (es de largo nLetras, se forma únicamente usando caracteres del abecedario, está en el (sub)diccionario y no está en la lista de inputs previos)
# Output en orden: [Largo valido, caracteres validos, presente en diccionario, no repetida]
def esValido(input, subdicc, abecedario, repetidas = []):
    return esFormable(input, abecedario, len(subdicc[0])) + [(input in subdicc), input not in repetidas] # formato lista optativo

# 8 Elegir palabra target/objetivo
def palabraTarget(subdicc):
    return random.choice(subdicc)

# 9 Comparar target e input. En este punto, target e input deben tener igual largo.
# Codificación:  1: bien ubicada, 
#                0: no tan bien ubicada, 
#               -1: letra no presente en target
def comparar(target, input):
    comparacion = []
    rep = {letra: target.count(letra) for letra in target}
    for i, letraInput in enumerate(input):
        ubicacion = -1
        if letraInput in target and rep[letraInput]:
            ubicacion = 1 - (letraInput != target[i])
            rep[letraInput] -= 1
        comparacion.append(ubicacion)
    return comparacion

# print(comparar('xxxxx', 'xxxxx'), # [ 1,  1,  1,  1,  1]
#       comparar('xxxxx', 'yyyyy'), # [-1, -1, -1, -1, -1]
#       comparar('knoll', 'lobos'), # [ 0,  0, -1, -1, -1]
#       comparar('casio', 'patos')) # [-1,  1, -1,  0,  0]

# 10 Generar output intuitivo en consola a partir de la comparación entre el target y el input del usuario
def mostrarPistas(input, comparacion):
    pistas = ''
    for ubicacion in comparacion:
        pistas += '+'*(ubicacion==1) + '-'*(ubicacion==0) + '_'*(ubicacion==-1)
    print(input)
    print(pistas)

# mostrarPistas('patos', comparar('casio', 'patos')) # patos
#                                                    # _+_--

# 11, 13 (optativo), 14 (optativo) Jugar un intento
def jugarIntento(target, subdicc, abecedario, repetidas = []):
    input         = pedirPalabra()
    inputValido   = esValido(input, subdicc, abecedario, repetidas)
    errores       = ['Tu palabra no es del largo correcto.',
                     'Tu palabra tiene algún caracter extraño.',
                     'Tu palabra no está en el diccionario.',
                     'Ya probaste esa palabra!'] # Lista de errores jerarquizados
    while not all(inputValido):
        print(errores[inputValido.index(False)], 'Intentá nuevamente.')
        input       = pedirPalabra()
        inputValido = esValido(input, subdicc, abecedario, repetidas)
    repetidas.append(input) # repetidas es modificada in-place
    comparacion = comparar(target, input)
    mostrarPistas(input, comparacion)
    return target == input

# 12 Jugar partida
def jugarPartida(nLetras, nIntentos, diccionario, abecedario):
    subdicc   = generarSubdiccionario(diccionario, abecedario, nLetras)
    target    = palabraTarget(subdicc) 
    repetidas = []
    victoria  = False
    i = 0
    while not victoria and i < nIntentos:
        print('#### Intento '+str(i+1)+' ####')
        victoria = jugarIntento(target, subdicc, abecedario, repetidas)
        i += 1

    if victoria:
        print('Ganaste en '+str(i)+' intentos!')
    else:
        print('F. La palabra era '+target+'.')
    return victoria

# 15 (opcional) Setear la semilla diaria, agregar variable diaria en # 1
def semillaDiaria():
    hoy = datetime.datetime.today().replace(hour = 0, minute = 0, second = 0)
    id  = int(datetime.datetime.timestamp(hoy))
    return id

def jugarPartida(nLetras, nIntentos, diccionario, abecedario, diaria):
    if diaria: random.seed(semillaDiaria())
    subdicc   = generarSubdiccionario(diccionario, abecedario, nLetras)
    target    = palabraTarget(subdicc) 
    repetidas = []
    victoria  = False
    i = 0
    while not victoria and i < nIntentos:
        print('#### Intento '+str(i+1)+' ####')
        victoria = jugarIntento(target, subdicc, abecedario, repetidas)
        i += 1

    if victoria:
        print('Ganaste en '+str(i)+' intentos!')
    else:
        print('F. La palabra era '+target+'.')
    return victoria

# 16 (opcional) definir usaPistas() y modificar esValido(), jugarIntento() y jugarPartida() para permitir la elección de dificultad (False baja, True alta), agregar variable dificil en # 1
# Que todas las pistas se usen implica:
# Las letras en posicion correcta deben permanecer en posicion
# Las letras en posicion no tan correcta deben utilizarse en como minimo igual cantidad de veces que la cantidad de veces que aparecen no tan bien ubicadas en la pista
# Por lo tanto se requerirá una constancia de la posición y un contador de letras, de forma analoga a lo hecho para comparar()
def usaPistas(input, prevInput, prevComparacion):
    comparacionInputs = comparar(input, prevInput)
    prevInputFiltrado = [letra for i, letra in enumerate(prevInput) if prevComparacion[i] in [0, 1]]
    letrasObligadas   = {letra: prevInput.count(letra) for letra in prevInputFiltrado}
    for i, ubicacion in enumerate(prevComparacion):
        if prevInput[i] in letrasObligadas.keys() and letrasObligadas[prevInput[i]]:
            if (ubicacion == 1 and comparacionInputs[i] == 1) or (ubicacion == 0 and comparacionInputs[i] in [0, 1]):
                letrasObligadas[prevInput[i]] -= 1
    return all([letrasObligadas[letra] == 0 for letra in letrasObligadas.keys()])

# print(usaPistas('amuse', 'audio', [ 0,  1, -1, -1, -1]), # False
#       usaPistas('muase', 'audio', [ 0,  1, -1, -1, -1]), # True
#       usaPistas('uadio', 'audio', [-1,  1,  1,  1,  1]), # False
#       usaPistas('aaaxx', 'fuaaa', [-1, -1,  1,  0,  0]), # True
#       usaPistas('xaaxx', 'fuaaa', [-1, -1,  1,  0,  0])) # False

def esValido(input, subdicc, abecedario, repetidas, dificil = 0, prevInput = '', comparacion = []):
    return esFormable(input, abecedario, len(subdicc[0])) + [(input in subdicc), input not in repetidas] + [usaPistas(input, prevInput, comparacion)] * dificil

def jugarIntento(target, subdicc, abecedario, repetidas, dificil = 0, prevInput = '', comparacion = []):
    input         = pedirPalabra()
    inputValido   = esValido(input, subdicc, abecedario, repetidas, dificil, prevInput, comparacion)
    errores       = ['Tu palabra no es del largo correcto.',
                     'Tu palabra tiene algún caracter extraño.',
                     'Tu palabra no está en el diccionario.',
                     'Ya probaste esa palabra!',
                     'Tenés que usar todas las pistas disponibles!'] # Lista de errores jerarquizados
    while not all(inputValido):
        print(errores[inputValido.index(False)], 'Intentá nuevamente.')
        input       = pedirPalabra()
        inputValido = esValido(input, subdicc, abecedario, repetidas, dificil, prevInput, comparacion)
    repetidas.append(input) # repetidas es modificada in-place
    comparacion = comparar(target, input)
    mostrarPistas(input, comparacion)
    return input, comparacion

def jugarPartida(nLetras, nIntentos, diccionario, abecedario, diaria = True, dificil = False):
    if diaria: random.seed(semillaDiaria())
    subdicc     = generarSubdiccionario(diccionario, abecedario, nLetras)
    target      = palabraTarget(subdicc)
    repetidas   = []
    prevInput   = nLetras * ' '
    comparacion = nLetras * [-1]
    victoria    = False
    i = 0
    while not victoria and i < nIntentos:
        print('#### Intento '+str(i+1)+' ####')
        prevInput, comparacion = jugarIntento(target, subdicc, abecedario, repetidas, dificil, prevInput, comparacion)
        victoria = all([ubicacion == 1 for ubicacion in comparacion])
        i += 1

    if victoria:
        print('Ganaste en '+str(i)+' intentos!')
    else:
        print('F. La palabra era '+target+'.')
    return victoria

jugarPartida(nLetras, nIntentos, diccionario, abecedario, dificil)

# 17 Go off