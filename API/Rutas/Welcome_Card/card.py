from fastapi import APIRouter, Response, HTTPException
from easy_pil import Editor, Font
from io import BytesIO
import requests
import logging

router = APIRouter()

@router.get("/api/welcome_card/")
def get_custom_image(avatar: str, background: str, ctx1: str="BIENVENIDO", ctx2: str="xquab#0", ctx3: str="Eres el Miembro 457"):
    try:
        # Obtener imagen del avatar
        avatar_response = requests.get(avatar)
        if avatar_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Fallo al descargar la imagen del avatar.")
        avatar_image = Editor(BytesIO(avatar_response.content)).resize((150, 150)).circle_image()

        # Obtener imagen de fondo
        background_response = requests.get(background)
        if background_response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Fallo al descargar la imagen de fondo. Código de estado: {background_response.status_code}, Razón: {background_response.reason}")
        
        # Cargar y redimensionar la imagen de fondo a 800x450
        background_editor = Editor(BytesIO(background_response.content)).resize((800, 450))

        # Preparar fuentes
        poppins = Font.poppins(size=50, variant="bold")
        poppins_small = Font.poppins(size=25, variant="regular")

        # Posicionamiento y dibujo en el fondo
        x_offset = 24
        background_editor.paste(avatar_image.image, (250 - x_offset, 90))

        # Calcular la caja delimitadora de la elipse
        caja_elipse = (250 - x_offset, 90, 250 - x_offset + 150, 90 + 150)
        background_editor.ellipse(caja_elipse, outline="white", width=5)

        background_editor.text((320 - x_offset, 260), ctx1, color="white", font=poppins, align="center")
        background_editor.text((320 - x_offset, 315), ctx2, color="white", font=poppins_small, align="center")
        background_editor.text((320 - x_offset, 350), ctx3, color="white", font=poppins_small, align="center")

        # Guardar la imagen final en un buffer
        img_buffer = BytesIO()
        background_editor.image.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        return Response(content=img_buffer.getvalue(), media_type="image/png")
    
    except Exception as e:
        logging.error(f"Error generando la imagen: {e}")
        raise HTTPException(status_code=500, detail=str(e))
