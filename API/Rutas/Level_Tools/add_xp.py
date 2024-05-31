from fastapi import APIRouter

router = APIRouter()

@router.get("/api/add_xp/")
def xp(xp: int, req: int, level: int, bonus: int):
    xp += bonus

    while xp >= req:
        xp -= req
        req *= 2
        level += 1
    
    return {"xp": xp, "req": req, "level": level}
