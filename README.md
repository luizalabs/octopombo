# Octopombo

Slack Bot para listagem de PR's em aberto nos repositórios cadastrados.

## Instalação

1. Criar um virtualenv:

        virtualenv fry -p python3
        
2. Instalar dependências do Python, via `pip`:

        pip install -r requirements.txt

## Deploy

Os deploys de `staging` e `production` são feitos através da [Teresa](https://github.com/luizalabs/teresa-api).

Variáveis de ambiente:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
DISABLE_COLLECTSTATIC
DJANGO_SETTINGS_MODULE
GITHUB_TOKEN
SLACK_CLIENT_ID
SLACK_CLIENT_SECRET
SLACK_CLIENT_TOKEN
```
