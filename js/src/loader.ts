import dotenv from "dotenv";
dotenv.config();

import path from "node:path";
import { createClient } from "redis";

import { DirectoryLoader } from "langchain/document_loaders/fs/directory";
import { JSONLoader } from "langchain/document_loaders/fs/json";
import { TokenTextSplitter } from "langchain/text_splitter";
import { RedisVectorStore } from "langchain/vectorstores/redis";
import { OpenAIEmbeddings } from "langchain/embeddings/openai";

const loader = new DirectoryLoader(path.resolve(__dirname, "../temp"), {
  ".json": (path) => new JSONLoader(path, "/text"),
});

async function laod() {
  const docs = await loader.load();

  const splitter = new TokenTextSplitter({
    encodingName: "cl100k_base",
    chunkSize: 600,
    chunkOverlap: 0,
  });

  const splitedDocs = await splitter.splitDocuments(docs);

  const redis = createClient({
    url: "redis://localhost:6379",
  });

  redis.connect().then(async () => {
    console.log("Connected to Redis");
  });

  await RedisVectorStore.fromDocuments(
    splitedDocs,
    new OpenAIEmbeddings({ openAIApiKey: process.env.OPENAI_API_KEY }),
    {
      indexName: "videos-embeddings",
      redisClient: redis,
      keyPrefix: "videos",
    }
  );

  await redis.disconnect();
}

laod();
