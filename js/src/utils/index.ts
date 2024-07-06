import { pipeline } from "@xenova/transformers";

export async function sentimentAnalysis(text: string) {
    return new Promise(async (resolve, reject) => {
        // const pipe = await pipeline('sentiment-analysis', 'Xenova/bert-base-multilingual-uncased-sentiment');
        const pipe = await pipeline('sentiment-analysis', 'Xenova/distilbert-base-uncased-finetuned-sst-2-english');

        pipe(text)
            .then((data: any) => resolve(data))
            .catch((err: Error) => reject(err));
    });
}