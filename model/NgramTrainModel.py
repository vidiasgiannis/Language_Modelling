import re

class NgramTrainModel:
    def __init__(self, model_name):
        """
        Initialize the NgramTrainModel with the name of the model (training data file).
        
        Parameters:
        model_name - the name of the file containing the training data
        """
        self.model_name = model_name
        self.trigram_counts = {}
        self.bigram_counts = {}
        self.unigram_counts = {}

    def preprocess_line(self, line):
        """
        Preprocess the input line by keeping only alphabets, spaces, and periods.
        Convert digits to '0' and lowercase all characters.
       
        Parameters:
        line - the input sentence to preprocess
        """
        expression = r'[a-zA-Z\s\.]+|\d+'
        matches = re.findall(expression, line)  # Extract alphabets, spaces, periods, and digits
        processed_text = ''.join(re.sub('\d', '0', match.lower()) for match in matches)  # Replace digits and lowercase
        processed_text = re.sub(' ', "_", processed_text)
        return f'##{processed_text}#'

    def ngrams(self, output, input_tokens, n):
        """
        Generate n-grams from the input tokens and update the output dictionary with their counts.
        
        Parameters:
        output - dictionary to store n-gram counts
        input_tokens - list of tokens (processed characters)
        n - the size of n-grams to generate
        """
        for i in range(len(input_tokens) - n + 1):
            g = ''.join(input_tokens[i:i + n])  # Join n tokens to form the n-gram
            output.setdefault(g, 0)
            output[g] += 1
        return output

    def train_model(self):
        """
        Read the training data from the model file and process each line to generate unigram, bigram, and trigram counts.
        """
        with open(self.model_name, "r") as file:
            lines = file.readlines()

        # Process each line in the file
        for l_num in lines:
            process_sentence = self.preprocess_line(l_num.strip())  # Preprocess each line
            tokens = list(process_sentence)  # Convert the processed sentence into a list of characters (tokens)

            # Count the n-grams and update the respective dictionaries
            self.ngrams(self.trigram_counts, tokens, 3)
            self.ngrams(self.bigram_counts, tokens, 2)
            self.ngrams(self.unigram_counts, tokens, 1)

        return self.trigram_counts, self.bigram_counts, self.unigram_counts
