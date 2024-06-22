##############################################################################
# Importing Python Libraries
##############################################################################
import getpass, os

##############################################################################
#  SMALL FUNCTIONS FOR CHECKING AND STREAMLINING OF PROGRAM TO PREVENT CRASHES
##############################################################################
class validator:

    # Initialising files
    def __init__(self):
        self.__input_file=''
        self.__output_file=''
        pass

    def pressEnter(self):
        user_input = getpass.getpass("Press Enter, to continue....")
        if not user_input:
            pass
        else:   
            print("You must press Enter to continue.")
            self.pressEnter()

    def only_has_alphabets(self):
        with open(self.__input_file, 'r') as file:
            input_text = file.read()
        for c in input_text:
            if not (c.isalpha() or c.isspace()):
                return False
        return True
    

    def check_alphabet_input_file_exists(self):
        while True:
            self.__input_file = input("\nPlease enter input file: ")
            if os.path.isfile(self.__input_file) and self.__input_file.lower().endswith('.txt') and self.only_has_alphabets():
                return self.__input_file
            else:
                print("Invalid input file or .txt file extension or does not only have alphabets.")

    def has_no_alphabets(self):
        with open(self.__input_file, 'r') as file:
            input_text = file.read()
        for c in input_text:
            if c.isalpha():
                return False
        return True

    def check_morse_input_file_exists(self):
        while True:
            self.__input_file = input("\nPlease enter input file: ")
            if os.path.isfile(self.__input_file) and self.__input_file.lower().endswith('.txt') and self.has_no_alphabets():
                return self.__input_file
            else:
                print("Invalid input file. Please provide a valid .txt file or morse code file\nFile should not have alphabets.")
        
    def check_output_file_type(self):
        while True:
            self.__output_file = input("Please enter output file: ")
            if self.__output_file.lower().endswith('.txt'):
                return self.__output_file
            else:
                print("Output file must have a .txt extension.")

def create_input_file(self):
    file_name = input("\nIf you want to create file (no need .txt ending), please enter the file name else just press enter: ").strip()
    if not file_name:
        return None

    if not file_name.endswith(".txt"):
        file_name += ".txt"

    print("\nPlease enter the text below and press Enter to Exit. End with an empty line:")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    user_text = "\n".join(lines)

    with open(file_name, 'w') as file:
        file.write(user_text)

    print(f"{file_name} has been successfully created!")
