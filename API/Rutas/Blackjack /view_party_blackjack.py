from fastapi import APIRouter, HTTPException
from typing import List, Tuple, Dict
import random
import uuid

app = APIRouter()

@app.get("/api/blackjack/{partida_id}")
def estado_partida(partida_id: str):
    """Obtiene el estado actual de una partida."""
    partida = partidas.get(partida_id)
    if not partida:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
    
    if partida["finalizada"]:
        raise HTTPException(status_code=400, detail="La partida ya ha finalizado")

    return {
        "mano_jugador": mostrar_mano(partida["mano_jugador"]),
        "valor_jugador": calcular_valor_mano(partida["mano_jugador"]),
        "mano_crupier": mostrar_mano(partida["mano_crupier"]),
        "valor_crupier": calcular_valor_mano(partida["mano_crupier"])
    }
