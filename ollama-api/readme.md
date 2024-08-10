# Help

- [Ollama Download](https://ollama.com/download)
- [Ollama Models](https://ollama.com/library)
- [Ollama Github](https://github.com/ollama/ollama)
- [Node Target Mapping](https://github.com/microsoft/TypeScript/wiki/Node-Target-Mapping)
- [Level Up Your Typescript Skills: Adding Ollama To Your Apps!](https://youtu.be/kaK3ye8rczA?list=TLPQMTAwODIwMjRH3DorwNt84Q)

# Sample

````md
saulo@saulo MINGW64 ~/Documentos/Github/video-transcript/ollama-api (master)
$ ollama run llama3.1:latest

> > > oi, tudo bem?
> > > Tudo bem, obrigado! Estou aqui para ajudar. Você está falando português? Quer conversar sobre algo específico ou apenas falar um pouco?

> > > com desenvolver uma api com node e usar vc para responder um chat com stream?
> > > Interessante!

Sim, posso ajudá-lo a desenvolver uma API em Node.js que envia respostas em tempo real através de streams. Aqui vai uma ideia geral sobre  
como você pode fazer isso:

**API em Node.js**

Crie uma API em Node.js utilizando um framework como Express.js ou Koa.js. Vamos utilizar o Express.js aqui.

```javascript
const express = require("express");
const app = express();

// Configuração da aplicação
app.use(express.json());

// Rota para obter respostas em tempo real
app.get("/resposta", (req, res) => {
  const resposta = "Olá, mundo!";

  // Enviar a resposta como stream
  res.writeHead(200, { "Content-Type": "text/event-stream" });
  res.write("data: " + resposta + "\n\n");

  // Fechar o stream após enviar a resposta
  setTimeout(() => {
    res.end();
  }, 1000); // Tempo de vida do stream em milissegundos
});
```
````

Nesse exemplo, a rota `/resposta` envia uma resposta como stream. O `setTimeout` é utilizado para fechar o stream após um tempo.

**Responder ao chat com streams**

Agora, vamos falar sobre como responder ao chat com streams. Você pode utilizar uma biblioteca como Socket.IO ou WebSocket-Node para
criar uma conexão bidirecional entre o cliente e a API.

Com Socket.IO, por exemplo, você pode criar um socket em seu front-end e usar ele para enviar requisições à API. A API, por sua vez, pode  
utilizar as streams para responder às requisições.

```javascript
// Front-end com Socket.IO
const io = require("socket.io-client");
const socket = io.connect("http://sua-api.com");

// Enviar requisição ao servidor
socket.emit("requisição", "Olá, servidor!");

// Receptor de respostas do servidor
socket.on("resposta", (data) => {
  console.log(data); // 'Olá, mundo!'
});
```

E no seu back-end:

```javascript
// API com Socket.IO
const express = require("express");
const app = express();
const server = require("http").createServer(app);
const io = require("socket.io")(server);

// Evento de conexão do cliente
io.on("connection", (socket) => {
  console.log("Cliente conectado!");

  // Evento de requisição do cliente
  socket.on("requisição", () => {
    const resposta = "Olá, mundo!";

    // Enviar a resposta como stream
    io.to(socket.id).emit("resposta", resposta);
  });
});

server.listen(3000, () => {
  console.log("Servidor rodando em http://localhost:3000");
});
```

Essa é uma visão geral sobre como desenvolver uma API que responde a requisições de clientes através de streams. É importante lembrar que  
você precisará configurar as bibliotecas certas e criar o código que corresponda às suas necessidades específicas.

Fale-me se tiver alguma dúvida ou precisar de mais ajuda!

```

```
