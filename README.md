# Octopombo

Slack Bot para listagem de PR's em aberto nos repositórios cadastrados.

## Comandos

### Adicionar um novo repositório
```
@octopombo add-repo nome-do-repo numero-de-approves
```

### Remover um repositório
```
@octopombo remove-repo nome-do-repo
```

### Mostrar os PR's em aberto
```
@octopombo show-prs
```
### Mostrar todos os comandos suportados no momento.
```
@octopombo help
```


### Dev

Environment variable:

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
GITHUB_TOKEN
SLACK_TOKEN
OWNER
```

### Install Dependencies

```
 glide install
 glide up
```

### Build
```
 go build .
```
