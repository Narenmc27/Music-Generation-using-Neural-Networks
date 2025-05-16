# Music-Generation-using-Neural-Networks

---

## 🚀 Features

- Parses MIDI files and extracts notes/chords using `music21`
- Trains an LSTM model to learn musical patterns
- Generates original music based on learned sequences
- Saves output as `.mid` and converts it to `.mp3` format

---

## 🛠️ Requirements

- Python 3.7+
- TensorFlow / Keras
- music21
- NumPy
- FluidSynth (for MIDI to MP3 conversion)
- SoundFont (e.g., GeneralUser.sf2)

Install dependencies:
```bash
pip install tensorflow music21 numpy
