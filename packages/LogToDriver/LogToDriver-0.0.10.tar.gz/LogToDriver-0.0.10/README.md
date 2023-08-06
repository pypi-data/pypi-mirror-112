# LogToDriver

Biblioteca responsável por enviar os logs para drives de Logs como ElasticSearch.


# Tabela de variáveis de ambiente
| Nome               | Tipo    | Exemplo                | Descrição      |
|--------------------|---------|------------------------|----------------|
| PUBLISH_TO_ELASTIC | Boolean | True              | Deve logar no Elastic. |
| ELASTICSEARCH_HOST | String  | ```https://<user>:<pws>@<host>:<port>/``` | Host do Elastic.|
| ENVIRONMENT        | String | ```prod``` | Ambiente produção ou dev  |

## Passos iniciais usando PIPENV
- Instalar.
```bash
pipenv install LogToDriver
```

- Pronto para uso importando desta forma.
```python
from LogToDriver.LogToDriver import LogToDriver
```

## Usando RCC da Robocorp

- Seguir os passos para instalação do [RCC](https://github.com/robocorp/rcc#direct-downloads-for-signed-executables-provided-by-robocorp)

- Teste para ver se instalou corretamente.
```bash
rcc
```

- Caso não tenha um projeto Robocorp criado. Executar o comando.
```bash
rcc create name-project
```

- Acessar o projeto.
```bash
cd name-project
```
- Add Library no conda.yaml via comando.
```bash
rcc robot libs -a LogToDriver -p --conda conda.yaml
```
- Adicionar no arquivo conda.yaml de forma manual.
```yaml
channels:
- conda-forge
dependencies:
- python=3.7.5
- pip=20.1
- pip:
  - LogToDriver
```


- Exemplo de importação da library.
```robot
*** Settings ***
Documentation       Projeto teste.
Library             LogToDriver.LogToDriver


*** Keywords ***
Example keyword
    Log Info        Seu log.  traceId=FG434  cnpj=4444444  qualquercampo=valor
    Log Warn        Seu log.  traceId=FG434  cnpj=4444444  qualquercampo=valor
    Log Debug       Seu log.  traceId=FG434  cnpj=4444444  qualquercampo=valor
    Log Error       Seu log.  traceId=FG434  cnpj=4444444  qualquercampo=valor

    Log Error       Seu log.  traceId=None
```

- Executar o comanda para rodar o projeto e instalar dependências.
```bash
rcc run
```