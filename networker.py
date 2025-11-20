from openai import OpenAI
from dotenv import load_dotenv
import os
import pyfiglet

class Networker:
    def __init__(self, token=None, api_url=None):
        #плюшка с огромным аски лого
        print(pyfiglet.figlet_format('Networker', font="slant"))
        print('⚠️ Держите Networker рядом с .env, иначе ключа не найдёт!')
        print('ℹ️ Совет: используйте NetworkerSilent для тихой работы без логов в консоль')
        
        if token is None and api_url is None:
            print('🆗 Токен и ссылка не были указаны вручную, возьмём их из env-файла')

            load_dotenv()
            
            self.token=os.getenv('API_TOKEN')
            self.api_url=os.getenv('API_URL')
            
            if self.api_url is None or self.token is None or self.token=='' or self.api_url=='':
                print('бабах!')
                raise TypeError('Инициализация не пошла, так как мы не нашли нужные переменные в env-файле')
        
            if not self.token.startswith('sk-'):
                print("⚠️ Предупреждение: Ключ не похож на корректный ключ для OpenAI-like API")
        else:
            print('🆗 Токен и ссылка были указаны вручную, используем их')
            self.token=token
            self.api_url=api_url
            if not token.startswith('sk-'):
                print("⚠️ Предупреждение: Ключ не похож на корректный ключ для OpenAI-like API")
        print('✅ Скрипт получил данные успешно, инициализация продолжается...')
            
        self.chat=[]
        self.apiClient=OpenAI(base_url=self.api_url,api_key=self.token)
        self.model='' # указывается программой потом
        
        print('✅ Инициализация Networker прошла успешно!')
        
    def set_system_prompt(self, content): #установка системного промпта
        self.chat.insert(0,{"role":"system","content":content})
        print('🥷 Установлен системный промпт')
    
    def snap(self,save_system_prompt=False): #сносит историю чата
        if not save_system_prompt:
            self.chat=[]
            print('🗑️ Чат удалён вместе с системным промптом')
        else:
            pass
    
    def set_model(self,model):
        self.model=model
        print(f'🆗 Установлен ID Модели {model}')
    
    def message(self, content):
        if self.model in ['',' ', 'null']:
            raise ValueError('Отправка сообщения невозможна без выбранной модели')
        
        self.chat.append({"role":"user","content":content})
        completion=self.apiClient.chat.completions.create(
            model=self.model,
            messages=self.chat
        )
        fixed_completion=completion.choices[0].message.content
        self.chat.append({"role":"assistant","content":fixed_completion})
        return fixed_completion
    