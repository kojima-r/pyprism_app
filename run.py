import streamlit as st
import pyprism
from streamlit_chat import message

st.title("PRISM demo") 
colA, colB = st.columns(2)
program=""
with colA:
    program=st.text_area("Input:", "", max_chars=None)

with colB:
    if 'history' not in st.session_state:
        st.session_state.history= []
        message_history=st.session_state.history
    else:
        message_history=st.session_state.history

        for i,msg in enumerate(message_history):
            st.text_area("Bot:", value=msg, max_chars=None, key="bot"+str(i))

    def remove_opening_message(msg):
        out_arr=msg.split("\n")
        out_i=0
        for i, line in enumerate(out_arr):
            if line[:9]=="loading::":
                out_i=i
                break
        bot_msg="\n".join(out_arr[out_i+1:])
        return bot_msg

    placeholder = st.empty()  # placeholder for latest message

    msg = st.text_input("you:")
    if msg:
        print(msg)
        o=pyprism.run("{}\n\nprism_main([]):-{}.".format(program,msg))
        out=str(o.stdout.decode("utf-8"))
        
        bot_msg = remove_opening_message(out)
        message_history.append(msg+"\n"+bot_msg)

        with placeholder.container():
            st.text_area("Bot:", message_history[-1], max_chars=None)
        #    message(message_history[-1]) # display the latest message
