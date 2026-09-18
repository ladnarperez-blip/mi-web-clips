const express = require('express');
const multer = require('multer');
const { exec } = require('child_process');
const fs = require('fs');

const app = express();
const upload = multer({ dest: 'uploads/' });

app.use(express.static('public'));

app.post('/api/analizar', upload.single('video'), (req, res) => {
    if (!req.file) return res.status(400).send('No se subió ningún archivo.');

    const inputPath = req.file.path;
    const audioPath = `uploads/${req.file.filename}.wav`;

    exec(`ffmpeg -i ${inputPath} -ac 1 -ar 16000 ${audioPath}`, (err) => {
        if (err) return res.status(500).json({ error: 'Error procesando audio' });

        exec(`python3 analizar.py ${audioPath}`, (pyErr, stdout) => {
            if (fs.existsSync(audioPath)) fs.unlinkSync(audioPath);
            if (pyErr) return res.status(500).json({ error: 'Error analizando' });

            const resultados = JSON.parse(stdout);
            res.json({ puntos: resultados });
        });
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Servidor activo en puerto ${PORT}`));
