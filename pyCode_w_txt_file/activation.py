##############################################################################
# Importing Python Classes
##############################################################################
import subprocess
tk_installed = subprocess.run(['pip', 'show', 'tk'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
pyaudio_installed = subprocess.run(['pip', 'show', 'pyaudio'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
# install if not installed yet
if not tk_installed:
    subprocess.run(['pip', 'install', 'tk'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if not pyaudio_installed:
    subprocess.run(['pip', 'install', 'pyaudio'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


from validation import validator
from convertion import converter
from generation import generator
from gui_converter import MorseCodeApp
from enigma import EnigmaMachine

##############################################################################
# Main Class
##############################################################################
class MorseCodeAnalyzer:

    # Initialising files
    def __init__(self):
        self.validator = validator()
        self.converter = converter()
        self.generator = generator()

    ##############################################################################
    #  START PROGRAM FUNCTION
    ##############################################################################

    def main(self):
        print('')
        print('*' * 50)
        print('* ST1507 DSAA: MorseCode Message Analyzer', ' ' * 6, '*')
        print('*________________________________________________*')
        print('*                                                *')
        print('*  - Done By: Shaun Kwo Rui Yu(2317933)          *')
        print('*  - Class DAAA/2A/03                            *')
        print('*' * 50, '\n\n')

        self.validator.pressEnter()

        while True:
            choice = input('''
Please select your choice ('1','2','3','4','5','6','7'):
    1. Convert Text To Morse Code
    2. Convert Morse Code To Text
    3. Generate Morse Word Frequencies Report
    4. Generate Morse Keyword Frequencies Graph
    5. Morse Code Converter and Flashlight
    6. WWII Engima Machine
    7. Exit
Enter choice: ''')

            if choice == '1':
                self.validator.create_input_file()
                input_file = self.validator.check_alphabet_input_file_exists()
                output_file = self.validator.check_output_file_type()
                input_file, output_file =self.converter.encode_morse(input_file, output_file)
                print()
                self.validator.pressEnter()
                self.converter.display_text_files(input_file,output_file)
                self.validator.pressEnter()
                pass


            elif choice == '2':
                self.validator.create_input_file()
                input_file = self.validator.check_morse_input_file_exists()
                output_file = self.validator.check_output_file_type()
                input_file, output_file =self.converter.decode_morse(input_file, output_file)
                print()
                self.validator.pressEnter()
                self.converter.display_text_files(input_file,output_file)
                self.validator.pressEnter()
                pass


            elif choice == '3':
                input_file = self.validator.check_morse_input_file_exists()
                output_file = self.validator.check_output_file_type()
                print('\n>>>Report generation completed!\n')
                self.validator.pressEnter()
                print()
                self.converter.decode_morse(input_file, output_file)
                self.generator.generate_report(input_file, output_file)
                pass


            elif choice == '4':
                input_file = self.validator.check_morse_input_file_exists()
                output_file = self.validator.check_output_file_type()

                print('\n>>>Graph generation completed!\n')
                self.validator.pressEnter()
                print()
                self.converter.decode_morse(input_file,output_file)
                self.generator.generate_graph(input_file, output_file)

                pass
            elif choice == '5':
                gui_app = MorseCodeApp()
                gui_app.run()

            elif choice == '6':
                input_file = self.validator.check_alphabet_input_file_exists()
                output_file = self.validator.check_output_file_type()
                engima= EnigmaMachine()
                engima.run(input_file, output_file)

                pass
            elif choice == '7':
                print("Bye, thanks for using ST1507 DSAA: MorseCode Message Analyzer")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    # This block will run only if this file is executed directly,
    # not when it's imported as a module
    analyzer = MorseCodeAnalyzer()
    analyzer.main()
