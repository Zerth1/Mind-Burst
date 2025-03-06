import random
import time
import threading
import keyboard
import pyttsx3
from mpmath import mp

TEXT_SPEED = 1.0 # Multiplier of TTS speed
DIGIT_SEQUENCE = 15 # Length of sequence to memorize and recite in order
CHUNK_LENGTH = 5 # Self-Explanatory
PUNISHMENT_SETTINGS = {
    "Enabled": True,
    "Interval": 60.0,
    "NumberOfDigitsSwapped": 10
}
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
    audio_engine.say("generating new sequence")
def recite_sequence(sequence: str):
    sequence_slice = " ".join(sequence[current_chunk_start: current_chunk_end + 1])
    audio_engine.say(sequence_slice)
    audio_engine.runAndWait()
punishment_clock = 0.0
indexed_sequence = ""
def play():
    global indexed_sequence
    global punishment_clock
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
            time.sleep(0.25)
        reset_game()
        punishment_clock = 0.0
        time.sleep(0.25)
main_thread = threading.Thread(target=play)
main_thread.start()
while True:
    time.sleep(0.25)
    print(punishment_clock)
    if PUNISHMENT_SETTINGS["Enabled"]:
        punishment_clock += 0.25
        if punishment_clock > PUNISHMENT_SETTINGS["Interval"]:
            print("PUNISHMENT")
            punishment_clock = 0.0
            selected_terms = list(range(DIGIT_SEQUENCE))
            random.shuffle(selected_terms)
            selected_terms = selected_terms[:PUNISHMENT_SETTINGS["NumberOfDigitsSwapped"]]
            for term in selected_terms:
                temp_list = list(indexed_sequence)
                temp_list[term] = str(random.randint(0, 9))
                indexed_sequence = "".join(temp_list)
