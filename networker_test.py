import networker
client=networker.Networker()
client.set_model('google/gemma-3-4b-it:free')
client.set_system_prompt('ты - крутой ассистент')
client.message('привет')
print(client.chat)