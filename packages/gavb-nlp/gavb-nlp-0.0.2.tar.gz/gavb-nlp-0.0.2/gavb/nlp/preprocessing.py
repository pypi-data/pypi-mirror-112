from transformers import AutoModel, AutoTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import torch
import numpy as np
import re
import os
import spacy
import spacy.cli
from spacy.lang.pt.stop_words import STOP_WORDS

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
spacy.cli.download("pt_core_news_sm")


class TextProcessing(object):
    """
    Natural language processing class with built-in preprocessing steps having
    as output a text preprocessing and word embeddings.

    Parameters
    ----------

    save_dir: str
        path to save .txt files contained preprocessing steps
    language: str
        choose between "english" and "portuguese" languages
    nlp_object: pandas dataframe
        it gots a pandas dataframe contain a corpus
    column_name: str
        column name of texts where are keeps
    tokenization: boolean
        True or False for apply tokenization on text
    remove_punctuation: boolean
        True or False for remove punctuation on text
    remove_emoji: boolean
        True or False for remove emojis on text
    remove_blank_whitespace: boolean
        True or False for remove blank whitespaces on text
    lower_case: boolean
        True or False for apply lower case on text 
    replace_words: dict
        key-value dict for replace words to another words
    regex_expression: list
        first element a regex expression, second a value to will be replace
    remove_email: boolean
        True or False for remove email adress
    stop_words_type: str
        choose between "default" or "custom" default is a built-in stop words list
    custom_stop_words: list
        custom stop words list to will be removed on text
    lemmatization: boolean
        True or False for apply lemmatization on text 
    pos_tagger: boolean
        True or False for apply Part-of-speech tagger
    embedding: boolean
        True or False for apply BERT embedding on text



    Returns
    -------
    the object text processing class.


    """

    def __init__(self, save_dir=None, language=None, nlp_object=None, column_name=None, tokenization=None,
                 remove_punctuation=None,
                 remove_emoji=None,
                 remove_blank_whitespace=None,
                 lower_case=None,
                 replace_words=None, regex_expression=None,
                 remove_email=None,
                 stop_words_type=None,
                 custom_stop_words=None, lemmatization=None,
                 pos_tagger=None,
                 embedding=None):

        self.save_dir = save_dir
        self.language = language
        self.nlp_object = nlp_object
        self.column_name = column_name
        self.tokenization = tokenization
        self.remove_punctuation = remove_punctuation
        self.remove_emoji = remove_emoji
        self.remove_blank_whitespace = remove_blank_whitespace
        self.lower_case = lower_case
        self.replace_words = replace_words
        self.regex_expression = regex_expression
        self.remove_email = remove_email
        self.stop_words_type = stop_words_type
        self.custom_stop_words = custom_stop_words
        self.lemmatization = lemmatization
        self.pos_tagger = pos_tagger
        self.embedding = embedding

    def create_dir(self):

        """
        Make a directory to save text processing.

        
        Parameters
        ----------
        save_dir(__init__): str
            path to save .txt files contained preprocessing steps


        Returns
        -------
        None
            

        """

        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def clean_text(self, text):

        """
        Clean all text on dataframe across regex expressions and strings manipulations
        remove noisy on text.


        Parameters
        ----------
        text: str
            text to will be processing
        remove_punctuation(__init__): boolean
           True or False for remove punctuation on text
        remove_emoji: boolean
            True or False for remove emojis on text
        remove_blank_whitespace: boolean
            True or False for remove blank whitespaces on text
        lower_case: boolean
            True or False for apply lower case on text 
        replace_words: dict
            key-value dict for replace words to another words
        regex_expression: list
            first element a regex expression, second a value to will be replace
        remove_email: boolean
            True or False for remove email adress


        Returns
        --------
        A new cleaned text on string format.

        """

        # 1- remove punctuations
        if self.remove_punctuation:
            text_cleaned = re.sub(r'[^\w\s]', '', str(text))

        # 2- remove emoji
        if self.remove_emoji:
            emoji_pattern = re.compile("["
                                       u"\U0001F600-\U0001F64F"  # emoticons
                                       u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                       u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                       u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                       u"\U0001F1F2-\U0001F1F4"  # Macau flag
                                       u"\U0001F1E6-\U0001F1FF"  # flags
                                       u"\U0001F600-\U0001F64F"
                                       u"\U00002702-\U000027B0"
                                       u"\U000024C2-\U0001F251"
                                       u"\U0001f926-\U0001f937"
                                       u"\U0001F1F2"
                                       u"\U0001F1F4"
                                       u"\U0001F620"
                                       u"\u200d"
                                       u"\u2640-\u2642"
                                       "]+", flags=re.UNICODE)
            text = emoji_pattern.sub(r'', text_cleaned)

        # 3- remove blank whitespace (beginning and end of phrase)
        if self.remove_blank_whitespace:
            text = text.lower().strip()

        # 4- customize replace word
        if self.replace_words:
            temp = text.split()
            results = []
            for word in temp:
                results.append(self.replace_words.get(word, word))

            text = ' '.join(results)

        # 5- case normalization (lower case)
        if self.lower_case:
            text = "".join([i.lower() for i in text])

            # 6- customize regex expression
        if self.regex_expression:
            text = re.sub(self.regex_expression[0], self.regex_expression[1], text)

        # 7- remove e-mail address
        if self.remove_email:
            text = re.sub("\S+@\S+", " ", text)

        # 8 - remove noisy
        text = text.replace(",", "")
        text = text.replace("'", "")

        return text

    def clean_function(self):

        """
        Apply clean on text within dataframe format.

        Parameters 
        ----------

        save_dir(__init__): str
            path to save .txt files contained preprocessing steps
        nlp_object(__init__): pandas dataframe
            it gots a pandas dataframe contain a corpus
        column_name(__init__): str
            column name of texts where are keeps


        Returns
        -------
        None
        
        """

        self.nlp_object[self.column_name] = self.nlp_object[self.column_name].apply(lambda x: self.clean_text(x))
        text_cleaned = str(list(self.nlp_object[self.column_name]))
        with open(f'{self.save_dir}/text_cleaned.txt', 'w', encoding="utf-8") as f:
            f.writelines(text_cleaned)

    def tokenizer_with_stop_words(self):

        """
        Setup for apply Tokenization and Stop words both english and portuguese language
        on dataframe corpus.

        Parameters 
        ---------- 
        save_dir(__init__): str
            path to save .txt files contained preprocessing steps
        language(__init__): str
            choose between "english" and "portuguese" languages
        nlp_object(__init__): pandas dataframe
            it gots a pandas dataframe contain a corpus
        column_name(__init__): str
            column name of texts where are keeps
        tokenization(__init__): boolean
            True or False for apply tokenization on text
        stop_words_type(__init__): str
            choose between "default" or "custom" default is a built-in stop words list
        custom_stop_words(__init__): list
            custom stop words list to will be removed on text
        

        Returns
        -------
        None 

        """

        # English
        if self.tokenization:
            if self.language == "english":
                if self.stop_words_type == "default":
                    self.stop_words_list = set(stopwords.words('english'))
                    word_tokens = word_tokenize(str(list(self.nlp_object[self.column_name])))

                    self.filtered_sentence = [w for w in word_tokens if not w in self.stop_words_list]


            elif self.stop_words_type == "custom":
                self.stop_words_list = set(self.custom_stop_words)
                word_tokens = word_tokenize(str(list(self.nlp_object[self.column_name])))

                self.filtered_sentence = [w for w in word_tokens if not w in self.stop_words_list]

            # Portuguese
            if self.language == "portuguese":
                if self.stop_words_type == "default":
                    self.stop_words_list = STOP_WORDS
                    self.filtered_sentence = []
                    nlp = spacy.load("pt_core_news_sm")

                    for line in list(self.nlp_object[self.column_name]):
                        doc = nlp(str(line))
                        for token in doc:
                            if token.is_stop == False:
                                self.filtered_sentence.append(token.text)

                elif self.stop_words_type == "custom":
                    self.stop_words_list = set(self.custom_stop_words)
                    for line in list(self.nlp_object[self.column_name]):
                        for token in line:
                            if token not in self.stop_words_list:
                                self.filtered_sentence.append(token)

        with open(f'{self.save_dir}/tokenization.txt', 'w', encoding="utf-8") as f:
            f.write(str(self.filtered_sentence))

    def part_of_speech_tagger(self):

        """
        Filter Part of Speech (POS) on text, extract words and tags.
 

        Parameters 
        ---------- 
        save_dir(__init__): str
            path to save .txt files contained preprocessing steps
        language(__init__): str
            choose between "english" and "portuguese" languages
        nlp_object(__init__): pandas dataframe
            it gots a pandas dataframe contain a corpus
        column_name(__init__): str
            column name of texts where are keeps
        pos_tagger(__init__): boolean
            True or False for apply Part-of-speech tagger
        

        Returns
        -------
        None 

        """

        if self.pos_tagger:
            if self.language == "english":
                tagged = nltk.pos_tag(self.filtered_sentence)


            elif self.language == "portuguese":
                nlp = spacy.load("pt_core_news_sm")
                tagged = []
                for line in list(self.nlp_object[self.column_name]):
                    doc = nlp(str(line))
                    for token in doc:
                        tag = (token.text,)
                        tag += (token.tag_,)
                        tagged.append(tag)

        with open(f'{self.save_dir}/pos_tagged.txt', 'w', encoding="utf-8") as f:
            f.write(str(tagged))

    def lemmatization_apply(self):

        """
        Separete pairs of words and your lemmas, extract word lemma on text.
 

        Parameters 
        ---------- 
        save_dir(__init__): str
            path to save .txt files contained preprocessing steps
        language(__init__): str
            choose between "english" and "portuguese" languages
        nlp_object(__init__): pandas dataframe
            it gots a pandas dataframe contain a corpus
        column_name(__init__): str
            column name of texts where are keeps
        lemmatization: boolean
            True or False for apply lemmatization on text 
        

        Returns
        -------
        None 

        """

        if self.lemmatization:

            if self.language == "english":
                word_lemmatizer = WordNetLemmatizer()
                lemma_object = word_lemmatizer.lemmatize(str(self.filtered_sentence))


            elif self.language == "portuguese":
                nlp = spacy.load("pt_core_news_sm")
                lemma_object = []
                for line in list(self.nlp_object[self.column_name]):
                    doc = nlp(str(line))
                    for token in doc:
                        lemma_object.append(token.lemma_)

        with open(f'{self.save_dir}/lemmatization.txt', 'w', encoding="utf-8") as f:
            f.write(str(lemma_object))

    def bert_embedding(self, sentence):

        """
        Create a word embeddings from BERT architecture as a pre-trained model over text.
 

        Parameters 
        ---------- 
        language(__init__): str
            choose between "english" and "portuguese" languages
        embedding: boolean
            True or False for apply BERT embedding on text 
        

        Returns
        -------
        An embedding list

        """

        if self.language == "english":
            tokenizer_bert = AutoTokenizer.from_pretrained('bert-base-uncased')
            model_bert = AutoModel.from_pretrained('bert-base-uncased')
        elif self.language == "portuguese":
            tokenizer_bert = AutoTokenizer.from_pretrained('neuralmind/bert-large-portuguese-cased')
            model_bert = AutoModel.from_pretrained('neuralmind/bert-large-portuguese-cased')

        embedding_list = []
        for phrase in sentence:
            input_ids = tokenizer_bert.encode(phrase, return_tensors='pt')
            with torch.no_grad():
                outs = model_bert(input_ids)
                encoded = outs[0][0, 1:-1]
                encoded = np.array(encoded)
        embedding_list.append(encoded)

        return embedding_list

    def embedding_generate(self):

        """
        Generate word embeddings applying BERT method.
 

        Parameters 
        ---------- 
        save_dir(__init__): str
            path to save .txt files contained preprocessing steps
        language(__init__): str
            choose between "english" and "portuguese" languages
        nlp_object(__init__): pandas dataframe
            it gots a pandas dataframe contain a corpus
        column_name(__init__): str
            column name of texts where are keeps
        embedding: boolean
            True or False for apply BERT embedding on text 
        

        Returns
        -------
        None

        """

        if self.embedding:
            embeddings_list = []
            text_list = list(self.nlp_object[self.column_name])
            for line in text_list:
                if len(line) <= 512:
                    embeddings = self.bert_embedding(sentence=line)
                    embeddings_list.append(embeddings)

        with open(f'{self.save_dir}/embeddings.txt', 'w', encoding="utf-8") as f:
            f.write(str(embeddings_list))

    def run_pipeline(self):

        """
        Run all NLP pipeline on text. 


        Parameters
        ----------
        None 


        Returns
        --------
        A list with whole cleaned text.

        """

        self.create_dir()
        self.clean_function()
        self.tokenizer_with_stop_words()
        self.part_of_speech_tagger()
        self.lemmatization_apply()
        self.embedding_generate()
        print("pipeline execution done!")

        return list(self.nlp_object[self.column_name])
