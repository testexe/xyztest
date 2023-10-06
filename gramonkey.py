import tkinter as tk
import openai
from googletrans import Translator
from tkinter import ttk
from ttkthemes import ThemedStyle

# OpenAI API key
api_key = "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"
openai.api_key = api_key

# Initialize the translator
translator = Translator()

def correct_text():
    user_input = input_text.get(1.0, tk.END)
    corrected_text = fix_grammar_and_spelling(user_input)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, corrected_text)

def translate_text():
    user_input = input_text.get(1.0, tk.END)
    target_language = target_language_combobox.get()
    translated_text = translate(user_input, target_language)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, translated_text)

def fix_grammar_and_spelling(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Correct the following text: '{text}'\n\n",
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def translate(text, target_language):
    translated = translator.translate(text, dest=target_language)
    return translated.text

def exit_application():
    window.destroy()

# Create the GUI window
window = tk.Tk()
window.title("Grammarly-like Grammar and Spelling Checker")

# Configure the window's appearance
window.geometry("1400x800")

# Apply a modern theme using ttkthemes
style = ThemedStyle(window)
style.set_theme("plastik")

# Create a frame for the input and output
frame_input = ttk.Frame(window)
frame_input.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

frame_output = ttk.Frame(window)
frame_output.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Text input field
input_text = tk.Text(frame_input, height=10, width=80, wrap=tk.WORD)
input_text.pack(fill=tk.BOTH, expand=True)

# Target language dropdown
languages = ['en', 'fr', 'es', 'de', 'it']  # Add more languages as needed
target_language_label = ttk.Label(frame_input, text="Select Target Language:")
target_language_label.pack(pady=10)
target_language_combobox = ttk.Combobox(frame_input, values=languages)
target_language_combobox.pack()


# Correct button (medium size)
correct_button = ttk.Button(frame_input, text="Correct", command=correct_text, width=15)
correct_button.pack(side=tk.LEFT, padx=10, pady=15)

# Translate button (medium size)
translate_button = ttk.Button(frame_input, text="Translate", command=translate_text, width=15)
translate_button.pack(side=tk.LEFT, padx=10, pady=15)

# Exit button (medium size)
exit_button = ttk.Button(frame_input, text="Exit", command=exit_application, width=15)
exit_button.pack(side=tk.RIGHT, padx=10, pady=15)

# Output field
output_text = tk.Text(frame_output, height=10, width=80, wrap=tk.WORD)
output_text.pack(fill=tk.BOTH, expand=True)

window.mainloop()
