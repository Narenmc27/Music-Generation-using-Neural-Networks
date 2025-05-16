import numpy as np
import pickle
from tensorflow.keras.models import load_model
import music21
import os

# Ensure output directory exists
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

def generate_music(model_file='music_model.h5', notes_file='data/notes.pkl', output_file='output/generated_music.mid', length=500):
    """ Generate a MIDI file using the trained model """
    
    # Check if notes file exists
    if not os.path.exists(notes_file):
        raise FileNotFoundError(f"❌ Error: {notes_file} not found!")

    # Load note sequences
    with open(notes_file, 'rb') as filepath:
        notes = pickle.load(filepath)

    pitchnames = sorted(set(notes))
    n_vocab = len(pitchnames)
    
    # Create mappings
    note_to_int = {note: number for number, note in enumerate(pitchnames)}
    int_to_note = {number: note for note, number in note_to_int.items()}

    # Load trained model
    model = load_model(model_file)
    model.compile(optimizer='adam', loss='categorical_crossentropy')  # Ensure compilation

    # Generate a random starting sequence
    start = np.random.randint(0, len(notes) - 100)
    pattern = [note_to_int[n] for n in notes[start:start + 100]]

    output_notes = []
    for _ in range(length):
        input_seq = np.array(pattern).reshape(1, 100, 1) / float(n_vocab)  # Ensure correct input shape
        prediction = model.predict(input_seq, verbose=0)
        
        index = np.argmax(prediction)
        result = int_to_note[index]
        output_notes.append(result)

        # Update pattern
        pattern.append(index)
        pattern = pattern[1:]

    # Convert predictions to MIDI format
    midi_stream = music21.stream.Stream()
    for element in output_notes:
        if '.' in element:
            chord_notes = [music21.note.Note(int(n)) for n in element.split('.')]
            midi_stream.append(music21.chord.Chord(chord_notes))
        elif element == 'rest':
            midi_stream.append(music21.note.Rest())
        else:
            midi_stream.append(music21.note.Note(int(element)) if element.isdigit() else music21.note.Note(element))

    # Save generated music
    midi_stream.write('midi', fp=output_file)
    print(f"✅ MIDI file saved: {output_file}")

if __name__ == "__main__":
    generate_music()
