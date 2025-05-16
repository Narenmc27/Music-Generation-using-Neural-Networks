# src/lstm_model.py
import pickle
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Activation
from tensorflow.keras.utils import to_categorical  # Updated import

# Load notes
with open('data/notes.pkl', 'rb') as filepath:
    notes = pickle.load(filepath)

# Prepare input sequences
sequence_length = 100
pitchnames = sorted(set(notes))
n_vocab = len(set(notes))
note_to_int = {note: number for number, note in enumerate(pitchnames)}

# Prepare data for training
network_input = []
network_output = []

for i in range(0, len(notes) - sequence_length):
    sequence_in = notes[i:i + sequence_length]
    sequence_out = notes[i + sequence_length]
    network_input.append([note_to_int[char] for char in sequence_in])
    network_output.append(note_to_int[sequence_out])

n_patterns = len(network_input)

network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
network_input = network_input / float(n_vocab)
network_output = to_categorical(network_output)  # Updated to_categorical

# Define LSTM model
model = Sequential()
model.add(LSTM(512, input_shape=(network_input.shape[1], network_input.shape[2]), return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(512, return_sequences=False))
model.add(Dropout(0.3))
model.add(Dense(256))
model.add(Activation('relu'))
model.add(Dropout(0.3))
model.add(Dense(n_vocab))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

# Train the model
model.fit(network_input, network_output, epochs=7, batch_size=64)
model.save('music_model.h5')
