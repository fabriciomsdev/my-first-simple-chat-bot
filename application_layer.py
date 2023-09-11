import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class TerminalApplicationLayer:
    def setup(self):
        pass
    
    def on_message(self, callback):
        self._on_message_callback = callback

    def listen(self):
        while (True):
            entrada = input().lower()

            if (entrada):
                self._on_message_callback(entrada)

    def send(self, message):
        print(message)


class WhatsappApplicationLayer:
    ultima_mensagem_lida = None

    def setup(self):
        self.driver = webdriver.Chrome()
        print("Acessando o WhatsApp Web...")
        self.driver.get('https://web.whatsapp.com/')
        self.driver.maximize_window()
        print("Escaneie o QR Code, e então pressione ENTER")
        input()


    def on_message(self, callback):
        self._on_message_callback = callback


    def listen(self):
        while True:
            print( "Buscando novas mensagens..")
            time.sleep(5)

            try:
                # Todos contatos que estão sinalizados com novas mensagens tem o atributo aria-label
                # Aqui buscamos todos eles
                contatos = self.driver.find_elements(By.CSS_SELECTOR, "span[aria-label]")
                # Percorre contatos com novas mensagens
                for contato in contatos:
                    # Clica no contato para que possamos acessar o campo de mensagem
                    contato.click()
                    # Obtém caixa de texto para enviarmos a mensagem
                    # Como o campo de busca e de mensagem tem as mesmas classes
                    seletor = '#main .message-in .selectable-text.copyable-text'
                    ultima_mensagem = self.driver.find_elements(By.CSS_SELECTOR, seletor)[-1]

                    # Verifica se a mensagem é diferente da última mensagem lida
                    if (ultima_mensagem.text != self.ultima_mensagem_lida):
                        self.ultima_mensagem_lida = ultima_mensagem.text
                        self._on_message_callback(str(ultima_mensagem.text).lower())

            except Exception as e:
                print(e)


    def send(self, message):
        # Obtemos apenas o segundo elemento encontrado - por isso o [1]
        campoMensagem = self.driver.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']")[1]
        # Clica no campo de mensagem
        campoMensagem.click()
        time.sleep(5)
        # Obtém mensagem aleatória e envia para o campo
        campoMensagem.send_keys(message)
        time.sleep(5)
        # Pressiona a tecla ENTER para enviar a mensagem
        campoMensagem.send_keys(Keys.ENTER)

