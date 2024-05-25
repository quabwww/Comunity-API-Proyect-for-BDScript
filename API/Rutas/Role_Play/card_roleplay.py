from easy_pil import Editor, Canvas, Font
from io import BytesIO
from fastapi import APIRouter, Response, HTTPException, Query
import requests


router = APIRouter()

@router.get("/api/dni-card/")
def param(avatar: str, nombre: str=None, apellido: str=None, sexo: str=None, nacionalidad: str=None, edad: str=None, nacimiento: str=None):
    
    canvas = Canvas((350, 200), color="black")


    avatar_response = requests.get(avatar)
    if avatar_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to download avatar image.")
    perfil = Editor(BytesIO(avatar_response.content)).resize((100,100))


    fondo = Editor(canvas)


    poppins = Font.poppins(size=15, variant="bold")
    fondo.rectangle((-2, 50), width=450, height=200, color=(153,153,153,255), radius=1)
    fondo.paste(perfil, (30,70))


    poppins = Font.poppins(size=15, variant="bold")
    fondo.text((26, 20), text="DOCUMENTO NACIONAL DE IDENTIDAD",font=poppins ,color="white")

    NOM = Font.poppins(size=12, variant="bold")
    fondo.text((157, 75), text=f"NOMBRE: {nombre}",font=NOM ,color="black")


    fondo.text((157, 95), text=f"APELLIDO: {apellido}",font=NOM ,color="black")


    fondo.text((157, 116), text=f"SEXO: {sexo}",font=NOM ,color="black")


    fondo.text((157, 135), text=f"NACIONALIDAD:{nacionalidad} ",font=NOM ,color="black")

    fondo.text((157, 155), text=f"EDAD: {edad}",font=NOM ,color="black")

    fondo.text((157, 175), text=f"NACIMIENTO: {nacimiento}",font=NOM ,color="black")


    NOM2 = Font.poppins(size=8, variant="bold")
    fondo.text((28, 180), text="FOTOGRAFIA DE ARCHIVO",font=NOM2 ,color="black")

    img_buffer = BytesIO()
    fondo.image.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    return Response(content=img_buffer.getvalue(), media_type="image/png")

