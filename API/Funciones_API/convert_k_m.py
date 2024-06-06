def abreviar_numero(numero):
    if numero >= 1_000_000:
        return f'{numero / 1_000_000:.1f}M'
    elif numero >= 1_000:
        return f'{numero / 1_000:.1f}k'
    else:
        return str(numero)
