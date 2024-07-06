import { join } from 'node:path';
import { spawn } from 'node:child_process';

const video = join(__dirname, '..', 'video.mp4')
const audio = join(__dirname, '..', 'audio.mp3')

console.log({
    video,
    audio
})


async function convertToMP3() {
    return new Promise((resolve, reject) => {
        const ffmpeg = spawn('ffmpeg', [
            '-i', video,
            '-f', 'mp3',
            '-y',
            audio
        ])

        ffmpeg.on('close', (code) => {
            if (code === 0) {
                resolve(code)
            } else {
                reject(code)
            }
        })
    })
}

async function main() {
    await convertToMP3()
        .then((data) => console.log({ data }))
        .catch((err) => console.log({ err }))

}


main()