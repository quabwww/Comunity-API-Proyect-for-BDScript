from fastapi import APIRouter, HTTPException
from typing import List, Tuple, Dict
import random
import uuid

router = APIRouter()

# Definimos los valores de las cartas
VALORES_CARTAS = {
    '2': 2, '3': 4, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

# Almacenamiento de las partidas en curso
partidas: Dict[str, Dict] = {}

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

@router.get("/blackjack/nuevo/")
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

    # Verificar si el jugador puede hacer un split
    se_puede_split = mano_jugador[0][0] == mano_jugador[1][0]

    # Determinar si se puede hacer double down
    se_puede_double_down = len(mano_jugador) == 2  # Solo se puede double down con las dos primeras cartas

    return {
        "partida_id": partida_id,
        "mano_jugador": mostrar_mano(mano_jugador),
        "valor_jugador": calcular_valor_mano(mano_jugador),
        "mano_crupier": f"{mano_crupier[0][0]} de {mano_crupier[0][1]} y una carta oculta",
        "valor_crupier": VALORES_CARTAS[mano_crupier[0][0]],
        "cartas_restantes": len(baraja),
        "se_puede_split": se_puede_split,
        "se_puede_double_down": se_puede_double_down,
        "acciones_disponibles": ["pedir", "doblar"]
    }




@router.get("/api/get_blackjack/{partida_id}")
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
        "valor_crupier": calcular_valor_mano(partida["mano_crupier"]),
        "cartas_restantes": len(partida["baraja"])
    }

@router.get("/api/blackjack_action/{partida_id}/")
def accion_partida(partida_id: str, accion: str):
    """Realiza una acción en la partida (pedir, plantarse, doblar, split)."""
    partida = partidas.get(partida_id)
    if not partida:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
    
    if partida["finalizada"]:
        raise HTTPException(status_code=400, detail="La partida ya ha finalizado")

    if accion not in ["pedir", "plantarse", "doblar", "split"]:
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
                "valor_crupier": calcular_valor_mano(partida["mano_crupier"]),
                "cartas_restantes": len(partida["baraja"])
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
                "valor_crupier": calcular_valor_mano(partida["mano_crupier"]),
                "cartas_restantes": len(partida["baraja"])
            }

    if accion == "split":
        # Verificar si las dos cartas son del mismo valor para hacer split
        if partida["mano_jugador"][0][0] != partida["mano_jugador"][1][0]:
            raise HTTPException(status_code=400, detail="No se pueden dividir cartas de diferente valor")
        
        # Crear dos manos separadas para el jugador
        nueva_mano_jugador = [partida["mano_jugador"][0], repartir_carta(partida["baraja"])]
        partida["mano_jugador"] = [partida["mano_jugador"][1], repartir_carta(partida["baraja"])]

        # Jugar cada mano por separado
        manos_resultantes = []
        for mano in [nueva_mano_jugador, partida["mano_jugador"]]:
            while True:
                mostrar_mano_jugador = mostrar_mano(mano)
                valor_jugador = calcular_valor_mano(mano)
                
                if valor_jugador > 21:
                    manos_resultantes.append({
                        "mensaje": "¡El jugador se pasa! El crupier gana.",
                        "mano_jugador": mostrar_mano_jugador,
                        "valor_jugador": valor_jugador,
                        "mano_crupier": mostrar_mano(partida["mano_crupier"]),
                        "valor_crupier": calcular_valor_mano(partida["mano_crupier"]),
                        "cartas_restantes": len(partida["baraja"])
                    })
                    break
                
                decision = input(f"¿Qué acción deseas para la mano {mostrar_mano_jugador}? (pedir/plantarse/doblar): ")
                
                if decision not in ["pedir", "plantarse", "doblar"]:
                    raise HTTPException(status_code=400, detail="Acción no válida")
                
                if decision == "pedir":
                    mano.append(repartir_carta(partida["baraja"]))
                elif decision == "doblar":
                    mano.append(repartir_carta(partida["baraja"]))
                    break
                elif decision == "plantarse":
                    break
        
        partida["finalizada"] = True
        return {
            "manos_resultantes": manos_resultantes,
            "cartas_restantes": len(partida["baraja"])
        }
    
    if accion == "plantarse":
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
            "valor_crupier": valor_crupier,
            "cartas_restantes": len(partida["baraja"])
        }

    return {
        "mano_jugador": mostrar_mano(partida["mano_jugador"]),
        "valor_jugador": calcular_valor_mano(partida["mano_jugador"]),
        "mano_crupier": mostrar_mano(partida["mano_crupier"]),
        "valor_crupier": calcular_valor_mano(partida["mano_crupier"]),
        "cartas_restantes": len(partida["baraja"])
    }


