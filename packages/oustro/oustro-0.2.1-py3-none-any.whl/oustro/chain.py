import requests

def chain(key, ID):
  
  endpoint = 'https://dev.oustro.co/chain'

  r = requests.post(endpoint, json={'key' : key, 'ID' : ID}) 

  return r.text
