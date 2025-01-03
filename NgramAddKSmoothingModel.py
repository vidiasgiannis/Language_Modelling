import math
import re
import itertools
import os

class NgramAddKSmoothingModel:
    def __init__(self, trigram_counts=None, bigram_counts=None, unigram_counts=None):
        """
        Initialize the NgramAddKSmoothingModel with the necessary attributes.
        
        Parameters:
        model_name - the name of the model (file containing training data)
        """
        self.trigram_counts = trigram_counts if trigram_counts is not None else {}
        self.bigram_counts = bigram_counts if bigram_counts is not None else {}
        self.unigram_counts = unigram_counts if unigram_counts is not None else {}

   
    def add_k_smoothing_probability(self, trigram, k=None):
        """
        Calculate trigram probability with add-k smoothing.

        Parameters:
        trigram - the trigram tuple (e.g., ('a', 'b', 'c'))
        """
        if(k is None):
            k=0.5
        if('#' in trigram[:-1]):
            total_vocabulary_size = 29  # Size of the vocabulary
        else:
            total_vocabulary_size = 30
        bigram_count = self.bigram_counts.get(trigram[:-1], 0)  # Get the bigram (first two elements of trigram)
        trigram_prob = (self.trigram_counts.get(trigram, 0) + float(k)) / (bigram_count + (k * total_vocabulary_size))
        return trigram_prob
    
    def write_trigram_probabilities_to_file(self, characters, output_file):
        """
        Generate all possible trigrams from the list of characters and write their add-k smoothed
        probabilities to a file.

        Parameters:
        characters - list of characters to generate trigrams from
        output_file - name of the output file to save trigram probabilities
        """
        # trigrams = [''.join(gram) for gram in itertools.product(characters, repeat=3)]  # Generate all possible trigrams
        # trigram_probabilities = {}

        # with open(output_file, "w") as model_file:
        #     for gram in trigrams:
        #         # Calculate the k-smoothing probability
        #         probability = self.add_k_smoothing_probability(gram)  # Pass as a string
        #         trigram_probabilities[gram] = probability
        #         # Write the trigram and its probability to the file
        #         model_file.write(f"{gram}   {probability}\n")
        
        output_dir = "model"
        os.makedirs(output_dir, exist_ok=True)

        # Generate all possible trigrams from the given character set
        trigrams = [''.join(gram) for gram in itertools.product(characters, repeat=3)]
        filtered_trigrams = []

        for trigram in trigrams:
            # Exclude trigrams like a## (first char is anything, followed by ##)
            if trigram[1] == '#' and trigram[2] == '#':
                continue
            # Exclude trigrams like ###
            if trigram[0] == '#' and trigram[1] == '#' and trigram[2] == '#':
                continue
            # Exclude trigrams like a#a (same first and third char, # in the middle)
            if trigram[0] !='#' and trigram[2] != '# 'and trigram[1] == '#':
                continue
            # Exclude trigrams like #a# (first and third are #, anything in the middle)
            if trigram[0] == '#' and trigram[2] == '#':
                continue
 
            # Append valid trigrams
            filtered_trigrams.append(trigram)
           

        # Construct the full path to the output file inside the "model" folder
        output_path = os.path.join(output_dir, output_file)

        with open(output_path, "w") as model_file:
            for trigram in filtered_trigrams:
                # Calculate the smoothed trigram probability using the interpolation model
                probability = self.add_k_smoothing_probability(trigram)
                
                # Write the trigram and its probability to the file
                model_file.write(f"{trigram}\t{probability}\n")

        
    
    
    
   


