// src/index.ts
import dotenv from "dotenv";
dotenv.config();

import { Client, LocalAuth, Message } from "whatsapp-web.js";
import { PrismaClient } from "@prisma/client";
import qrcode from "qrcode-terminal";
import ollama from "ollama";

const client = new Client({
  authStrategy: new LocalAuth({
    dataPath: "./data/zapzap",
    clientId: "zap-1",
  }),
});

client.once("ready", () => {
  console.log("Client is ready!");
});

client.on("qr", (qr) => {
  qrcode.generate(qr, { small: true });
});

client.on("authenticated", () => {
  console.log("Client authenticated!");
});

client.on("disconnected", (reason) => {
  console.log("Client disconnected!", reason);
});

client.on("error", (error) => {
  console.log("Client error!", error);
});

client.on("change_state", (state) => {
  console.log("Client state changed!", state);
});

const enviarMensagem = ({ to, message }) => {
  console.log(">>> Enviando mensagem:", to, message);
  client
    .sendMessage(to, message)
    .then((message) => {
      console.log("Mensagem enviada:", message);
    })
    .catch((error) => {
      console.log("Erro ao enviar mensagem:", error);
    });
};

client.on("message", async (msg: Message) => {
  if (msg.type == "chat") {
    console.log(msg.body);
    ollamaChat(msg);
  }
});

client.initialize();

/* ollama */
async function ollamaChat(msg: Message) {
  console.log(">>> Mesagem em Ollama");

  await adicionarAoHistorico({
    userId: msg.from,
    message: msg.body,
    role: "user",
  });

  const historico = await historicoCompleto({
    userId: msg.from,
  });

  const messages = historico.map((m) => ({
    role: m.role,
    content: m.message,
  }));

  ollama
    .chat({
      model: "llama3.1",
      messages,
    })
    .then(async (response) => {
      console.log(">>> Resposta do Ollama:", response.message.content);

      await adicionarAoHistorico({
        userId: msg.from,
        message: response.message.content,
        role: "assistant",
      });

      enviarMensagem({ to: msg.from, message: response.message.content });
    })
    .catch((error) => {
      console.log("Erro no Ollama:", error);
    });
}

/* prisma */
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
  console.log(">>> Adicionando ao historico:", { userId, role, message });
  await prisma.message.create({
    data: {
      userId,
      message,
      role,
    },
  });
};

const historicoCompleto = async ({ userId }: { userId: string }) => {
  const historico = await prisma.message.findMany({
    where: {
      userId,
    },
    orderBy: {
      createdAt: "asc",
    },
  });
  return historico;
};
