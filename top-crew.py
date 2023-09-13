import requests

url = "https://imdb8.p.rapidapi.com/title/get-top-crew"

querystring = {"tconst":"tt1999819"}

headers = {
	"X-RapidAPI-Key": "de0a79f57emsh16f2464e9868dccp1b0077jsn3c9b24a0edac",
	"X-RapidAPI-Host": "imdb8.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())