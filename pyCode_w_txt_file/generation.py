##############################################################################
# Importing Python Libraries
##############################################################################
import numpy as np
import datetime

from validation import validator
from convertion import converter

##############################################################################
# FUNCTION TO CALCULATE AND STORE THE VARIABLES IN CHOICE 3 & 4 ARE THE SAME
##############################################################################
class generator:

    def __init__(self):
        self.__input_file = None
        self.__output_file = None
        self.validator=validator()
        self.converter=converter()
        
##############################################################################
#  SIMPLE ENCODER FOR CHOICE 3 AND 4
##############################################################################
    def charToMorse(self, char):
        text_morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
            'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
            'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..', " ": " ",
            '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
            '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'
        }
        
        char = char.upper()

        # Check if letter is in keys
        if char in text_morse_dict:
            return text_morse_dict[char]
            
        else:
            self.validator.check_morse_input_file_exists()
            self.validator.check_output_file_type()

            print('\n>>>Report generation completed!\n')
            self.validator.pressEnter()

            self.converter.decode_morse(self.__input_file, self.__output_file)
            self.generate_report(self.__input_file, self.__output_file)
        

    def textToMorse(self, line):
        output = ''
        for char in line[:-1]:  # Everything except the last
            output += self.charToMorse(char) + ','
        # Do the last separately
        output += self.charToMorse(line[-1])  # Only the last one
        return output
    


    def store_output_data(self, input_file, output_file):
        self.__input_file = input_file
        self.__output_file = output_file
        with open(self.__output_file, 'r') as output_file:
            content = output_file.read().upper()

        with open('./stopwords.txt', 'r') as stopword_file:
            stopwords = set(stopword_file.read().upper().split())

        # Find unique words in output content
        words = set(content.split())
        
        # Initialise dictionary to store KEY: VALUE which is WORD: COUNT
        word_frequency = {}
        for word in words:
            if word.isalpha():
                # Do a count for each word
                word_frequency[word] = content.split().count(word)


        # Sort words by frequency in ascending order
        sorted_by_frequency = sorted(word_frequency.items(), key=lambda x: x[1])

        # Organize words by frequency for printing
        words_by_frequency = {}
        for word, frequency in sorted_by_frequency:
            if frequency not in words_by_frequency:
                words_by_frequency[frequency] = []
            words_by_frequency[frequency].append((word, self.textToMorse(word)))

        # Append keywords not in stopwords to the keywords list
        keywords = [word for word in word_frequency if word not in stopwords]

        # Sort keywords by frequency in descending order
        keywords.sort(key=lambda x: word_frequency[x], reverse=True)

        return content, words_by_frequency, sorted_by_frequency, stopwords, keywords, word_frequency
    
        
##############################################################################
#  CHOICE 3
##############################################################################
    def generate_report(self, input_file, output_file):
        content, words_by_frequency, sorted_by_frequency, stopwords, keywords, word_frequency = self.store_output_data(input_file, output_file)

        current_time = datetime.datetime.now()
        report = f"                            REPORT GENERATED ON: {current_time.strftime('%d-%m-%Y %H:%M')}"

        report_header = [
            "*" * 100,
            report,
            "*" * 100,
            '',
            '*** Decoded Morse Text',
            content,
            '\n'
        ]

        report_body = []
        for frequency, word_list in words_by_frequency.items():
            report_body.append(f'*** Morse Words with frequency=> {frequency}')
            sorted_by_morse_length = sorted(word_list, key=lambda x: (-len(x[1]), x[0]))
            for word, morse in sorted_by_morse_length:
                label = '(*)' if word not in stopwords else ''
                report_body.append(f'[{morse}]=> {word} {label}')
            report_body.append('')

        report_body.append('*** Keywords sorted by frequency')
        for keyword in keywords:
            frequency = word_frequency[keyword]
            report_body.append(f'{keyword}({frequency})')

        full_report = report_header + report_body

        with open(self.__output_file, 'w') as output_file:
            output_file.write('\n'.join(full_report))

        with open(self.__output_file, 'r') as output_file:
            display_report = output_file.read()
            print(display_report)

##############################################################################
# CHOICE 4
##############################################################################
    def generate_graph(self, input_file, output_file):
        content, words_by_frequency, sorted_by_frequency, stopwords, keywords, word_frequency = self.store_output_data(input_file, output_file)

        current_time = datetime.datetime.now()
        graph = f"                            GRAPH GENERATED ON: {current_time.strftime('%d-%m-%Y %H:%M')}"
        graph_header = f"""
{'*' * 100}
{graph}
{'*' * 100}

"""
        

        graph_body = ""
        max_freq = max(word_frequency.values())
        max_spacing = ' ' * max_freq

        for idx, keyword in enumerate(keywords):
            stars = '*' * word_frequency[keyword]
            spaces = ' ' * (max_freq - word_frequency[keyword])
            morse_code = self.textToMorse(keyword)

            graph_body+=f'{spaces}{stars}-{morse_code}\n'
            graph_body+=f'{max_spacing}-{keyword}\n'
            graph_body+=f'{max_spacing}-\n' * 8

        lines = graph_body.split('\n')
        max_len = max(len(line) for line in lines)

        # Create a 2D list with each line padded to the maximum length
        padded_lines = [line.ljust(max_len) for line in lines]

        transposed_body_graph = ''
        for i in range(max_len):
            for line in padded_lines:
                if i < len(line):
                    transposed_body_graph += line[i]
                else:
                    transposed_body_graph += '  '
            transposed_body_graph += '\n'

        full_graph = graph_header + transposed_body_graph

        with open(self.__output_file, 'w') as output_file:
            output_file.write(full_graph)


        with open(self.__output_file, 'r') as output_file:
            display_graph = output_file.read()
            print(display_graph)


if __name__ == '__main__':
    generator = generator()
    generator.generate_graph('morse.txt', 'graph.txt')
