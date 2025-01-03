import itertools
import math
import NgramModel
import os

class InterpolationSmoothingModel:
    def __init__(self, trigram_counts, bigram_counts, unigram_counts):
        """
        Initialize the InterpolationSmoothingModel with the necessary n-gram counts.

        Parameters:
        trigram_counts - dictionary storing trigram counts
        bigram_counts - dictionary storing bigram counts
        unigram_counts - dictionary storing unigram counts
        """
        self.trigram_counts = trigram_counts
        self.bigram_counts = bigram_counts
        self.unigram_counts = unigram_counts

    

    def raw_trigram_probability(self, trigram):
        """
        Returns the raw trigram probability.
        """
        if self.bigram_counts.get(trigram[:2], 0) != 0:
            return self.trigram_counts.get(trigram, 0) / self.bigram_counts[trigram[:2]]
        else:
            return 0.0

    def raw_bigram_probability(self, bigram):
        """
        Returns the raw bigram probability.
        """
        if self.unigram_counts.get(bigram[0], 0) != 0:
            return self.bigram_counts.get(bigram, 0) / self.unigram_counts[bigram[0]]
        else:
            return 0.0

    def raw_unigram_probability(self, unigram):
        """
        Returns the raw unigram probability.
        """
        return self.unigram_counts.get(unigram, 0) / sum(self.unigram_counts.values())

    def smoothed_trigram_probability(self, trigram, hyper_parameter=None):
        """
        Returns the smoothed trigram probability using linear interpolation.
        """
        if(hyper_parameter is None):
            lambda1 = 0.7
            lambda2 = 0.1
            lambda3 = 0.2
        else:
            lambda1 = hyper_parameter[0]
            lambda2 = hyper_parameter[1]
            lambda3 = 1 - (lambda1 + lambda2)

        smoothed = 0.0
        smoothed += lambda1 * self.raw_trigram_probability(trigram)
        smoothed += lambda2 * self.raw_bigram_probability(trigram[1:])  # Trigram without the first character
        smoothed += lambda3 * self.raw_unigram_probability(trigram[2:])  # Trigram without the first two characters

        return smoothed
    
    
    
    def write_interpolation_smoothed_probabilities(self, characters, output_file):
        
    
    # Generate all possible trigrams from the given character set
        # trigrams = [''.join(gram) for gram in itertools.product(characters, repeat=3)]

        # with open(output_file, "w") as model_file:
        #     for trigram in trigrams:
        #         # Calculate the smoothed trigram probability using the interpolation model
        #         probability = self.smoothed_trigram_probability(trigram)  # Pass trigram as a string
                
        #         # Write the trigram and its probability to the file
        #         model_file.write(f"{trigram}   {probability}\n")
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
                probability = self.smoothed_trigram_probability(trigram)
                
                # Write the trigram and its probability to the file
                model_file.write(f"{trigram}\t{probability}\n")

    
    