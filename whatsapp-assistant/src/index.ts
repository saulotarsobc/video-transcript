import { Client, LocalAuth, Message, MessageTypes } from "whatsapp-web.js";
import { PrismaClient } from "@prisma/client";
import qrcode from "qrcode-terminal";
import ollama from "ollama";

// Inicialização do cliente do WhatsApp
const client = new Client({
  authStrategy: new LocalAuth({
    dataPath: "./zapzap",
    clientId: "zap-1",
  }),
  puppeteer: {
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
    headless: true,
  },
});

client.initialize();

/* ---------- Eventos do Cliente ---------- */

client.once("ready", () => console.log("Client is ready!"));

client.on("qr", (qr) => qrcode.generate(qr, { small: true }));

client.on("authenticated", () => console.log("Client authenticated!"));

client.on("disconnected", (reason) =>
  console.log("Client disconnected!", reason)
);

client.on("error", (error) => console.log("Client error!", error));

client.on("change_state", (state) =>
  console.log("Client state changed!", state)
);

client.on("remote_session_saved", () => console.log("Session saved"));

/* ---------- Funções Auxiliares ---------- */

// Enviar mensagem
const enviarMensagem = ({ to, message }: { to: string; message: string }) => {
  console.log(">>> Enviando mensagem:", { to, message });
  client
    .sendMessage(to, message)
    .then(() => console.log(`Mensagem enviada: `, { to, message }))
    .catch((error) =>
      console.log("Erro ao enviar mensagem:", { to, message }, error)
    );
};

// Gerenciar mensagem recebida
client.on("message", async (msg: Message) => {
  const chat = await msg.getChat();

  if (chat.isGroup) {
    console.log("Mensagem de grupo:", msg.from, msg.body);
    return;
  }

  if (msg.from === "status@broadcast") {
    console.log("Mensagem de status:", msg.from, msg.body);
    return;
  }

  switch (msg.type) {
    case MessageTypes.LOCATION:
      msg.reply("O formato de localização ainda não foi implementado");
      break;

    case MessageTypes.AUDIO:
    case MessageTypes.VOICE:
      msg.reply("O formato de áudio ainda não foi implementado");
      break;

    case MessageTypes.DOCUMENT:
      msg.reply("O formato de documento ainda não foi implementado");
      break;

    case MessageTypes.IMAGE:
      ollamaImagem(msg);
      break;

    case MessageTypes.TEXT:
      if (msg.body) {
        console.log(msg.body);
        chat.sendStateTyping();
        await ollamaChat(msg);
      }
      break;

    default:
      console.log("Tipo de mensagem não suportado:", msg.type);
  }
});

/* ---------- Funções de Actions ---------- */

// Função para identificar a action solicitada pelo usuário e executá-la
const processarAction = async (action: string, msg: Message) => {
  switch (action) {
    case "consultarBanco":
      const dados = await consultarBanco(msg.from);
      enviarMensagem({ to: msg.from, message: `Dados encontrados: ${dados}` });
      break;

    case "enviarSaudacao":
      enviarMensagem({
        to: msg.from,
        message: "Olá! Como posso ajudar você hoje?",
      });
      break;

    default:
      enviarMensagem({ to: msg.from, message: "Ação não reconhecida." });
  }
};

// Função para consultar banco de dados (exemplo)
const consultarBanco = async (userId: string) => {
  const historico = await historicoCompleto({ userId });
  return historico.map((item) => item.message).join(", ");
};

/* ---------- Funções Ollama ---------- */

const ollamaChat = async (msg: Message) => {
  console.log(">>> Mensagem em Ollama");

  await adicionarAoHistorico({
    userId: msg.from,
    message: msg.body,
    role: "user",
  });

  const historico = await historicoCompleto({ userId: msg.from });

  const messages = [
    {
      role: "system",
      content:
        "Você está no controle do WhatsApp do Saulo Costa, um desenvolvedor web. Ao interagir com o usuário, identifique se a solicitação corresponde a uma ação específica. Se o usuário pedir para ver o histórico, dados, ou mensagens anteriores, responda apenas com 'action: consultarBanco'. Para saudações como 'Oi', responda com 'action: enviarSaudacao'. Em todos os outros casos, responda com uma mensagem adequada sem ações.",
    },
    ...historico.map((m) => ({ role: m.role, content: m.message })),
  ];

  try {
    const response = await ollama.chat({
      model: "llama3.2",
      messages,
    });

    console.log(">>> Resposta completa do Ollama:", response.message.content);

    // Verifica se a resposta contém uma action
    const actionRegex = /action:\s*(\w+)/;
    const match = response.message.content.match(actionRegex);

    if (match) {
      const action = match[1];
      await processarAction(action, msg);
    } else {
      // Caso não tenha action, envia a resposta normal
      await adicionarAoHistorico({
        userId: msg.from,
        message: response.message.content,
        role: "assistant",
      });

      enviarMensagem({ to: msg.from, message: response.message.content });
    }
  } catch (error) {
    console.log("Erro no Ollama:", error);
  }
};

const ollamaImagem = async (msg: Message) => {
  console.log("Mensagem de imagem:", msg.from, msg.body);

  const media = await msg.downloadMedia();

  const response = await ollama
    .chat({
      model: "llava-llama3",
      messages: [
        {
          role: "system",
          content: "Descreva as imagens em português",
        },
        {
          role: "user",
          content: msg.body ?? "Descreva essa imagem em português",
          images: [media.data],
        },
      ],
    })
    .then((response) => {
      console.log(">>> Resposta do Ollama:", response.message.content);
      return response;
    })
    .catch((error) => {
      console.log("Erro no Ollama:", error);
      return;
    });

  if (response) {
    // adicionar prompt ao histórico
    await adicionarAoHistorico({
      userId: msg.from,
      message: msg.body ?? "Descreva essa imagem em português",
      role: "user",
    });

    // adicionar descrição ao histórico
    await adicionarAoHistorico({
      userId: msg.from,
      message: "O usuário enviou uma imagem: " + response.message.content,
      role: "assistant",
    });

    // enviar resposta para o usuário
    msg.reply(response.message.content);
  }
};

/* ---------- Funções Prisma ---------- */

const prisma = new PrismaClient();

const adicionarAoHistorico = async ({
  userId,
  message,
  role,
}: {
  userId: string;
  message: string;
  role: string;
}) => {
  console.log(">>> Adicionando ao histórico:", { userId, role, message });
  await prisma.message.create({
    data: { userId, message, role },
  });
};

const historicoCompleto = async ({ userId }: { userId: string }) => {
  return await prisma.message.findMany({
    where: { userId },
    orderBy: { createdAt: "asc" },
  });
};
