import requests
import json

headers = {
	"X-RapidAPI-Key": "de0a79f57emsh16f2464e9868dccp1b0077jsn3c9b24a0edac",
	"X-RapidAPI-Host": "imdb8.p.rapidapi.com"
}

def get_genres(movie_id):
	url = "https://imdb8.p.rapidapi.com/title/get-genres"
	querystring = {"tconst":movie_id}
	response_ = requests.get(url, headers=headers, params=querystring)
	return response_.json()

print(get_genres('tt0316288'))
# url = "https://imdb8.p.rapidapi.com/auto-complete"

# querystring = {"q":"Aama"}

# response = requests.get(url, headers=headers, params=querystring)

# print(response.json())

# data = json.loads(response.text)

# # Format the json to be more readable this is mostly for viewing raw
# # response data when debugging
# formattedData = json.dumps(data, indent=4)


# # Load the json data into a dictionary
# dataDict = json.loads(formattedData)

# # Save the most important data in our list
# print(dataDict)
