import networker
client=networker.Networker()
client.set_model('google/gemma-3-4b-it:free')
print(client.message('Привет!'))