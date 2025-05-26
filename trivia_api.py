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



class Api():
    def __init__(self):
        self.session_token = self.get_session_token()

    def get_session_token(self):
        token = None
        response = requests.get("https://opentdb.com/api_token.php?command=request")
        if response.status_code == 200:
            data = json.loads(response.content)  
            if data["response_code"] == 0:
                token = data["token"]
        else:
            print(f"Fehler beim Abrufen des Tokens: {response.status_code}")
    
        return token
    
    def get_trivia(self, category: int, amount: int):
        url = f"https://opentdb.com/api.php?amount={amount}&type=multiple"
        if category and int(category) != 0:
            url += f"&category={category}"
        url += f"&token={self.session_token}"
        response = requests.get(url)
        questions = []
        if response.status_code == 200:
            data = json.loads(response.content)
            results = data["results"]
            return results
        else:
            print(f"Fehler beim Abrufen der Fragen: {response.status_code}")
        return questions