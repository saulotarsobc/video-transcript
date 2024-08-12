import dotenv from "dotenv";
import { Client, LocalAuth, Message, MessageTypes } from "whatsapp-web.js";
import { PrismaClient } from "@prisma/client";
import qrcode from "qrcode-terminal";
import ollama from "ollama";

// Configuração do dotenv
dotenv.config();

// Inicialização do cliente do WhatsApp
const client = new Client({
  authStrategy: new LocalAuth({
    dataPath: "./data/zapzap",
    clientId: "zap-1",
  }),
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
      // msg.reply("O formato de imagem ainda não foi implementado");
      console.log("Mensagem de imagem:", msg.from, msg.body);

      const media = await msg.downloadMedia();

      const response = await ollama.chat({
        model: "llava",
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
      });

      msg.reply(response.message.content);

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

/* ---------- Funções Ollama ---------- */

async function ollamaChat(msg: Message) {
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
        "Você está no controle do whatsapp do Saulo Costa, um desenvolvedor web. Seja sempre respeitoso e cordial. Lembre-se de dar respostas de forma clara e concisa.",
    },
    ...historico.map((m) => ({ role: m.role, content: m.message })),
  ];

  try {
    const response = await ollama.chat({
      model: "llama3.1",
      messages,
    });

    console.log(">>> Resposta do Ollama:", response.message.content);

    await adicionarAoHistorico({
      userId: msg.from,
      message: response.message.content,
      role: "assistant",
    });

    enviarMensagem({ to: msg.from, message: response.message.content });
  } catch (error) {
    console.log("Erro no Ollama:", error);
  }
}

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
