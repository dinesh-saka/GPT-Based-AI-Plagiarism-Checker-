import streamlit as st
import nltk
from nltk.util import ngrams
from nltk.lm.preprocessing import pad_sequence, padded_everygram_pipeline
from nltk.lm import MLE
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import string

# Download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('brown')

def preprocess_text(text):
    tokens = nltk.word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words and token not in string.punctuation]
    return tokens

def plot_most_common_words(text):
    tokens = preprocess_text(text)
    word_freq = nltk.FreqDist(tokens)
    most_common_words = word_freq.most_common(10)

    words, counts = zip(*most_common_words)

    plt.figure(figsize=(10, 6))
    plt.bar(words, counts)
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Most Common Words')
    plt.xticks(rotation=45)
    st.pyplot(plt)

def plot_repeated_words(text):
    tokens = preprocess_text(text)
    word_freq = nltk.FreqDist(tokens)
    repeated_words = [word for word, count in word_freq.items() if count > 1][:10]

    if repeated_words:
        words, counts = zip(*[(word, word_freq[word]) for word in repeated_words])

        plt.figure(figsize=(10, 6))
        plt.bar(words, counts)
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.title('Repeated Words')
        plt.xticks(rotation=45)
        st.pyplot(plt)
    else:
        st.write("No repeated words found.")

def calculate_perplexity(text, model):
    tokens = preprocess_text(text)
    padded_tokens = ['<s>'] + tokens + ['</s>']
    ngrams_sequence = list(ngrams(padded_tokens, model.order))
    perplexity = model.perplexity(ngrams_sequence)
    return perplexity

def calculate_burstiness(text):
    tokens = preprocess_text(text)
    word_freq = nltk.FreqDist(tokens)

    avg_freq = sum(word_freq.values()) / len(word_freq)
    variance = sum((freq - avg_freq) ** 2 for freq in word_freq.values()) / len(word_freq)

    burstiness_score = variance / (avg_freq ** 2)
    return burstiness_score

def is_generated_text(perplexity, burstiness_score):
    if perplexity < 100 and burstiness_score < 1:
        return "Likely generated by a language model"
    else:
        return "Not likely generated by a language model"

def main():
    st.title("Language Model Text Analysis")
    text = st.text_area("Enter the text you want to analyze", height=200)
    if st.button("Analyze"):
        if text:
            # Load or train your language model
            tokens = nltk.corpus.brown.words()  # Using the Brown corpus
            train_data, padded_vocab = padded_everygram_pipeline(1, tokens)
            model = MLE(1)  # Unigram model
            model.fit(train_data, padded_vocab)

            # Calculate perplexity
            perplexity = calculate_perplexity(text, model)
            st.write("Perplexity:", perplexity)

            # Calculate burstiness score
            burstiness_score = calculate_burstiness(text)
            st.write("Burstiness Score:", burstiness_score)

            # Check if text is likely generated by a language model
            generated_cue = is_generated_text(perplexity, burstiness_score)
            st.write("Text Analysis Result:", generated_cue)
            
            # Plot most common words
            plot_most_common_words(text)

            # Plot repeated words
            plot_repeated_words(text)
        else:
            st.warning("Please enter some text to analyze.")

if __name__ == "__main__":
    main()
