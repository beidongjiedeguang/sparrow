import streamlit as st
from io import StringIO
from queue import Queue
from collections import deque
from dataclasses import dataclass

if 'file_state' not in st.session_state:
    @dataclass
    class FileState:
        data: deque
        name: deque
        type: deque


    st.session_state['file_state'] = {"data": deque(maxlen=2), "name": deque(maxlen=2), "type": deque(maxlen=2)}

file_state = st.session_state['file_state']

uploaded_files = st.file_uploader("Choose file", accept_multiple_files=True)
print(uploaded_files)
if uploaded_files:
    # To read file as bytes:
    for uploaded_file in uploaded_files:
        file_state['data'].append(uploaded_file.getvalue())
        file_state['name'].append(uploaded_file.type)
        file_state['type'].append(uploaded_file.type)

        if "image/" in uploaded_file.type:
            st.image(uploaded_file)
        elif 'video' in uploaded_file.type:
            st.video(uploaded_file)

    # To convert to a string based IO:
    # stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    # st.write(stringio)
    #
    # # To read file as string:
    # string_data = stringio.read()
    # st.write(string_data)
    #
    # # Can be used wherever a "file-like" object is accepted:
    # dataframe = pd.read_csv(uploaded_file)
    # st.write(dataframe)

if file_state['name']:
    st.download_button('Download file', file_state['data'][-1],
                       mime=file_state['type'][-1],
                       # file_name=file_state['name'][-1]
                       )
