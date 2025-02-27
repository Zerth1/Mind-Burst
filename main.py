import random
import time
import keyboard
import pyttsx3
from mpmath import mp

TEXT_SPEED = 1.0 # Multiplier of TTS speed
DIGIT_SEQUENCE = 20 # Length of sequence to memorize and recite in order
CHUNK_LENGTH = 5 # Self-Explanatory
audio_engine = pyttsx3.init()
audio_engine.setProperty('volume', 1.0)
audio_engine.setProperty("rate", audio_engine.getProperty("rate") * TEXT_SPEED)

mp.dps = DIGIT_SEQUENCE + 10
def generate_sequence():
    return str(mp.pi * random.randint(1, 1000000)).split(".")[1][:DIGIT_SEQUENCE]
current_chunk_start = 0
current_chunk_end = CHUNK_LENGTH - 1
def reset_game():
    global current_chunk_start
    global current_chunk_end
    current_chunk_start = 0
    current_chunk_end = CHUNK_LENGTH - 1
def recite_sequence(sequence: str):
    sequence_slice = " ".join(sequence[current_chunk_start: current_chunk_end + 1])
    audio_engine.say(sequence_slice)
    audio_engine.runAndWait()
while True:
    indexed_sequence = generate_sequence()
    print(indexed_sequence)
    while True:
        pressed_input = keyboard.read_key()
        if pressed_input == "space":
            recite_sequence(indexed_sequence)
        elif pressed_input == "a":
            if current_chunk_start > CHUNK_LENGTH - 1:
                current_chunk_start -= CHUNK_LENGTH
                current_chunk_end -= CHUNK_LENGTH
        elif pressed_input == "l":
            if current_chunk_end < DIGIT_SEQUENCE - CHUNK_LENGTH: 
                current_chunk_start += CHUNK_LENGTH
                current_chunk_end += CHUNK_LENGTH
            else:
                break
        time.sleep(0.5)
    reset_game()
    time.sleep(0.5)
