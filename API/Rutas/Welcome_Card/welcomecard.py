from fastapi import APIRouter, Response, HTTPException
from easy_pil import Editor, Font
from io import BytesIO
import requests
import logging

app = APIRouter()

@router.get("/image/")
def get_custom_image(avatar: str, background: str, ctx1: str="WELCOME", ctx2: str="xquab#0", ctx3: str="You are the 457th Member"):
    try:
        # Download and process avatar image
        avatar_response = requests.get(avatar)
        if avatar_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to download avatar image.")
        avatar_image = Editor(BytesIO(avatar_response.content)).resize((150, 150)).circle_image()

        # Download and process background image
        background_response = requests.get(background)
        if background_response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to download background image. Status code: {background_response.status_code}, Reason: {background_response.reason}")
        background_image = Editor(BytesIO(background_response.content)).resize((800, 400)).image

        # Define fonts for text overlay
        poppins = Font.poppins(size=50, variant="bold")
        poppins_small = Font.poppins(size=25, variant="regular")

        # Define the amount of horizontal shift (2 cm in pixels)
        horizontal_shift = 60

        # Create a new Editor object for the background image
        editor = Editor(background_image)

        # Overlay avatar image on background (move 2 cm to the right)
        editor.paste(avatar_image.image, (250 + horizontal_shift, 90))
        editor.ellipse((250 + horizontal_shift, 90), 150, 150, outline="white", stroke_width=5)

        # Add text overlays (move 2 cm to the right)
        editor.text((320 + horizontal_shift, 260), ctx1, color="white", font=poppins, align="center")
        editor.text((320 + horizontal_shift, 315), ctx2, color="white", font=poppins_small, align="center")
        editor.text((320 + horizontal_shift, 350), ctx3, color="white", font=poppins_small, align="center")

        # Save the edited image to a buffer
        img_buffer = BytesIO()
        editor.image.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        # Return the image as a response
        return Response(content=img_buffer.getvalue(), media_type="image/png")
    
    except Exception as e:
        logging.error(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

