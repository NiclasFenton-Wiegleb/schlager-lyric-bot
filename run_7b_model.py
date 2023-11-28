import requests

API_URL = "https://api-inference.huggingface.co/models/niclasfw/schlager-bot-004"
headers = {"Authorization": "Bearer "}

def query(prompt):
	response = requests.post(API_URL, headers=headers, json=prompt)
	return response.json()

sample = f"""Wer ist der attraktivste Spieler der Bundesliga?/n
Es ist Rosenfelder!\n
Max Rosenfelder/n
Wir wollen mit dem schonsten Mann der Liga feiern gehen!
"""

prompt = f"""### Instruction:
Benuzte den gegebenen Input um ein Schlager Lied zu schreiben.

### Input:
{sample}

### Response:
"""

output = query({
	"inputs": prompt,
})

print(output)