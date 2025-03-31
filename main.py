import pygame
import sounddevice as sd
import numpy as np
import os
import sys
import tkinter as tk
from tkinter import messagebox


# Функция для получения правильного пути к ресурсам (например, папке с звуками)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


# Получение списка звуковых файлов в папке "sounds"
def get_sound_files_from_folder(folder_path):
    return [file for file in os.listdir(folder_path) if file.endswith(".mp3")]


# Функция для воспроизведения MP3 через выбранное устройство
def play_sound(mp3_file):
    pygame.mixer.init(frequency=44100, size=-16, channels=1)
    pygame.mixer.music.load(mp3_file)
    pygame.mixer.music.play()


def toggle_pause():
    if pygame.mixer.music.get_busy():
        if pygame.mixer.music.get_pos() > 0:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()


# Получение доступных устройств для ввода
def list_input_devices():
    return [(i, dev['name']) for i, dev in enumerate(sd.query_devices()) if dev['max_input_channels'] > 0]


# Основная часть программы с GUI
def create_interface():
    sounds_folder = resource_path("sounds")
    sound_files = get_sound_files_from_folder(sounds_folder)
    input_devices = list_input_devices()

    root = tk.Tk()
    root.title("Sound Pad")

    def on_sound_select(event):
        sound_index = sound_listbox.curselection()[0]
        selected_sound.set(sound_files[sound_index])

    def on_mic_select(event):
        mic_index = mic_listbox.curselection()[0]
        selected_mic.set(input_devices[mic_index][1])

    def on_play_button_click():
        selected_sound_file = os.path.join(sounds_folder, selected_sound.get())
        play_sound(selected_sound_file)

    sound_label = tk.Label(root, text="Выберите звук:")
    sound_label.pack(pady=5)

    sound_listbox = tk.Listbox(root)
    for sound in sound_files:
        sound_listbox.insert(tk.END, sound)
    sound_listbox.pack(pady=5)
    sound_listbox.bind("<<ListboxSelect>>", on_sound_select)

    selected_sound = tk.StringVar()
    selected_sound.set(sound_files[0] if sound_files else "")

    mic_label = tk.Label(root, text="Выберите микрофон:")
    mic_label.pack(pady=5)

    mic_listbox = tk.Listbox(root)
    for i, name in input_devices:
        mic_listbox.insert(tk.END, name)
    mic_listbox.pack(pady=5)
    mic_listbox.bind("<<ListboxSelect>>", on_mic_select)

    selected_mic = tk.StringVar()
    selected_mic.set(input_devices[0][1] if input_devices else "")

    play_button = tk.Button(root, text="Воспроизвести звук", command=on_play_button_click)
    play_button.pack(pady=10)

    pause_button = tk.Button(root, text="остановить звук", command=toggle_pause)
    pause_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_interface()
