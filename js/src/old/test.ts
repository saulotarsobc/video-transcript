// npm i @xenova/transformers
import { pipeline } from "@xenova/transformers";
import { readFileSync } from "fs";
import { join } from "path";

const audio = join(__dirname, 'jfk.wav');
const audioBuffer = readFileSync(audio);

// Converte o Buffer para Float32Array
const audioData = new Float32Array(
  audioBuffer.buffer,
  audioBuffer.byteOffset,
  audioBuffer.byteLength / Float32Array.BYTES_PER_ELEMENT
);

// Cria o pipeline de transcrição
async function main() {
  const transcriber = await pipeline("automatic-speech-recognition", "Xenova/whisper-tiny.en");

  // Faz a transcrição utilizando o Float32Array
  const data = await transcriber(audioData, { return_timestamps: true });

  console.log(JSON.stringify(data, null, 2));
}

main();
