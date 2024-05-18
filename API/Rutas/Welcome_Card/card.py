from fastapi import APIRouter, Response, HTTPException
from easy_pil import Editor, Font
from io import BytesIO
import requests
import logging

router = APIRouter()

@router.get("/api/welcome_card/")
def get_custom_image(avatar: str, background: str, ctx1: str="WELCOME", ctx2: str="xquab#0", ctx3: str="You are the 457th Member"):
    try:
        
        avatar_response = requests.get(avatar)
        if avatar_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to download avatar image.")
        avatar_image = Editor(BytesIO(avatar_response.content)).resize((150, 150)).circle_image()


        background_response = requests.get(background)
        if background_response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to download background image. Status code: {background_response.status_code}, Reason: {background_response.reason}")
        
        background = Editor(BytesIO(background_response.content)).resize((900, 270))
        
        




        poppins = Font.poppins(size=50, variant="bold")
        poppins_small = Font.poppins(size=25, variant="regular")


        x_offset = 24


        background.paste(avatar_image.image, (250 - x_offset, 90))
        background.ellipse((250 - x_offset, 90), 150, 150, outline="white", stroke_width=5)


        background.text((320 - x_offset, 260), ctx1, color="white", font=poppins, align="center")
        background.text((320 - x_offset, 315), ctx2, color="white", font=poppins_small, align="center")
        background.text((320 - x_offset, 350), ctx3, color="white", font=poppins_small, align="center")



        img_buffer = BytesIO()
        background.image.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        return Response(content=img_buffer.getvalue(), media_type="image/png")
    except Exception as e:
        logging.error(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail=str(e))




