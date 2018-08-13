#Basic import statements
from tkinter import *   ## notice lowercase 't' in tkinter here
import requests
import config as cfg

#Spotify Auth Startup

URL = 'https://accounts.spotify.com/api/token'
grant_type = 'client_credentials'
body_params = {'grant_type' : grant_type}
# sending get request and saving the response as response object
r = requests.post(URL, data=body_params, auth = (cfg.client_id, cfg.client_secret))
# extracting data in json format
data = r.json()
token = data['access_token']


#1/2 Necessay boilerplate
root = Tk()

#Title for Window
root.title("Spotify API Retrieval")
root.geometry('400x400')


listbox = Listbox(root, width=45, height=15)
text = Entry(root, width=25)

def Search():
	#text_contents = text.get()
    if listbox.size() != 0:
        for i in range (listbox.size()):
            if listbox.get(i) == "At this point queries must be spelled perfectly":
                listbox.delete(i)

    searchURL = 'https://api.spotify.com/v1/search'
    #album, artist, playlist, track

    artist = text.get()
    type = 'artist'

    search_params = {
                    'q' : artist,
                    'type' : type,
                    'market' : 'US',
                    'limit' : '1'
                    }

    search=requests.get(searchURL, headers={ 'Authorization': 'Bearer ' + token }, params=search_params )

    searchData = search.json()
    if len(searchData['artists']['items']) != 0:
        #print("This is Search Data")
        #print (searchData)
        searchURI = searchData['artists']['items'][0]['uri']
        searchURI = searchURI[15:]

        country = 'US'

        #ToDo: make URL more dynamic so users can choose what they do with search results
        resultsURL = 'https://api.spotify.com/v1/artists/' + searchURI + '/top-tracks?country=' + country

        results = requests.get(resultsURL, headers = { 'Authorization': 'Bearer ' + token} )

        resultsData = results.json()


        songs = resultsData['tracks']
        titles = list()
        for i in range(0, len(songs)) :
            #titles.append(songs[i]['name'])
            listbox.insert(END, songs[i]['name'])
    else:
        listbox.insert(END, "At this point queries must be spelled perfectly")

def Select():
    selection = listbox.curselection()
    if selection:
        print (listbox.get(listbox.curselection()))

#Creating widgets for Window
button1 = Button(root, text="Search", command = lambda: Search())
button2 = Button(root, text="Select", command = lambda: Select())



text.pack(side="top")
button1.pack(side="top")
button2.pack(side="top")
listbox.pack(side="top")



#2/2 Necessay boilerplate
root.mainloop()
