// src/prisma/index.ts
import { PrismaClient } from "@prisma/client";

class PrismaService {
  private static instance: PrismaClient;

  private constructor() {}

  public static getInstance(): PrismaClient {
    if (!PrismaService.instance) {
      PrismaService.instance = new PrismaClient();
    }
    return PrismaService.instance;
  }

  public static async connect(): Promise<void> {
    const prisma = PrismaService.getInstance();
    await prisma.$connect();
    console.log("Prisma connected successfully");
  }
}

// Inicia a conexão ao carregar o módulo
PrismaService.connect().catch((err) => {
  console.error("Failed to connect Prisma:", err);
  process.exit(1);
});

export default PrismaService.getInstance();
