import os


class AppConfig:
    default_intent = 'padrao'
    exit_intent = 'padrao'
    ui_mode = os.environ.get('UI_MODE', 'terminal')