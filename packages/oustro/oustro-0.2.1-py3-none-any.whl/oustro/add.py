import requests

def add(trans, key, ID, user):
  
  endpoint = 'https://dev.oustro.co/add'

  r = requests.post(endpoint, json={'key' : key, 'ID' : ID, 'trans' : trans, 'creator' : user}) 

  return r.text
