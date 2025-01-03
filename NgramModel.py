import re
import math
import random
import NgramAddKSmoothingModel
import InterpolationSmoothingModel
import numpy as np

class NGramModel:
    def __init__(self, model_name):
        """
        Initialize the class with the model name (file to read).
        """
        self.model_name = model_name
        self.trigram_counts = {}
        self.bigram_counts = {}
        self.unigram_counts = {}
        self.model_probabilities = {}
        self.starting_bigram = ""

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
        return f'##{processed_text}#'
 

    def ngrams(self, output, input, n):
        """
        Generate n-grams and update the output dictionary with their counts.
        
        Parameters:
        output - dictionary to store n-gram counts
        input - list of tokens (processed words)
        n - the size of n-grams to generate
        """
        for i in range(len(input) - n + 1):
            g = ''.join(input[i:i + n])
            output.setdefault(g, 0)
            output[g] += 1
        return output

    def train_model(self):
        """
        This function reads the corpus from a file, preprocesses and get the counts for character level trigrams, bigrams and unigrams
        """

        # Read all the lines in a file
        with open(self.model_name, "r") as file:
            lines = file.readlines()

        # Process each line in the file
        for l_num in lines:
            process_sentence = self.preprocess_line(l_num.strip())
            tokens = list(process_sentence)  # Convert processed sentence into a list of characters (tokens)
            
            # Count the n-grams and update the respective dictionaries
            self.trigram_counts = self.ngrams(self.trigram_counts, tokens, 3)
            self.bigram_counts = self.ngrams(self.bigram_counts, tokens, 2)
            self.unigram_counts = self.ngrams(self.unigram_counts, tokens, 1)

        return self.trigram_counts, self.bigram_counts, self.unigram_counts
    
    def perplexity(self, text, model, hyper_paramater=None):
        """
        This function calculates perplexity of a document against the trained models

        Parameters:
        text - The text content of the document
        model - The type of model (Add-k / Interpolation)
        hyper_paramater - Hyper parameter to be passed to the model
        """

        ngram_model_add_k = NgramAddKSmoothingModel.NgramAddKSmoothingModel(self.trigram_counts,self.bigram_counts,self.unigram_counts)
        ngram_model_interpolation = InterpolationSmoothingModel.InterpolationSmoothingModel(self.trigram_counts,self.bigram_counts,self.unigram_counts)
        
        # Window size is 3 to get all the trigrams
        window_size = 3
        trigrams = []
        n = 0


        for line in text.split():
            preprocess_text = self.preprocess_line(line)
            for i in range(len(preprocess_text) - window_size + 1):
                trigrams.append(preprocess_text[i:i+window_size])

        log_sum = 0


        for trigram in trigrams:
            # Get the probability of the trigram
            probability = ngram_model_add_k.add_k_smoothing_probability(trigram, hyper_paramater) if model == "add_k" else ngram_model_interpolation.smoothed_trigram_probability(trigram, hyper_paramater)
            # Sum of the logs of corresponding probabilities
            log_sum = log_sum + math.log(probability,2)
            # Count the number of trigrams
            n = n + 1
        if n > 0:
            # Average negative log probability
            avg_log_prob = -(log_sum) / float(n)

        # Average negative log probability exponentiated to 2
        result = pow(2, avg_log_prob)
        return result

    def optimize_k(self, validation_corpus):
         """
         Function to optimise the value of K for alpha smoothing
         """
         k_values = [0.00001, 0.0001, 0.001, 0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
         best_k = None
         best_perplexity = float('inf')

         for k in k_values:
             perplexity = self.perplexity(validation_corpus, "add_k", k)
             print("K value:", k, " Perplexity", perplexity)
             if(perplexity < best_perplexity):
                 best_perplexity = perplexity
                 best_k = k

         print('best k: ',best_k)    


    def optimize_lambdas(self, validation_corpus):
        """
        Function to find the lambda values with lower perplexity
        """
        lambda_values = [(0.9, 0.05), (0.8, 0.05), (0.8, 0.1), (0.7, 0.2), (0.7, 0.1), (0.6, 0.3), (0.4, 0.3)]

        best_lambda = None
        best_perplexity = float('inf')

        for value in lambda_values:
            perplexity = self.perplexity(validation_corpus, "interpolation", value)
            print("lambdas:", value, "perplexity: ", perplexity)
            if(perplexity < best_perplexity):
                best_perplexity = perplexity
                best_lambda = value

        print('best lambda:', best_lambda)

            
             
    


    
    
    

  
    


