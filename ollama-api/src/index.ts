// src\index.ts
import dotenv from "dotenv";
dotenv.config();

import express, { Request, Response } from "express";
import ollama from "ollama";

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

const chat = async (text: string) => {
  const response = await ollama.chat({
    model: "llama3.1",
    messages: [{ role: "user", content: text }],
  });
  return response.message.content;
};

app.post("/chats", async (req: Request, res: Response) => {
  console.log("chats");

  const { message } = req.body;

  const response = await chat(message);

  res.send(response);
});

// Inicia o servidor
app.listen(PORT, () => {
  console.log(`Servidor rodando em http://localhost:${PORT}`);
});
