from wordcloud import WordCloud, STOPWORDS
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import requests
import nltk
from nltk import FreqDist
from nltk.tokenize import RegexpTokenizer

class AiNames:

    most_common_limit = 20 #report the counts of the x most frequent words
    source_texts = [
        #url and css selector of HTML elements to get text from on that page
        ('https://developers.google.com/machine-learning/problem-framing/cases', '.devsite-article-body'),
        ('https://en.wikipedia.org/wiki/Artificial_intelligence','#content')
    ]

    def all_text(self):
        return " ".join(AiNames.main_page_text(source[0], source[1]) for source in self.source_texts)

    def all_text_tokens(self):
        tokenizer = RegexpTokenizer(r'\w+')#remove punctuation and anything not alphanumeric
        return tokenizer.tokenize(self.all_text())

    @staticmethod
    def main_page_text(url, css_selector):
        """
        Take a url of an html page, return the inner text of the element specified by css_selector
        """
        response = requests.get(url)
        parsed_html = bs(response.text, features='lxml')
        main_elements = parsed_html.select(css_selector)
        main_text = " ".join(element.getText() for element in main_elements)
        return main_text

    @staticmethod
    def display_wordcloud(text):
        """
        take frequency distribution of words and display graphical representation
        """
        wc = WordCloud(
            background_color='black',
            stopwords=set(STOPWORDS),
            max_words=200,
            max_font_size=40,
            scale=3,
            random_state=1
        ).generate(str(text.encode('ascii', 'ignore')))
        fig = plt.figure(1, figsize=(12,12))
        plt.axis('off')
        fig.suptitle("Ai Names", fontsize=20)
        #fig.subplots_adjust(top=2.3)
        plt.imshow(wc)
        plt.show()

if __name__ == "__main__":
    ainames = AiNames()
    all_tokens = ainames.all_text_tokens()
    useful_tokens = [word.lower() for word in all_tokens if word.lower() not in STOPWORDS]
    fd = FreqDist(useful_tokens)
    print(fd.most_common(ainames.most_common_limit))

    text = ainames.all_text()
    ainames.display_wordcloud(text)
