from fastapi import APIRouter, HTTPException
from typing import List, Tuple, Dict
import random
from API.Funciones_API.black_jack_funcs import crear_baraja, barajar_baraja, repartir_carta, calcular_valor_mano, mostrar_mano
import uuid

app = APIRouter()


VALORES_CARTAS = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

# Almacenamiento de las partidas en curso
partidas: Dict[str, Dict] = {}



@app.get("/blackjack-new/")
def nueva_partida():
    """Inicia una nueva partida de Blackjack."""
    # Crear y barajar la baraja
    baraja = crear_baraja()
    barajar_baraja(baraja)

    # Repartir las cartas iniciales
    mano_jugador = [repartir_carta(baraja), repartir_carta(baraja)]
    mano_crupier = [repartir_carta(baraja), repartir_carta(baraja)]

    # Crear un ID único para la partida
    partida_id = str(uuid.uuid4())
    partidas[partida_id] = {
        "baraja": baraja,
        "mano_jugador": mano_jugador,
        "mano_crupier": mano_crupier,
        "finalizada": False
    }

    return {
        "partida_id": partida_id,
        "mano_jugador": mostrar_mano(mano_jugador),
        "valor_jugador": calcular_valor_mano(mano_jugador),
        "mano_crupier": f"{mano_crupier[0][0]} de {mano_crupier[0][1]} y una carta oculta",
        "valor_crupier": VALORES_CARTAS[mano_crupier[0][0]]
    }
