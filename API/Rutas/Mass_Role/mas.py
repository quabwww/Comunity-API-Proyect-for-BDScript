
from fastapi import APIRouter, HTTPException, Header
import requests

router = APIRouter()

@router.post("/api/mass_roles/")
async def manage_role_for_all_members(
    action: str = Header(..., description="Action to perform (add or remove)"),
    role_id: int = Header(..., description="ID of the role to add or remove"),
    bot_token: str = Header(..., description="Discord Bot Token"),
    guild_id: str = Header(..., description="Discord Server ID")
):
    if action not in ["add", "remove"]:
        raise HTTPException(status_code=400, detail="Invalid action, must be 'add' or 'remove'")

    headers = {
        "Authorization": f"Bot {bot_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/members", headers=headers, params={"limit": 1000})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch members")

    members = response.json()

    
    failed_members = []

    
    successful_members = 0
    for member in members:
        user_id = member["user"]["id"]
        if action == "add":
            response = requests.put(f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}/roles/{role_id}", headers=headers)
        else:
            response = requests.delete(f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}/roles/{role_id}", headers=headers)
        
        if response.status_code != 204:
            failed_members.append(user_id)
        else:
            successful_members += 1

    total_members = len(members)
    failed_members_count = len(failed_members)
    successful_members_count = total_members - failed_members_count

    return {
        "message": f"Role {action}ed for members. {successful_members_count} members were {action}ed successfully.",
        "total_members": total_members,
        "successful_members_count": successful_members_count,
        "failed_members_count": failed_members_count,
        "failed_members_ids": failed_members
    }

