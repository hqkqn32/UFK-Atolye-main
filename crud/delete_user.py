import json
import os

def delete_user_from_json(id: str):
    try:
        with open("./user.json", "r", encoding="utf-8") as file:
            users = json.load(file)
        
        user_index = None
        user_to_delete = None
        
        for i, user in enumerate(users):
            if user.get("id") == id:
                user_index = i
                user_to_delete = user
                break
        
        if user_index is None:
            return {"success": False, "message": f"User with ID '{id}' not found."}
        
        deleted_user = users.pop(user_index)
        
        with open("./user.json", "w", encoding="utf-8") as file:
            json.dump(users, file, indent=2, ensure_ascii=False)
        
        return {"success": True, "message": f"User with ID '{id}' successfully deleted.", "deleted_user": deleted_user}
    
    except FileNotFoundError:
        return {"success": False, "message": "user.json file not found."}
    except json.JSONDecodeError:
        return {"success": False, "message": "user.json contains invalid JSON."}
    except Exception as e:
        return {"success": False, "message": f"Error while deleting user: {str(e)}"}

