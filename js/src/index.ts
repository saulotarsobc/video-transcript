import ffmpegStatic from "ffmpeg-static";
import ffmpeg from "fluent-ffmpeg";
import { join } from "node:path";
import { pipeline, env } from "@xenova/transformers";
import fs from "node:fs";

env.allowLocalModels = true;

const video = join(__dirname, "..", "videos", "e.mp4");
const audio = join(__dirname, "..", "audio.aifc");

export const convertToAudio = () =>
  new Promise((resolve, reject) => {
    ffmpeg.setFfmpegPath(String(ffmpegStatic));

    ffmpeg()
      .input(video)
      // .addOutputOptions(["-ab", "20k", "-f", "mp4"])
      .output(audio)
      .on("end", () => {
        resolve(true);
      })
      .on("error", (err: Error) => {
        reject(err);
      })
      .on("progress", (progress: any) => {
        console.log(
          "convertToAudio [PERCENT] >",
          Math.floor(progress.percent) + "% done"
        );
      })
      .run();
  });

export const convertToText = () =>
  new Promise(async (resolve, reject) => {
    const transcriber = await pipeline("automatic-speech-recognition", "", {
      cache_dir: join(__dirname, "..", ".cache"),
      quantized: true,
    });

    const audioBuffer = fs.readFileSync(audio);
    const audioData = new Float32Array(
      audioBuffer.buffer,
      audioBuffer.byteOffset,
      audioBuffer.byteLength / Float32Array.BYTES_PER_ELEMENT
    );

    const data = await transcriber(audioData, {
      // language: "portuguese",
      task: "transcribe",
      chunk_length_s: 30,
      stride_length_s: 5,
    }).catch((err: Error) => reject(err));

    resolve(data);
  });

const main = async () => {
  await convertToAudio()
    .then((data) => {
      console.log("convertToAudio [SUCESSO] >", { data, msg: "success" });
    })
    .catch((err) => {
      return console.error(["convertToAudio [ERRO] >"], { err });
    });

  convertToText()
    .then((data: any) => {
      console.log("convertToText [SUCESSO] >");

      console.log(data);
    })
    .catch((err) => {
      return console.error(["convertToText [ERRO] >"], { err });
    });

  // const sentimento = await sentimentAnalysis('Curso: Dominando CSS 3 com SASS. Aula: SCSS - [2024] Sass - CSS com Super-poderes. Mensage: FALTA DE CONTEUDO - FALTA EXPLICAÇÕES E AULAS SOBRE GRID LAYOUT');
  // console.log({ sentimento });
};

main();
