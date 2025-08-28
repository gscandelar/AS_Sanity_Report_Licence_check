# AS License Check

Projeto em Python para verificar se artigos possuem licença assinada ou não, consultando a API interna do Wiley Admin.

## Objetivo

O script lê uma lista de IDs de artigos, acessa a API do Wiley Admin e verifica se a licença de cada artigo está assinada. O resultado é salvo em um CSV para análise.

## Arquivos do projeto

- **main.py**: Script principal que realiza a verificação de licenças.  
- **cookies.txt**: Arquivo que deve conter os cookies de autenticação necessários para acessar a API. Deve ser preenchido com:
```
WPP\_AUTH\_TOKEN=...
almSessionId=...
```
Substitua `...` pelos valores reais obtidos no Wiley Admin. Estes valores expiram periodicamente e precisam ser atualizados.  

- **input/article_list.csv**: Arquivo CSV que deve conter os IDs dos artigos a serem verificados, um ID por linha.  
Exemplo:

```csv
100288049,
100287683,
100288157
```
- **output/results.csv**: Arquivo gerado pelo script contendo o resultado da verificação. Cada linha terá o ID do artigo e o status da licença (`SIGNED`, `NOT SIGNED` ou `ERROR`).

## Como usar

1. Preencha o arquivo `cookies.txt` com os valores corretos.  
2. Adicione os IDs de artigos no `input/article_list.csv`.  
3. Execute o script:

```bash
python main.py
```
4. Confira o arquivo `output/results.csv` para os resultados.


