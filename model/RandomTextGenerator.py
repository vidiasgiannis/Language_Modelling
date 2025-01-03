import string
import random
import re

class RandomTextGenerator:

    model_file_path = ""
    model_probabilities = {}
    starting_bigram = ""

    # Allowed characters from vocabulary
    characters = 'abcdefghijklmnopqrstuvwxyz0_.'

    def __init__(self, model_file_path, starting_bigram):
        """
        Initializes the model file path and starting bigram to start generation

        Parameters:
        model_file_path - Path to the model file
        starting_bigram - Starting bigram for generation of text
        """
        self.model_file_path = model_file_path
        self.starting_bigram = starting_bigram

        with open(model_file_path, "r") as f:
            for line in f:
                split_line = line.split()
                if(len(split_line) > 1):
                    key = split_line[0]
                    value = split_line[1]
                    self.model_probabilities[key] = value
                else:
                    print("Line not splittable", split_line)
    

    def generate_from_lm(self, n):
        """
        Generate text given a language model

        Parameters:
        n - number of characters to generate
        """
        generated_string = self.starting_bigram
        starting_random_bigram = self.starting_bigram

        while len(generated_string)<300:
            # Filter out all potential trigrams given a starting bigram
            filtered_dict = {k: v for k, v in self.model_probabilities.items() if k.startswith(starting_random_bigram)}

            if(len(filtered_dict) > 0):
                v = list(filtered_dict.values())
                k = list(filtered_dict.keys())
                normalized_probs = [float(p) for p in filtered_dict.values()]

                # Weighted random pick of trigram based on probabilities
                predicted_trigram = random.choices(list(filtered_dict.keys()), normalized_probs, k=1)
                
                # The output string
                generated_string = generated_string + predicted_trigram[0][-1]
                starting_random_bigram = generated_string[-2:]

            else:
                # This condition signals end of a sentence. Reset the starting bigram to look for beginning of the next sentence
                print("No trigram found for", starting_random_bigram)
                starting_random_bigram = "##"
        
        # Replace '_' with space
        generated_string = re.sub('_', " ", generated_string)

        # Replace beginning and end of sentence markers
        generated_string = re.sub('##', " ", generated_string)
        generated_string = re.sub('#', "", generated_string)
        return generated_string

        
