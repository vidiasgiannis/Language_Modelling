# Language Modeling Project - ANLP 2024

This repository contains the implementation and report for **Assignment 1** of the Advanced Natural Language Processing (ANLP) 2024 course. The focus is to build a character-level trigram language model and analyze its performance on language detection tasks.

## **Overview**

The key objectives of this project are:
- **Build a trigram language model**: Construct a character-level language model from training data.
- **Generate random sequences**: Use the language model to generate random text sequences.
- **Preprocess input data**: Normalize input by lowercasing, removing special characters, and converting digits.
- **Evaluate models with perplexity**: Calculate the perplexity of test documents using language models.

## **Repository Structure**

```
/data/            # Training and test datasets (English, Spanish, German)
/model/           # Python scripts including main.py (entry point for running the model)
/README.md        # Project documentation
/requirements.txt # List of dependencies for installing with pip
/report.pdf       # Report containing analysis and implementation details
```

## **Key Features**

1. **Preprocessing**  
   Converts text to lowercase, removes non-alphanumeric characters (except `.`), and normalizes digits to `0`.

2. **Language Model Construction**  
   Collects character 3-grams and estimates probabilities using the maximum likelihood estimation (MLE).

3. **Sequence Generation**  
   Generates text sequences based on the trigram model’s probabilities.

4. **Perplexity Computation**  
   Computes perplexity to measure how well a model predicts unseen text.

## **How to Run the Project**

1. **Clone the Repository**
   ```bash
   git clone <your-repository-url>
   cd <repository-folder>
   ```

2. **Install Dependencies**  
   Ensure Python 3.x is installed and run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Project**  
   To run the main script:
   ```bash
   python model/main.py
   ```