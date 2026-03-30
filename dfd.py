from google import genai

client = genai.Client(api_key="AIzaSyAoqY7uIKY9peK2ZEUrpw0Yb-hw_sL5TTY")

models = client.models.list()

for m in models:
    print(m.name)