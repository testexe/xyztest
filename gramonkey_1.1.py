import ctypes
import sys
import tkinter as tk
from tkinter import ttk, simpledialog
from ttkthemes import ThemedStyle
import openai
from googletrans import Translator
from datetime import datetime, timedelta

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():                           
    print("Running as administrator")
    translator = Translator()
# Dark and Light Mode Colors
    dark_mode_bg = "black"
    dark_mode_fg = "white"
    light_mode_bg = "white"
    light_mode_fg = "black"
# Default mode is Light Mode
    current_mode = "light"
# Initialize the API key and expiration date
    api_key = ""
    api_key_expiration_date = datetime.now() + timedelta(days=15)
    openai.api_key = api_key
    
    def toggle_dark_light_mode():
        global current_mode
        if current_mode == "light":
            current_mode = "dark"
            set_dark_mode()
        else:
            current_mode = "light"
            set_light_mode()

    def set_dark_mode():
        window.configure(bg=dark_mode_bg)
        frame_input.configure(style="Dark.TFrame")
        frame_output.configure(style="Dark.TFrame")
        input_text.config(bg=dark_mode_bg, fg=dark_mode_fg, insertbackground=dark_mode_fg)
        output_text.config(bg=dark_mode_bg, fg=dark_mode_fg, insertbackground=dark_mode_fg)
    
    # Update styles for buttons and combobox
        set_dark_style_to_widgets()

    def set_light_mode():
        window.configure(bg=light_mode_bg)
        frame_input.configure(style="Light.TFrame")
        frame_output.configure(style="Light.TFrame")
        input_text.config(bg=light_mode_bg, fg=light_mode_fg, insertbackground=light_mode_fg)
        output_text.config(bg=light_mode_bg, fg=light_mode_fg, insertbackground=light_mode_fg)
    
    # Update styles for buttons and combobox
        set_light_style_to_widgets()

    def set_dark_style_to_widgets():
        correct_button.configure(style="Dark.TButton")
        translate_button.configure(style="Dark.TButton")
        exit_button.configure(style="Dark.TButton")
        target_language_combobox.configure(style="Dark.TCombobox")  # Update style for the combobox
        settings_menu.entryconfig("Dark Mode", state="disabled")
        settings_menu.entryconfig("Light Mode", state="active")
        settings_menu.entryconfig("Renew API Key", state="active")

    def set_light_style_to_widgets():
        correct_button.configure(style="Light.TButton")
        translate_button.configure(style="Light.TButton")
        exit_button.configure(style="Light.TButton")
        target_language_combobox.configure(style="Light.TCombobox")  # Update style for the combobox
        settings_menu.entryconfig("Dark Mode", state="active")
        settings_menu.entryconfig("Light Mode", state="disabled")
        settings_menu.entryconfig("Renew API Key", state="active")

    def correct_text():
        user_input = input_text.get("1.0", "end-1c")
        if user_input.strip():
            try:
                corrected_text = fix_grammar_and_spelling(user_input)
                output_text.config(state=tk.NORMAL)
                output_text.delete("1.0", tk.END)
                output_text.insert(tk.END, corrected_text)
                output_text.config(state=tk.DISABLED)
            except Exception as e:
                show_error("Error", f"An error occurred: {str(e)}")
        else:
            show_info("Information", "Please enter text to correct.")

    def translate_text():
        user_input = input_text.get("1.0", "end-1c")
        if user_input.strip():
            target_language = target_language_combobox.get()
            try:
                translated_text = translate(user_input, target_language)
                output_text.config(state=tk.NORMAL)
                output_text.delete("1.0", tk.END)
                output_text.insert(tk.END, translated_text)
                output_text.config(state=tk.DISABLED)
            except Exception as e:
                show_error("Error", f"An error occurred: {str(e)}")
        else:
            show_info("Information", "Please enter text to translate.")

    def renew_api_key():
            global api_key, api_key_expiration_date
            new_api_key = simpledialog.askstring("Renew API Key", "Enter your new API key:")
            if new_api_key:
                api_key = new_api_key
                api_key_expiration_date = datetime.now() + timedelta(days=15)
                openai.api_key = api_key
                show_info("API Key Renewed", "Your API key has been renewed.")
            else:
                show_info("API Key Not Renewed", "No new API key provided.")

    def check_api_key():
            global api_key_expiration_date  # Declare api_key_expiration_date as global
            if datetime.now() > api_key_expiration_date:
        # Your API key has expired. Please renew it and talk to the vendor.
                renew_and_talk_message = "Your API key has expired. Please renew it and talk to the vendor."
                new_api_key = simpledialog.askstring("Renew API Key", renew_and_talk_message + "\nEnter your new API key:")
                if new_api_key:
                    api_key = new_api_key
                    api_key_expiration_date = datetime.now() + timedelta(days=15)
                    openai.api_key = api_key
                    show_info("API Key Renewed", "Your API key has been renewed.")
                else:
                    show_info("API Key Not Renewed", "No new API key provided.")
                    exit_application()



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

    def show_info(title, message):
        tk.messagebox.showinfo(title, message)

    def show_error(title, message):
        tk.messagebox.showerror(title, message)

# Create the GUI window
    window = tk.Tk()
    window.title("Gramonkey")
    window.iconbitmap("gramonkey.ico")  
    window.geometry("1600x900")  # Increased size

# Apply a modern theme using ttkthemes
    style = ThemedStyle(window)
    style.set_theme("arc")  # Change theme to "arc"

# Create a frame for the input and output
    frame_input = ttk.Frame(window, style="Light.TFrame")  # Initial style set to Light Mode
    frame_input.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

    frame_output = ttk.Frame(window, style="Light.TFrame")  # Initial style set to Light Mode
    frame_output.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Text input field (Increased size)
    input_text = tk.Text(frame_input, height=15, width=100, wrap=tk.WORD, font=("Arial", 14))  # Increased height and width, adjusted font size
    input_text.pack(fill=tk.BOTH, expand=True)

# Target language dropdown
    languages = ['en', 'fr', 'es', 'de', 'it', 'zh-CN']  # Add more languages as needed
    target_language_label = ttk.Label(frame_input, text="Select Target Language:")
    target_language_label.pack(pady=10)
    target_language_combobox = ttk.Combobox(frame_input, values=languages)
    target_language_combobox.pack()

# Correct button (Medium size)
    correct_button = ttk.Button(frame_input, text="Fix", command=correct_text, width=20)  # Increased width
    correct_button.pack(side=tk.LEFT, padx=10, pady=15)

# Translate button (Medium size)
    translate_button = ttk.Button(frame_input, text="Translate", command=translate_text, width=20)  # Increased width
    translate_button.pack(side=tk.LEFT, padx=10, pady=15)

# Exit button (Medium size)
    exit_button = ttk.Button(frame_input, text="Exit", command=exit_application, width=20)  # Increased width
    exit_button.pack(side=tk.RIGHT, padx=10, pady=15)

# Output field (Increased size)
    output_text = tk.Text(frame_output, height=15, width=100, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 14))  # Increased height and width, adjusted font size
    output_text.pack(fill=tk.BOTH, expand=True)

# Create the top menu
    menu = tk.Menu(window)
    window.config(menu=menu)

# Add a "Settings" menu
    settings_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Settings", menu=settings_menu)

# Add Dark Mode and Light Mode options
    settings_menu.add_command(label="Dark Mode", command=toggle_dark_light_mode)
    settings_menu.add_command(label="Light Mode", command=toggle_dark_light_mode)

# Add "Renew API Key" option
    settings_menu.add_command(label="Renew API Key", command=renew_api_key)

# Initialize the GUI in Light Mode
    set_light_mode()

# Check API key expiration
    check_api_key()

    window.mainloop()

else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
