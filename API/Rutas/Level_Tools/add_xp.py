from fastapi import APIRouter


router = APIRouter()


@router.get("/api/add_xp/)
def xp(xp:str, req:str, level: str, bonus:str):
  xp += bonus
  
  while xp >= req:
    xp -= req
    req *= 2
    level += 1
  return {"xp": xp, "req": req, "level": level}
