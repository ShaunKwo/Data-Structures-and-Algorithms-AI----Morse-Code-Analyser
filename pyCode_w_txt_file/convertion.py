##############################################################################
# Importing Class
##############################################################################
from validation import validator

##############################################################################
#  CHOICE 1: COMPLEX MORSE ENCODER WITH TEXT WITH SENTENCES AND PARAGRAPHS
##############################################################################
class converter:

    # Initialising files
    def __init__(self):
        self.__input_file = None
        self.__output_file = None
        self.validator=validator()

        # Initialising dictionaries
        self.text_morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
            'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
            'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..', " ": " ",
            '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
            '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'
        }

        self.morse_text_dict={value: key for key, value in self.text_morse_dict.items()}



    def encode_morse(self, input_file, output_file):
        self.__input_file = input_file
        self.__output_file = output_file

        with open(self.__input_file, 'r') as input_file:
            input_text = input_file.read()

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

                encoded_word.append(','.join(encoded_letter))

            encoded_line.append(', ,'.join(encoded_word))

        with open(self.__output_file, 'w') as output_file:
            output_file.write('\n'.join(encoded_line))

        return self.__input_file, self.__output_file
    

##############################################################################
#  CHOICE 2: COMPLEX MORSE DECODER WITH TEXT WITH SENTENCES AND PARAGRAPHS
##############################################################################
    def decode_morse(self, input_file, output_file):
        self.__input_file = input_file
        self.__output_file = output_file
        with open(self.__input_file, 'r') as input_file:
            encoded_text = input_file.readlines()

        decoded_text = []
        for line in encoded_text:
            decoded_line = []
            for code in line.strip().split(','):
                if code in self.morse_text_dict:
                    decoded_line.append(self.morse_text_dict[code])
                else:
                    print(f"Error: Morse code '{code}' not recognized. Please enter a file with valid Morse codes.")
                    self.__input_file = self.validator.check_morse_input_file_exists()
                    return self.decode_morse(input_file, output_file)  
            decoded_text.append(''.join(decoded_line))

        with open(self.__output_file, 'w') as output_file:
            output_file.write('\n'.join(decoded_text))

        return self.__input_file, self.__output_file

    def display_text_files(self, input_file, output_file):
        self.__input_file = input_file
        self.__output_file = output_file
        with open(input_file, 'r') as input_file:
            input_content = input_file.read()

        with open(output_file, 'r') as output_file:
            content = output_file.read()
            
        print()
        print(f"Input File: {input_file.name}")
        print('='*100)
        print(input_content)
        print('='*100)
        print('\n')
        print(f"Output File: {output_file.name}")
        print('='*100)
        print(content)
        print('='*100)
        print()

if __name__ == '__main__':
    converter = converter()
    converter.display_text_files()
