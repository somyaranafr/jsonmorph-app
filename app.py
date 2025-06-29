import streamlit as st
import json
from jsonmorph import process_json

st.title("JSON Morphing")
st.divider()

if "pane" not in st.session_state:
    st.session_state.pane = 1

if "info" not in st.session_state:
    st.session_state.info = {}

def go_to_pane1():
    st.session_state.pane = 1

def go_to_pane2(input, settings, input_file, settings_file):
    if input_file:
        input = input_file.read()
    if settings_file:
        settings = settings_file.read()

    st.session_state.info["input"] = input
    st.session_state.info["settings"] = settings
    st.session_state.pane = 2
    st.rerun()

if st.session_state.pane == 1:
    with st.form(key="input_form"):
        st.subheader("Input your JSON")

        col1, col2 = st.columns(2)
        with col1:
            input = st.text_area("Enter Input JSON:", height=200)
            st.badge("OR")
            input_file = st.file_uploader("Upload your Input JSON File:")
            st.caption("This would contain the original JSON")

        with col2:
            settings = st.text_area("Enter Settings JSON:", height=200)
            st.badge("OR")
            settings_file = st.file_uploader("Upload your Settings JSON File:")
            st.caption("This would contain the defining configuration/settings JSON")

        submit_button = st.form_submit_button("Submit")

        input_given = input and input.strip() != ""
        settings_given = settings and settings.strip() != ""

        if submit_button:
            if (input_given or input_file) and (settings_given or settings_file):
                flag = False
                if input_given and input_file:
                    st.warning("Enter only **ONE** Input JSON | Text JSON **OR** File JSON")
                    flag = True
                if settings_given and settings_file:
                    st.warning("Enter only **ONE** Settings JSON | Text JSON **OR** File JSON")
                    flag = True
                elif not flag:
                    go_to_pane2(input,settings,input_file,settings_file)
            else:
                st.warning("Incomplete fields")


if st.session_state.pane == 2:
    with st.container(border=True):
        st.header("Morphed JSON")
        st.divider()

        try:
            input_json = json.loads(st.session_state.info.get('input',''))
            settings_json = json.loads(st.session_state.info.get('settings',''))

            with open("input.json",'w') as f:
                json.dump(input_json,f)

            with open("settings.json",'w') as f:
                json.dump(settings_json,f)

            output = process_json("input.json", "settings.json", "output.json")

            st.write("Output.json")
            st.json(output)

            st.divider()
            with open('output.json','r') as file:
                output_content = file.read()
                st.download_button("Download Output JSON", data=output_content, file_name="output.json")

        except Exception as e:
            st.error("Invalid JSON, Enter again")
        
        st.button("Back", on_click=go_to_pane1)