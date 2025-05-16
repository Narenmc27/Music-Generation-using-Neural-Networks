import os
import subprocess
from music21 import stream, note, chord, midi

# Define paths
fluidsynth_path = r"Z:\testing\bin\fluidsynth.exe"
soundfont_path = r"Z:\testing\soundfonts\GeneralUser.sf2"
midi_output = r"output/generated_music.mid"
mp3_output = r"output/generated_music.mp3"

# Ensure output directory exists
os.makedirs(os.path.dirname(midi_output), exist_ok=True)

def generate_midi():
    """Creates a simple MIDI file with notes and chords."""
    midi_stream = stream.Stream()

    # Add some notes and a chord
    midi_stream.append(note.Note("C4"))
    midi_stream.append(note.Note("E4"))
    midi_stream.append(note.Note("G4"))
    midi_stream.append(chord.Chord(["C4", "E4", "G4"]))
    
    # Save as MIDI
    midi_stream.write("midi", fp=midi_output)
    print(f"✅ MIDI file saved: {midi_output}")

def convert_to_mp3():
    """Converts the generated MIDI file to MP3 using FluidSynth."""
    if not os.path.exists(soundfont_path):
        raise FileNotFoundError(f"❌ SoundFont file not found: {soundfont_path}")

    try:
        subprocess.run([
            fluidsynth_path, "-ni", soundfont_path, midi_output, "-F", mp3_output, "-r", "44100"
        ], check=True)
        print(f"✅ MIDI converted to MP3: {mp3_output}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running FluidSynth: {e}")

if __name__ == "__main__":
    generate_midi()  # Step 1: Generate MIDI file
    convert_to_mp3()  # Step 2: Convert to MP3
