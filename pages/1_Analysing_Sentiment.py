import random
import streamlit as st
import numpy as np
from functions.streamlit_page import get_config_interface, get_analysis_interface, get_result_interface, show_qr_code
from streamlit_autorefresh import st_autorefresh
import warnings
warnings.filterwarnings("ignore")

random.seed(0)
np.random.seed(0)


def main():
    if 'state' not in st.session_state.keys():
        st.session_state['state'] = 'user config'

    # ----------------------- Config -----------------------#
    if st.session_state['state'] == 'user config':
        df, uploaded_file, utterance_field = get_config_interface()
        show_qr_code()
        if df is not None:
            st.session_state['df'] = df
            st.session_state['uploaded_file'] = uploaded_file
            st.session_state['utterance_field'] = utterance_field

            st.session_state['state'] = 'analysis1'
            st_autorefresh()

    # ----------------------- Clear the page -----------------------#
    elif st.session_state['state'] == 'analysis1':
        st.write("")
        st.session_state['state'] = 'analysis'

        st_autorefresh()

    # ----------------------- Perform Analysis -----------------------#
    elif st.session_state['state'] == 'analysis':
        excel_buffer, df_count = get_analysis_interface()
        st.session_state['excel_buffer'] = excel_buffer
        st.session_state['df_count'] = df_count

        st.session_state['state'] = 'results'
        st_autorefresh()

    # ----------------------- Download the Resultss -----------------------#
    elif st.session_state['state'] == 'results':
        get_result_interface()
        show_qr_code()


if __name__ == "__main__":
    main()
