import sys
import wave
import struct
import math
import json

def analizar(audio_path):
    with wave.open(audio_path, 'rb') as wav:
        framerate = wav.getframerate()
        n_frames = wav.getnframes()
        sampwidth = wav.getsampwidth()
        
        chunk_frames = int(framerate * 0.2)
        amplitudes = []
        timestamps = []
        
        for i in range(0, n_frames, chunk_frames):
            frames = wav.readframes(chunk_frames)
            if not frames: break
            
            count = len(frames) // sampwidth
            if sampwidth == 2:
                samples = struct.unpack(f"<{count}h", frames)
                rms = math.sqrt(sum(s**2 for s in samples) / len(samples)) if samples else 0
                amplitudes.append(rms)
                timestamps.append(i / float(framerate))

        if not amplitudes: return []
        
        max_amp = max(amplitudes) or 1
        umbral = max_amp * 0.65
        
        puntos = []
        ultimo = -5
        for amp, t in zip(amplitudes, timestamps):
            if amp >= umbral and (t - ultimo) >= 5:
                puntos.append({
                    "segundos": round(t, 2),
                    "timestamp": f"{int(t//60):02d}:{int(t%60):02d}",
                    "porcentaje": round((amp/max_amp)*100)
                })
                ultimo = t
        return puntos

if __name__ == "__main__":
    if len(sys.argv) > 1:
        res = analizar(sys.argv[1])
        print(json.dumps(res))
