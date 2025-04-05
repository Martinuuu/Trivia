import requests
import json

def get_categories():
    categories = []
    categories.append((0, "Alle Kategorien"))
    
    response = requests.get("https://opentdb.com/api_category.php")
    if response.status_code == 200:
        data = json.loads(response.content)  
        for item in data["trivia_categories"]:
            categories.append((item["id"], item["name"]))
    else:
        print(f"Fehler beim Abrufen der Kategorien: {response.status_code}")
    
    return categories
