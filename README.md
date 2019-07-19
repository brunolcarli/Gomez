<table align="center"><tr><td align="center" width="9999">

<img src="https://upload.wikimedia.org/wikipedia/en/a/a4/John_Astin_as_Gomez_Addams.jpg" align="center" width="150" alt="Project icon">

# Telegram Bot

[![Generic badge](https://img.shields.io/badge/docs-blue.svg)](https://github.com/brunolcarli/Gomez/wiki)

Bot 4Fun para o Telegram

>I loved her not for the way she danced with my angels, but for the way the sound of her name could silence my demons.

</td></tr></table>

[Gomez](https://en.wikipedia.org/wiki/Gomez_Addams) é um telegram bot utilizado na interação e recreação do nosso grupo
particular no telegram.

# Desenvovedores

Para rodar você precisará inicialmente de um `token`, você terá acesso ao token
solicitando ao BotFather no telegram.

Para utilizar comandos de armazenamento de dados (como o `quote`) o bot acessa
uma API que, para desenvovlimento, precsa ser configurada e levantada. Você poderá
clonar a API [aqui](https://github.com/brunolcarli/Lisa/tree/threepio_chatbot).

Clone este rojeto e crie na raiz um arquivo chamado `.env`, insira nele o token e a url
da API desta forma:

```
TOKEN=djbsajdnasojdhpisaund.du8sa9uidsaudsaidsa
LISA=http://localhost:8000/graphql/
```

Pronto pra rodar :thumbsup:

## Rodando

Prepare uma virtualenv python e instale nela as dependências com:

```
make install
```

Rode o bot com:

```
make run
```