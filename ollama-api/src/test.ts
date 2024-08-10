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

chat("conte do numero um até o cinco");
