import glob
import pickle
import music21

def parse_midi(file):
    """ Parse a midi file and return the notes and chords """
    notes = []
    try:
        midi = music21.converter.parse(file)
        parts = music21.instrument.partitionByInstrument(midi)
        if parts:  # If parts are available
            notes_to_parse = parts.parts[0].recurse()
        else:
            notes_to_parse = midi.flat.notes
        for element in notes_to_parse:
            if isinstance(element, music21.note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, music21.chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))
    except Exception as e:
        print(f"Error parsing {file}: {e}")
    return notes

def process_midi_files(data_folder):
    """ Process all MIDI files and save extracted notes """
    notes = []
    midi_files = glob.glob(f"{data_folder}/*.mid")

    for file in midi_files:
        print(f"Processing file: {file}")
        notes.extend(parse_midi(file))
    
    with open('data/notes.pkl', 'wb') as filepath:
        pickle.dump(notes, filepath)
    
    print(f"Extracted notes from {len(midi_files)} files.")
    
if __name__ == "__main__":
    data_folder = 'data'
    process_midi_files(data_folder)
111