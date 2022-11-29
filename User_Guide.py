import random
import streamlit as st
import numpy as np
from PIL import Image
import warnings
warnings.filterwarnings("ignore")

random.seed(0)
np.random.seed(0)


def main():
    st.title("GovText Tool for Sentiment Analysis")

    st.markdown("## User Guide")
    st.text("")

    st.markdown("### Introduction:")
    st.write("This is a GovText microsite which provides a trial version of a sentiment analysis tool. Sentiment analysis helps you identify sentiment in textual data. Using sentiment analysis tool, you can get a sentiment label (“Postive”, “Neutral” or “Negative”) and a confidence score for each piece of text description.")

    st.text("")

    st.markdown("### How to use:")
    st.write('''
    1. Prepare your data in a CSV or Excel spreadsheet. The text description should be arranged in one column and the column should have a header. Each row shall contain one piece of text description. For example, if you have a number of feedback cases, all the feedback case descriptions shall be arranged in the same column, and one case per row.

    \n2. Click on the tab **“Analysing Sentiment”** on the left menu of this page.

    \n3. Indicate the header name of the column to be analysed. Please note that the header name is case sensitive. 

    \n4. Upload your dataset by browsing your file or drag and drop your file.
    
    \n5. Click the “▶️ Run Analysis” button to generate the analysis.
    
    \n6. Wait for the results to be generated and click the 📥 download button to download the results to your computer.

    ''')

    st.text("")

    st.markdown("### How to interprete the results:")
    st.write('''
    Sentiment analysis returns the result file in excel format which is presented in three additional columns:
    \n    1. Case index:
    \n\tIndex is generated for each row according to the order in the original file.
    \n    2. Predicted sentiment:
    \n\tSentiment labels are identified based on the textual description in each row. Each row will be assigned with one of the three possible values of sentiments, namely “Postive”, “Neutral” or “Negative”.
    \n    3. Confidence score:
    \n\tConfidence scores range from 1 to 0. Scores closer to 1 indicate higher confidence in the predicted sentiment value, while lower scores indicate lower confidence.
    ''')

    st.text("")
    st.text("")

    st.markdown("### Your comment for this tool:")
    st.write('''
    You are cordially invited to provide your feedback after you tried out this clustering tool. Your feedback will help us further improve the tool.
    ''')
    st.write(
        "Appreciate your time for a simple survey [here](https://form.gov.sg/6361e6d5113c43001230071e) or by scanning the QR code below.")
    image = Image.open('QR_code.png')
    resize_image = image.resize((300, 300))
    st.image(resize_image)

    st.text("")
    st.text("")
    st.text("")

    st.write("Developed by GovText")
    st.write("Data Science and Artificial Intelligence Division, GovTech")


if __name__ == "__main__":
    main()
