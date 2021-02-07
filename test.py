import requests

BASE = "http://127.0.0.1:5000/"

data = [{"vowel": "a", "name": "hat", "views":10},
        {"vowel": "e", "name": "hen", "views":5},
        {"vowel": "i", "name": "pig", "views":2} ]

for i in range(len(data)):
    response = requests.put(BASE + "word/" + str(i), data[i])
    print(response.json())     

input()

#response=requests.delete(BASE + "word/0")
#print(response)
#input()

response = requests.get(BASE + "word/2")
print(response.json())

