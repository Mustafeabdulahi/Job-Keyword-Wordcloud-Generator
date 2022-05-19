from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator  # Generate word clouds
from PIL import Image  # Load images
import pandas as pd 
import numpy as np  # Convert images to numbers
import re  # clean the user_text_put and remove none words char
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from collections import Counter  # Count the frequency of distinct strings
from gensim.parsing.preprocessing import remove_stopwords

# Streamline syntax ro create title, subtitle and text_input
st.sidebar.image('logo1.png', width=300)
# Add the expander to provide some information about the app
with st.sidebar.expander("About the App"):
    st.write("""
        This  Word cloud generator app is created by a group of inspiring data scientist and data analyst 
        as part of internship program for Data Career Jumpstart Bootcamp. The main purpose 
        of this app is to help job seekers to quickly generate and visualize key 
        words in a job description and know what words they should include in their resume.""")
st.title("Wordcloud Job Description Keyword Generator")  # set the title

text_input = st.text_input(" ").lower()  # get user input as string and turn it all lowercase

# create text input field and display it on sidebar
background_color = st.sidebar.text_input('Choose background color', value="white")

# Create number input field and display it on sidebar
height = int(st.sidebar.number_input('Choose height between 500 - 1000 pixels',
                                     value=640))
width = int(st.sidebar.number_input('Choose width between 500 - 1000 pixels',
                                    value=800))


# st.markdown(text_input)

# Create a function to remove none words in the job description
def text():
    pattern = r'\W+'  # return only words with in text
    # Split the text into a list of individual words
    word = re.split(pattern, text_input)
    return word


# join text with space
words = " ".join(text())
words_NST = remove_stopwords(words)

im_shape = st.sidebar.file_uploader("Upload your shape as an jpeg, image must have white backround (optional).", type='jpeg')
# Create a wordcloud generator
try:
    if im_shape is not None:
        image = Image.open(im_shape)  # Load the image from a file

        mask = np.array(image)  # Convert the image to a numeric representation

        # Create a wordcloud generator using Heart shape
        wordcloud = WordCloud(mask=mask, background_color=background_color).generate(words)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud)
        plt.xticks([])  # hide y tick marks from the graph
        plt.yticks([])  # hide y tick marks from the graph
        # plt.axis('off')
        st.pyplot(fig)
    else:
        # Create a wordcloud generator with defaults default arguments
        wordcloud = WordCloud(stopwords=STOPWORDS, background_color=background_color,
                              height=height, width=width).generate(words)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud)
        plt.xticks([])
        plt.yticks([])
        # plt.axis('off')
        st.pyplot(fig)
except ValueError:
    st.markdown("##### Copy & paste your job description in the box above & hit Enter!")  # set the sub header

check = st.checkbox('Graph Bar Chart')

if check and text_input:
    list_of_word = list((words_NST.split(" ")))
    #st.write(list_of_word)
    list_of_words = [word for word in list_of_word]
   # st.write(list_of_word)
    count = Counter(list_of_words)

    #st.write(count)

    list_of_words_df = pd.DataFrame(count.most_common(100), columns=["words", "word_count"])
    # st.write(list_of_words_df)
    # Plot horizontal bar graph
    list_of_words_df.sort_values(by='word_count')
    fig = px.bar(list_of_words_df, x="word_count", y="words",
        labels={'word_count':'Word Frequences'}, height=640,  width=1000)
    st.plotly_chart(fig)


