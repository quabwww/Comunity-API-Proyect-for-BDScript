from easy_pil import Editor, Canvas, Font
from io import BytesIO
from fastapi import APIRouter, Response, HTTPException
import requests

router = APIRouter()

@router.get("/api/level_up/")
def level(avatar: str, level:int):
    if not str(level).isdigit(): 
        level = 1
       
    canvas = Canvas((700, 130), color=(0, 0, 0, 0))
    editor = Editor(canvas.image)

   
    avatar_response = requests.get(avatar)
    if avatar_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to download avatar image.")
    profile = Editor(BytesIO(avatar_response.content)).resize((101, 101)).circle_image()

   
    poppins = Font.poppins(size=30)
    desplazamiento_x = 17  
    editor.rectangle((110, 16), width=230, height=100, fill="#25262a", radius=15)
    editor.ellipse((30 + desplazamiento_x, 11), width=110, height=110, outline="white", stroke_width=8)
    editor.text((180, 57), f"level {level}", font=poppins, color="white")
    editor.paste(profile.image, (35 + desplazamiento_x, 16))

    
    img_buffer = BytesIO()
    editor.image.save(img_buffer, format="PNG")
    img_buffer.seek(0)

       
    return Response(content=img_buffer.getvalue(), media_type="image/png")
