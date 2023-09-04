import pandas as pd
import openai
import requests
import json

api_url = 'https://sdw-2023-prd.up.railway.app'
openai.api_key = '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'


df = pd.read_csv('./Clients.csv')
users_ids = df['UserID'].tolist()

def get_clients(id):
    response = requests.get(f'{api_url}/users/{id}')
    return response.json() if response.status_code == 200 else None

def generate_ai_news(user):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Você é um especialista em segurança de dados bancários."
            },
            {
                "role": "user",
                "content": f"De dicas para {user['name']} de como evitar fraudes bancárias(máximo 120 caracteres)"
            }
        ]
    )
    return completion.choices[0].message.content.strip('\"')


users = [user for id in users_ids if (user := get_clients(id)) is not None]

for user in users:
    news = generate_ai_news(user)
    print(news)
    user['news'].append({
      "description": news
    })
