import pprint
import re
from answer_generator import AskDeliveryAction

from config import AppConfig
from dtos import UserInputUnderstandingDTO

import re
import nltk
from nltk.corpus import wordnet

class LanguageUnderstandingModel:
    def setup(self):
        # Precisa efetuar o download do wordnet
        nltk.download('wordnet')
        # Caso use o Open Multilingual Wordnet
        nltk.download('omw')
        nltk.download('omw-1.4')

        palavras=[
            'olá',
            'entrega',
            'pacote',
            'largura',
            'altura',
            'comprimento',
            'peso',
            'destino',
            'coleta',
            'produto',
            'venda',
            'colete',
            'pegue',
            'pegar',
            'entregar',
            'coletar',
            'confirmar',
            'confirmo',
            'confirmado',
            'confirmada',
            'confirmados',
            'confirmadas',
            'ver',
            'cotações',
            'pesa'
        ]
        # Dicionários de sinônimos
        lista_sinonimos={}

        # Percorre a lista de palavras
        for palavra in palavras:
            sinonimos=[]
            # Busca sinônimos da palavra no wordnet em pt-br
            for syn in wordnet.synsets(palavra, lang="por"):
                # Busca formas léxicas da palavra
                for lem in syn.lemmas(lang="por"):
                # Adiciona forma na lista
                    sinonimos.append(lem.name())

            # Remove palavras duplicadas e adiciona ao dicionário
            lista_sinonimos[palavra]=set(sinonimos)

        lista_sinonimos['peso'] = lista_sinonimos['peso'] | lista_sinonimos['pesa']

        lista_sinonimos['pacote'] = lista_sinonimos['pacote'] | {'encomenda', 'envelope', 'caixa', 'pacotinho'}
        lista_sinonimos['pacote'] = lista_sinonimos['pacote'] | lista_sinonimos['venda'] | lista_sinonimos['produto']

        lista_sinonimos['largura'] = lista_sinonimos['largura'] | {'largura da caixa', 'largura do pacote', 'largura do envelope', 'largura do produto'}
        lista_sinonimos['altura'] = lista_sinonimos['altura'] | {'altura da caixa', 'altura do pacote', 'altura do envelope', 'altura do produto'}
        lista_sinonimos['comprimento'] = lista_sinonimos['comprimento'] | {'comprimento da caixa', 'comprimento do pacote', 'comprimento do envelope', 'comprimento do produto'}

        tipos_aleatorios_de_entregas = []

        lista_sinonimos['entrega'] = lista_sinonimos['entrega'] | {'enviar', 'despacho', 'remessa', 'transporte', 'fazer entrega', 'fazer entrega de', 'delivery', 'entregar meu produto'}

        for sinonimo_pacote in lista_sinonimos['pacote']:
            for sinonimo_entrega in lista_sinonimos['entrega']:
                tipos_aleatorios_de_entregas.append(sinonimo_entrega + ' ' + sinonimo_pacote)

        lista_sinonimos['entrega'] = lista_sinonimos['entrega'] | set(tipos_aleatorios_de_entregas)

        lista_sinonimos['entregar'] = lista_sinonimos['entregar'] | {'entregar na', 'entregar no', 'entregar em', 'entregar para', 'entregar ao', 'entregar a', 'entregar'}

        lista_sinonimos['confirmar'] = [
            'confirmo',
            'confirmado',
            'confirmada',
            'confirmados',
            'confirmadas',
        ]

        # Dicionário de palavras-chave e intenções
        keywords={}
        keywords_dict={}

        # Criando um novo registro de intenção para saudações
        keywords[AskDeliveryAction.greeting] = []
        keywords[AskDeliveryAction.pedir_entrega] = []
        keywords[AskDeliveryAction.definir_endereco_de_coleta] = []
        keywords[AskDeliveryAction.definir_largura_do_pacote] = []
        keywords[AskDeliveryAction.definir_altura_do_pacote] = []
        keywords[AskDeliveryAction.definir_comprimento_do_pacote] = []
        keywords[AskDeliveryAction.definir_peso_do_pacote] = []
        keywords[AskDeliveryAction.definir_endereco_de_entrega] = []
        keywords[AskDeliveryAction.mostrar_opcoes_de_entrega] = []
        keywords[AskDeliveryAction.escolher_opcao_de_entrega] = []
        keywords[AskDeliveryAction.confirm] = []

        # Popula a entrada criada com a lista de sinônimos da palavra-chave "olá", e formata com os metacaracteres do regex
        for sin in list(lista_sinonimos['entrega']):
            keywords[AskDeliveryAction.pedir_entrega].append('.*\\b'+sin+'\\b.*')

        for sin in list(lista_sinonimos['coletar']):
            keywords[AskDeliveryAction.definir_endereco_de_coleta].append('.*\\b'+sin+'\\b.*')

        for sin in list(lista_sinonimos['largura']):
            keywords[AskDeliveryAction.definir_largura_do_pacote].append('.*\\b'+sin+'\\b.*')

        for sin in list(lista_sinonimos['altura']):
            keywords[AskDeliveryAction.definir_altura_do_pacote].append('.*\\b'+sin+'\\b.*')

        for sin in list(lista_sinonimos['comprimento']):
            keywords[AskDeliveryAction.definir_comprimento_do_pacote].append('.*\\b'+sin+'\\b.*')

        for sin in list(lista_sinonimos['peso']):
            keywords[AskDeliveryAction.definir_peso_do_pacote].append('.*\\b'+sin+'\\b.*')

        for sin in list(lista_sinonimos['entregar']):
            keywords[AskDeliveryAction.definir_endereco_de_entrega].append('.*\\b'+sin+'\\b.*')

        for sin in list(lista_sinonimos['olá']):
            keywords[AskDeliveryAction.greeting].append('.*\\b'+sin+'\\b.*')

        for sin in ['está correto', 'está certo', 'o endereço está certo', 'sim, está correto', 'meu enredeço está correto']:
            keywords[AskDeliveryAction.mostrar_opcoes_de_entrega].append('.*\\b'+sin+'\\b.*')

        for sin in ['escolho', 'a cotação', 'a opção', 'a opção de entrega', 'a opção de entrega númer']:
            keywords[AskDeliveryAction.escolher_opcao_de_entrega].append('.*\\b'+sin+'\\b.*')

        for sin in list(lista_sinonimos['confirmar']):
            keywords[AskDeliveryAction.confirm].append('.*\\b'+sin+'\\b.*')

        for intent, keys in keywords.items():
        # Une todas palavras-chave sinônimas com o operador OU
            keywords_dict[intent]=re.compile('|'.join(keys))

        self.set_intent_db(keywords_dict)

    def set_intent_db(self, intent_db):
        self.intent_db = intent_db
        print(self.intent_db)

    def undestand(self, message: str):
        matched_intent = None

        for intent,pattern in self.intent_db.items():
            # Busca as palavras-chave na entrada do usuário utilizando regex
            if re.search(pattern, message):

                # Se encontrou, guarda o nome da intenção correspondente
                matched_intent=intent

        # Por padrão, definimos a intenção padrão
        return UserInputUnderstandingDTO(
            message=message,
            intent= matched_intent if matched_intent else AppConfig.default_intent
        )