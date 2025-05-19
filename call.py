import requests

base = "http://127.0.0.1:11111"

records = [
    {"description": "monthly rent", "amount": -10},
    {"description": "uber ride", "amount": -5},
    {"description": "food court", "amount": -5},
    {"description": "freelance income", "amount": 50},
    {"description": "tv subscription", "amount": -5.5},
]

def post_to_microservice(endpoint, data):
    url = base + "/" + endpoint
    response = requests.post(url, json = {"records": data})
    return response.json()

print("Summary:")
print(post_to_microservice("summary", records))

print("\nClassify Purpose:")
print(post_to_microservice("classify/purpose", records))

print("\nClassify Duration:")
print(post_to_microservice("classify/duration", records))
