##############################################################################
# Importing Class
##############################################################################
from convertion import converter

##############################################################################
#  CHOICE 6: WII Enigma Machine
##############################################################################

class EnigmaMachine(converter):
    def __init__(self, rotor=None):
        # Initialize the parent class
        super().__init__()
        # Initialize the rotors with lists of characters from 'A' to 'Z'
        self.__rotors = [[chr(i) for i in range(65, 91)] for _ in range(3)]
        # Set up predefined reflector mapping
        self.__reflector = {'A': 'Y', 'B': 'R', 'C': 'U', 'D': 'H', 'E': 'Q', 'F': 'S', 'G': 'L', 'H': 'D',
                            'I': 'P', 'J': 'X', 'K': 'N', 'L': 'G', 'M': 'O', 'N': 'K', 'O': 'M', 'P': 'I',
                            'Q': 'E', 'R': 'B', 'S': 'F', 'T': 'Z', 'U': 'C', 'V': 'W', 'W': 'V', 'X': 'J',
                            'Y': 'A', 'Z': 'T'}
        if rotor:
            self.set_rotor(rotor)
        else:
            self.__rotor = [0, 0, 0]

    def set_rotor(self, positions):
        self.__rotor = positions

    def rotate_rotors(self):
        # Rotate the first rotor and check for full rotation
        self.__rotor[0] = (self.__rotor[0] + 1) % 26
        if self.__rotor[0] == 0:
            # Rotate the second rotor if the first has completed a full rotation
            self.__rotor[1] = (self.__rotor[1] + 1) % 26
            if self.__rotor[1] == 0:
                # Rotate the third rotor if the second has completed a full rotation
                self.__rotor[2] = (self.__rotor[2] + 1) % 26

    def encode_decode(self, text):
        output = ''
        for letter in text:
            if letter.isalpha():
                for i in range(3):
                    pos = (ord(letter.upper()) - 65 + self.__rotor[i]) % 26
                    letter = self.__rotors[i][pos]

                # Reflect the letter
                letter = self.__reflector[letter]
                for i in range(2, -1, -1):
                    # In the Enigma machine, letters pass through the rotors from right to left during decoding,
                    # so we start from the third rotor (index 2) and move towards the first rotor (index 0).
                    pos = (self.__rotors[i].index(letter) - self.__rotor[i] + 26) % 26
                    letter = chr(pos + 65)
            output += letter
            self.rotate_rotors()
        return output

    def prompt_rotor(self):
        rotor = []
        for i in range(3):
            while True:
                try:
                    pos = int(input(f"Enter rotor {i+1} position (1-26): "))
                    if pos < 1 or pos > 26:
                        raise ValueError("Position must be between 1 and 26.\n")
                    rotor.append(pos - 1)  # Convert to 0-based index
                    break
                except ValueError as e:
                    print(e)
        return rotor

    def run(self, input_file, output_file):
        rotor = self.prompt_rotor()
        self.set_rotor(rotor)

        with open(input_file, 'r') as file:
            plaintext = file.read()

        print()
        ciphertext = self.encode_decode(plaintext)

        with open(output_file, 'w') as file:
            file.write(ciphertext)

        print(">>>Encryption complete. Check the output file for the ciphertext.")
        self.display_text_files(input_file, output_file)

# Save this file as enigma.py
if __name__ == "__main__":
    input_file = input("Enter the input file path: ")
    output_file = input("Enter the output file path: ")
    enigma = EnigmaMachine()
    enigma.run(input_file, output_file)
