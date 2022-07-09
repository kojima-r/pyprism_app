import streamlit as st
import pyprism
from streamlit_chat import message
import os
import glob

st.set_page_config(page_title="PRISM demo", layout="wide")
st.title("PRISM demo") 
colA, colB = st.columns(2)
if 'program' not in st.session_state:
    st.session_state.program=""

with colA:
    placeholder_prog = st.empty()  # placeholder for latest message
    filelist=list(glob.glob("./exs/**/*.psm"))
    selected_exs = st.selectbox(
        'Example:',
        filelist)
    load_btn = st.button('Load Example')
    text=st.session_state.program
    with placeholder_prog.container():
        if load_btn == True and selected_exs is not None:
            fp=open(selected_exs)
            lines = fp.readlines()
            text="".join(lines)
        program=st.text_area("Program:", text, max_chars=None,height=300)
        #program=st.code("Input:", text, max_chars=None)
        st.session_state.program=text


def remove_opening_message(msg):
    out_arr=msg.split("\n")
    out_i=0
    for i, line in enumerate(out_arr):
        if line[:9]=="loading::":
            out_i=i
            break
    out_arr=out_arr[out_i+1:]
    bot_msg="\n".join(out_arr)
    return bot_msg,len(out_arr)


with colB:
    clr_btn = st.button('Clear')
    if clr_btn:
        st.session_state.history= []

    if 'history' not in st.session_state:
        st.session_state.history= []
        message_history=st.session_state.history
    else:
        message_history=st.session_state.history

        for i,msg in enumerate(message_history):
            #st.text_area("Log:", value=msg, max_chars=None, key="log"+str(i))
            text   =msg[0]
            length =msg[1]
            if length>30:
                length=30
            #st.text_area("Log:", text, height=length, max_chars=None)
            st.text_area("Log:", value=text, height=length*10, max_chars=None, key="log"+str(i))
        #    
    placeholder = st.empty()  # placeholder for latest message

    msg = st.text_input("Query:")
    if msg:
        o=pyprism.run("{}\n\nprism_main([]):-{}.".format(program,msg))
        out=str(o)
        
        bot_msg,length = remove_opening_message(out)
        message_history.append((msg+"\n"+bot_msg,length))

        with placeholder.container():
            text   =message_history[-1][0]
            length =message_history[-1][1]
            if length>30:
                length=30
            st.text_area("Log:", text, height=length*10, max_chars=None)
        #    message(message_history[-1]) # display the latest message

