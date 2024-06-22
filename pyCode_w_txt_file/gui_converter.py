#############################################################################
#  Importing Python Libraries
#############################################################################
import time, threading, pyaudio
import tkinter as tk
import numpy as np

#############################################################################
#  Choice 5: Morse Code GUI
#############################################################################
class MorseCodeApp:

    def __init__(self):
        self.root = tk.Tk()
        self.playing=False
        self.root.title("Morse Code Converter and Flashlight")
        self.root.geometry("800x800")
        self.root.config(bg="#f0f0f0")

        self.text_morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
            'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
            'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
            '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',' ': ' '
        }

        self.morse_text_dict = {value: key for key, value in self.text_morse_dict.items()}

        self.playing = False  # Flag to control playback
        self.create_widgets()

    def text_to_morse(self, input_text):
        encoded_line = []
        paragraphs = input_text.split('\n')
        
        for paragraph in paragraphs:
            words = paragraph.split()
            encoded_word = []

            for word in words:
                encoded_letter = []
                for letter in word.upper():
                    if letter in self.text_morse_dict:
                        encoded_letter.append(self.text_morse_dict[letter])
                    else:
                        tk.messagebox.showerror('Error',f"Character '{letter}' cannot be converted to Morse code.")
                        return ""

                encoded_word.append(','.join(encoded_letter))

            encoded_line.append(', ,'.join(encoded_word))

        return '\n'.join(encoded_line)

    def morse_to_text(self, input_text):
        decoded_text = []
        for line in input_text.split('\n'):
            decoded_line = []
            for code in line.split(','):
                if code in self.morse_text_dict:
                    decoded_line.append(self.morse_text_dict[code])
                else:
                    tk.messagebox.showerror('Error',f"Morse code '{code}' not recognized. Please enter alphabetic Morse codes.")
                    return ''
            decoded_text.append(''.join(decoded_line))

        return '\n'.join(decoded_text)

    def convert_text(self):
        self.stop_playing()  # Stop any ongoing playback
        mode = self.mode_var.get()
        input_text = self.input_text.get("1.0", tk.END).strip()
        output_text = ""

        if mode == "text_to_morse":
            output_text = self.text_to_morse(input_text)
        else:
            output_text = self.morse_to_text(input_text)

        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, output_text)
        self.output_text.config(state=tk.DISABLED)

        # Flash Morse code if conversion is successful
        if mode == "text_to_morse" and output_text:
            self.start_flashing(output_text)
        elif mode == "morse_to_text" and input_text and output_text:
            self.start_flashing(input_text)

    def play_tone(self, frequency, duration):
        p = pyaudio.PyAudio()
        volume = 0.5
        fs = 44100

        samples = (np.sin(2 * np.pi * np.arange(fs * duration) * frequency / fs)).astype(np.float32)

        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=fs,
                        output=True)

        stream.write(volume * samples)

        # Close the stream after playing
        stream.stop_stream()
        stream.close()


    def flash_dot(self, label):
        label.config(bg="yellow")
        label.update()
        threading.Thread(target=self.play_tone, args=(1000, 0.2)).start()
        time.sleep(0.2)
        label.config(bg="black")
        label.update()
        time.sleep(0.2)

    def flash_dash(self, label):
        label.config(bg="yellow")
        label.update()
        threading.Thread(target=self.play_tone, args=(1000, 0.6)).start()
        time.sleep(0.6)
        label.config(bg="black")
        label.update()
        time.sleep(0.2)

    def flash_space(self, label):
        time.sleep(0.8)

    def morse_flash(self, morse_code, label):
        self.playing = True
        for char in morse_code:
            if not self.playing:
                break
            if char == '.':
                self.flash_dot(label)
                time.sleep(0.2)
            elif char == '-':
                self.flash_dash(label)
                time.sleep(0.6)
            elif char == ' ':
                self.flash_space(label)
                time.sleep(0.8)
            elif char == ',':
                time.sleep(0.2)
        self.playing = False

    def start_flashing(self, morse_code):
        self.playing = True
        threading.Thread(target=self.morse_flash, args=(morse_code, self.flashlight_label)).start()

    def stop_playing(self):
        self.playing = False

    def clear_textboxes(self, *args):
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.stop_playing()
    
    def exit_program(self):
        self.stop_playing()
        self.root.quit()  # Stop the main event loop
        self.root.destroy()  # Destroy the window
        

    def create_widgets(self):
        # Create and configure the title label
        title_label = tk.Label(self.root, text="Morse Code Converter and Flashlight", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)

        # Create a frame to hold the mode selection radio buttons
        mode_frame = tk.Frame(self.root, bg="#f0f0f0")
        mode_frame.pack(pady=10)

        # Create a StringVar to hold the mode selection and set its default value
        self.mode_var = tk.StringVar(value="text_to_morse")
        self.mode_var.trace_add("write", self.clear_textboxes)

        # Create and configure the "Text to Morse" radio button
        text_to_morse_rb = tk.Radiobutton(mode_frame, text="Text to Morse", variable=self.mode_var,
                                        value="text_to_morse", bg="#f0f0f0", font=("Helvetica", 12))
        text_to_morse_rb.grid(row=0, column=0, padx=20)

        # Create and configure the "Morse to Text" radio button
        morse_to_text_rb = tk.Radiobutton(mode_frame, text="Morse to Text", variable=self.mode_var,
                                        value="morse_to_text", bg="#f0f0f0", font=("Helvetica", 12))
        morse_to_text_rb.grid(row=0, column=1, padx=20)

        # Create a frame to hold the input and output text boxes
        text_frame = tk.Frame(self.root, bg="#f0f0f0")
        text_frame.pack(pady=20)

        # Create and configure the input label
        input_label = tk.Label(text_frame, text="Input Box", font=("Helvetica", 12), bg="#f0f0f0")
        input_label.grid(row=0, column=0, sticky="w", padx=10)

        # Create and configure the input text box
        self.input_text = tk.Text(text_frame, height=5, width=70, font=("Helvetica", 12))
        self.input_text.grid(row=1, column=0, padx=10, pady=10)

        # Create and configure the output label
        output_label = tk.Label(text_frame, text="Display Output Box", font=("Helvetica", 12), bg="#f0f0f0")
        output_label.grid(row=2, column=0, sticky="w", padx=10)

        # Create and configure the output text box (initially disabled)
        self.output_text = tk.Text(text_frame, height=5, width=70, font=("Helvetica", 12), state=tk.DISABLED)
        self.output_text.grid(row=3, column=0, padx=10, pady=10)

        # Create and configure the flashlight title label
        flashlight_title_label = tk.Label(self.root, text="Morse Code Flashlight", font=("Helvetica", 18, "bold"), bg="#f0f0f0")
        flashlight_title_label.pack(pady=10)

        # Create and configure the flashlight label (initially black)
        window_width = self.root.winfo_reqwidth()
        self.flashlight_label = tk.Label(self.root, bg="black", width=window_width, height=10)
        self.flashlight_label.pack(pady=20)

        # Create a frame to hold the buttons
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=20)

        # Create and configure the "Generate" button
        generate_button = tk.Button(button_frame, text="Generate", command=self.convert_text, bg="#4CAF50", fg="white",
                                    font=("Helvetica", 12), padx=20, pady=10)
        generate_button.pack(side=tk.LEFT, padx=10)

        # Create and configure the "Exit" button
        exit_button = tk.Button(button_frame, text="Exit", command=self.exit_program, bg="red", fg="white",
                                font=("Helvetica", 12), padx=20, pady=10)
        exit_button.pack(side=tk.RIGHT, padx=10)


    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MorseCodeApp()
    app.run()