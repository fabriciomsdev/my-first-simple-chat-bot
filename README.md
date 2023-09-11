### PUCPR - Agentes conversacionais - Chat bot com python:

#### Objetivo:
    Este agente conversacional fechado, auxilia o cliente a pedir uma entrega de um pacote online usando um dos projetos que participo:
    https://any.stone.com.br

#### Em funcionamento
    ![alt text](./evidence.png)
    OBS: existe um arquivo chamado test.txt onde há um dialogo de testes

### Para rodar:
```sh
    python3 -m venv venv &&
    . ./venv/bin/activate &&
    pip install -r requirements.txt
```

#### Arquitetura:
    <img src="./architecture.jpg" width="100%" />

##### Componentes importantes e suas reponsabilidades:
    TerminalApplicationLayer: Responsável por fazer interface com o terminal para rodar a aplicação quando está no model terminal

    WhatsappApplicationLayer: Responsável por fazer interface com o terminal para rodar a aplicação quando está no model whatsapp

    ChatBot: Classe responsável pelo start e injeção de dependencia em toda a aplicação

    LanguageUnderstandingModel: Modelo de NLP básico criado na nltk

    ActionsManager: Gerenciador de ações do usuário na plataforma

    DialogManager: Controlador de devoluções de dialogos

    FlowOrchestrator: Controlador do fluxo para garantir que o usuário sempre que cair no fluxo de exceção vai voltar ao normal

    AppConfig: Configuração da aplicação

#### Técnicas utilizadas:
    - Named Entity Recognition (NER)
    - Patternmatching
    - Intents

#### Observações:
    1 - Optei por fazer algumas na mão sem utilizar plataformas prontas, justamente para aprender mais sobre o tema.
    2 - O modelo N.E.R. se encontra no ActionsManager para interpretação de medidas
    3 - No LanguageUnderstandingModel se encontra as configurações dos modelo
