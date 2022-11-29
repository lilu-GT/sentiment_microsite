import streamlit as st
import pandas as pd
import io
import numpy as np
import pandas as pd
from datetime import datetime
from functions.aws_clients import s3_client, s3_bucket_name
from functions.prediction import predict_sentiments
from functions.preprocessing import preprocess_df
from PIL import Image


def get_config_interface():
    df = None
    df, uploaded_file, utterance_field = get_upload_file()

    st.text("")
    if st.button('▶️ Run Analysis'):

        if df is None:
            st.error("🚨 Please upload the feedback file")

        else:
            if utterance_field not in df.columns:
                st.error("Please fill in the correct column header name", icon="🚨")
            else:
                return df, uploaded_file, utterance_field

    return None, None, None


def get_analysis_interface():
    st.subheader('Generating the analysis:')
    st.warning(
        '⚠️ Please do not leave this page until the process has completed.')
    placeholder_sentiment = st.empty()
    placeholder_sentiment_progress_bar = st.empty()
    show_qr_code()

    df = st.session_state['df']
    utterance_field = st.session_state['utterance_field']
    uploaded_file = st.session_state['uploaded_file']

    # columns_in_file = df.columns.to_list()

    df_processed, df_empty_responses = preprocess_df(df=df,
                                                     text_field=utterance_field)

    # ----------------------- Sentiment Correction -----------------------#
    placeholder_sentiment.warning(
        '⌛ Please wait for the sentiment cleaning...')
    df_sentiment = predict_sentiments(df_processed, utterance_field,
                                      placeholder_sentiment_progress_bar)

    # df_count = pd.DataFrame(df_sentiment['Predicted sentiment'].value_counts())
    df_count = pd.DataFrame([('Positive', df_sentiment[df_sentiment['Predicted sentiment'] == 'Positive'].shape[0]),
                             ('Neutral',
                              df_sentiment[df_sentiment['Predicted sentiment'] == 'Neutral'].shape[0]),
                             ('Negative',
                              df_sentiment[df_sentiment['Predicted sentiment'] == 'Negative'].shape[0]),
                             ('Empty', df_empty_responses.shape[0]),
                             ('', ''),
                             ('Total', df_sentiment.shape[0])], columns=['Sentiment', 'Number of cases'])

    # ----------------------- Compile the results -----------------------#
    # Excel File
    df_result = pd.concat(
        [df_sentiment, df_empty_responses], axis=0, ignore_index=True)
    df_result = df_result.sort_values('Case index')
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer) as writer:
        df_result.to_excel(writer, index=False)
        # df_empty_responses.to_excel(
        #     writer, index=False, sheet_name='empty cases')

    # ----------------------- Upload to S3 -----------------------#
    results_filename = uploaded_file.name[:uploaded_file.name.rfind('.')] + '_results_' + \
        datetime.now().strftime("%Y_%m_%d_%H%M%S") + '.xlsx'
    response = s3_client.put_object(
        Bucket=s3_bucket_name, Key=results_filename, Body=excel_buffer.getvalue())
    # print status of uploading to s3
    status = response.get("ResponseMetadata",
                          {}).get("HTTPStatusCode")
    if status == 200:
        s3_status_message = f"Results successfully uploaded to S3. Status - {status}"
    else:
        s3_status_message = f"Uploading of results to S3 unsuccessful. Status - {status}"
    print('S3 Bucket message:' + s3_status_message)

    return excel_buffer, df_count


def get_result_interface():
    st.subheader('Results:')
    excel_buffer = st.session_state['excel_buffer']
    df_count = st.session_state['df_count']
    uploaded_file = st.session_state['uploaded_file']

    st.success('🎉 Done! Results have been generated.')

    st.text('')

    hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(df_count)

    st.text('')
    st.text('')

    st.download_button(
        label="📥 Download Results as Excel worksheets",
        data=excel_buffer.getvalue(),
        file_name=uploaded_file.name[:uploaded_file.name.rfind(
            '.')] + '_results' + '.xlsx',
        mime="application/vnd.ms-excel"
    )

    st.write("Please refresh the page to perform a new analysis.")

    return


def show_qr_code():
    st.text("")
    st.text("")
    st.text("")
    st.markdown("### Appreciate your feedback for improving this tool")
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
    return


def get_upload_file():
    # st.set_page_config(layout="wide")
    # Title
    st.title("GovText Tool for Sentiment Analysis")
    st.markdown("## Analysing Sentiment")

    st.text("")
    st.markdown("### Data preparation")
    st.write('''
    \nPlease prepare your data in a CSV or Excel spreadsheet before proceeding to the analysis. 
    \nThe text to be analysed should be arranged in one column and the column should have a header. Each row shall contain one case.
    ''')

    st.text("")

    # Description field
    st.text("")
    st.markdown("### Please copy the column header name of case description")
    utterance_field = st.text_input(
        "Column Header Name:", "").strip()

    # Upload
    st.text("")
    st.text("")
    st.markdown("### Please upload the file")
    uploaded_file = st.file_uploader(
        "", type=['csv', 'xls', 'xlsx'])

    df = None

    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        df['Case index'] = np.arange(1, df.shape[0] + 1)

    return df, uploaded_file, utterance_field
