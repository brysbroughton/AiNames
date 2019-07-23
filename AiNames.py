from wordcloud import WordCloud, STOPWORDS
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import requests
import sys

def main_page_text(url, css_selector):
    """
    Take a url of an html page, return the inner text of the element specified by css_selector
    """
    response = requests.get(url)
    parsed_html = bs(response.text, features='lxml')
    main_elements = parsed_html.select(css_selector)
    main_text = " ".join(element.getText() for element in main_elements)
    return main_text

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
    #print(sys.argv)
    text = main_page_text(*sys.argv[1:])
    print(text)
    display_wordcloud(text)
