from fastapi import APIrouter, HTTPException
from typing import List, Tuple, Dict
import random
import uuid

app = APIrouter()


@app.get("/api/blackjack/{partida_id}/")
def accion_partida(partida_id: str, accion: str):
    """Realiza una acción en la partida (pedir, plantarse, doblar)."""
    partida = partidas.get(partida_id)
    if not partida:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
    
    if partida["finalizada"]:
        raise HTTPException(status_code=400, detail="La partida ya ha finalizado")

    if accion not in ["pedir", "plantarse", "doblar"]:
        raise HTTPException(status_code=400, detail="Acción no válida")

    if accion == "pedir":
        partida["mano_jugador"].append(repartir_carta(partida["baraja"]))
        valor_jugador = calcular_valor_mano(partida["mano_jugador"])
        if valor_jugador > 21:
            partida["finalizada"] = True
            return {
                "mensaje": "¡El jugador se pasa! El crupier gana.",
                "mano_jugador": mostrar_mano(partida["mano_jugador"]),
                "valor_jugador": valor_jugador,
                "mano_crupier": mostrar_mano(partida["mano_crupier"]),
                "valor_crupier": calcular_valor_mano(partida["mano_crupier"])
            }

    if accion == "doblar":
        partida["mano_jugador"].append(repartir_carta(partida["baraja"]))
        valor_jugador = calcular_valor_mano(partida["mano_jugador"])
        partida["finalizada"] = True
        if valor_jugador > 21:
            return {
                "mensaje": "¡El jugador se pasa! El crupier gana.",
                "mano_jugador": mostrar_mano(partida["mano_jugador"]),
                "valor_jugador": valor_jugador,
                "mano_crupier": mostrar_mano(partida["mano_crupier"]),
                "valor_crupier": calcular_valor_mano(partida["mano_crupier"])
            }
    
    if accion == "plantarse" or accion == "doblar":
        # Turno del crupier
        while calcular_valor_mano(partida["mano_crupier"]) < 17:
            partida["mano_crupier"].append(repartir_carta(partida["baraja"]))
        
        valor_jugador = calcular_valor_mano(partida["mano_jugador"])
        valor_crupier = calcular_valor_mano(partida["mano_crupier"])
        partida["finalizada"] = True

        if valor_crupier > 21 or valor_jugador > valor_crupier:
            mensaje = "¡El jugador gana!"
        elif valor_jugador < valor_crupier:
            mensaje = "El crupier gana."
        else:
            mensaje = "Es un empate."
        
        return {
            "mensaje": mensaje,
            "mano_jugador": mostrar_mano(partida["mano_jugador"]),
            "valor_jugador": valor_jugador,
            "mano_crupier": mostrar_mano(partida["mano_crupier"]),
            "valor_crupier": valor_crupier
        }

    return {
        "mano_jugador": mostrar_mano(partida["mano_jugador"]),
        "valor_jugador": calcular_valor_mano(partida["mano_jugador"]),
        "mano_crupier": mostrar_mano(partida["mano_crupier"]),
        "valor_crupier": calcular_valor_mano(partida["mano_crupier"])
    }
