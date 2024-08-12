import ollama from "ollama";

const chat = async (text: string) => {
  const response = await ollama.generate({
    model: "llama3.1",
    prompt: text,
    stream: true,
  });

  for await (const part of response) {
    process.stdout.write(part.response);

    if (part.done) {
      process.stdout.write(`\n\nstats: ${part.eval_count} evals\n\n`);
    }
  }
};

// chat("conte do numero um até o cinco");

// ollama
//   .embed({
//     input: "caramelo",
//     model: "llama3.1",
//   })
//   .then((response) => console.log(response))
//   .catch((error) => console.log(error));

async function criarModelo() {
  try {
    const response = await ollama.create({
      model: "llama3.1",
    });
    console.log("Modelo criado com sucesso:", response);
  } catch (error) {
    console.error("Erro ao criar o modelo:", error);
  }
}

criarModelo();
