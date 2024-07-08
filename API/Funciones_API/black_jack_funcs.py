from fastapi import APIRouter, HTTPException
from typing import List, Tuple, Dict
import random
import uuid
from API.Rutas.Blackjack.starts_blackjack import VALORES_CARTAS, partidas


def crear_baraja() -> List[Tuple[str, str]]:
    """Crea una baraja de cartas."""
    palos = ['Corazones', 'Diamantes', 'Tréboles', 'Picas']
    valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return [(valor, palo) for valor in valores for palo in palos]

def barajar_baraja(baraja: List[Tuple[str, str]]):
    """Baraja la baraja de cartas."""
    random.shuffle(baraja)

def repartir_carta(baraja: List[Tuple[str, str]]) -> Tuple[str, str]:
    """Reparte una carta de la baraja."""
    return baraja.pop()

def calcular_valor_mano(mano: List[Tuple[str, str]]) -> int:
    """Calcula el valor total de una mano."""
    valor = 0
    num_ases = 0
    for carta, _ in mano:
        valor += VALORES_CARTAS[carta]
        if carta == 'A':
            num_ases += 1
    
    while valor > 21 and num_ases:
        valor -= 10
        num_ases -= 1
    
    return valor

def mostrar_mano(mano: List[Tuple[str, str]]) -> str:
    """Muestra las cartas y el valor de una mano."""
    return ', '.join(f"{valor} de {palo}" for valor, palo in mano)
