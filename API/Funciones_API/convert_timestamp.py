def segundos(solicitud: str):
    unidades = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'y': 31536000}
    resultado = 0
    cantidad = ''
    for caracter in solicitud:
        if caracter.isdigit():
            cantidad += caracter
        elif caracter in unidades:
            resultado += int(cantidad) * unidades[caracter]
            cantidad = ''
    return resultado