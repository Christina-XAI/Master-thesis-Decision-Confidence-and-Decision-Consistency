from ast import Str
from asyncore import write
from operator import truediv
from random import Random, random
from time import strftime
from tkinter import Image
from tokenize import ContStr
from turtle import onclick
from typing import Sequence

import datetime
import csv
import streamlit as st
import pandas as pd
import numpy as np
import pickle as pkle
import os.path
from os.path import exists

# Horizontal radio buttons for the whole app.
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{padding-left:2px;}</style>', unsafe_allow_html=True)
st.markdown(
    """ <style>
            div[role="radiogroup"] >  :first-child{
                display: none !important;
            }
        </style>
   """,
unsafe_allow_html=True)

# Variables 
tempdata = {
    "gender": "None",
    "group": "None",
    "age":"None",
    "nationality":"None",
    "highest_degree_education":"None",
    "been_in_Berlin":[],
    "been_in_Hamburg":"None",
    "been_in_Jerusalem":"None",
    "been_to_Israel":"None",
    "been_in_TelAviv":"None",
    "ID_number": "None",
    "date":"None",
    "image_nr": 3,
    "Starting":1,
    "round_status": 1,
    "General":[],
    "history":[],
    "current_roundnumber": 0,
    "status": 0,
    "AI_round": 0,
    "user_guess":[],
    "user_guess_documentation":[],
    "sureness_user_guess":[],
    "sureness_user_guess_after_AI":[],
    "trust_in_AI":[],
    "Decision_reason":[],
    "Label_city":["Jerusalem", "Hamburg", "Tel Aviv", "Berlin", "Hamburg", "Tel Aviv", "Tel Aviv", "Berlin", "Jerusalem", "Hamburg", "Berlin", "Jerusalem"],
    "AI_guess":["Jerusalem","Berlin", "Tel Aviv", "Hamburg", "Hamburg", "Tel Aviv", "Tel Aviv", "Berlin", "Jerusalem", "Hamburg", "Berlin", "Jerusalem"]
    }

# Create file to collect general information and answers of this specific participant. 
filename = "tempdata.XAI"

if exists(filename): 
    with open(filename, "rb") as f: 
       tempdata = pkle.load(f)

# First questions to collect general information.
if tempdata["current_roundnumber"] == 0 and tempdata["status"] == 0: 
    ID_number = st.text_input('Please enter your anonym ID-number')
    tempdata["ID_number"] =ID_number
    tempdata["group"]=st.radio('Please enter your group', ["Choose an option",'AI', 'XAI'])
    tempdata["nationality"]=st.text_input('Please enter your nationality')
    tempdata["gender"]= st.selectbox('What best describes your gender?', ['Choose one','Male', 'Female', 'Other'])
    tempdata["age"]=st.number_input('What is your age?', 1, 100)
    tempdata["highest_degree_education"]=st.selectbox('What is the highest degree of education you have completed?', ['Choose one','Middle School', 'High School', 'Undergraduate Studies', 'Graduate Studies', 'Post-Graduate-Studies', 'Other', 'Prefer not to say'])
    
    tempdata["date"]=st.date_input("Today's date is: ", (datetime.date.today()))
    st.markdown('***')

    tempdata["been_in_Berlin"]=str(st.radio("Have you ever been in Berlin?", ["Choose an option","Yes", "No"]))
    st.markdown('')
    st.markdown('***')

    tempdata["been_in_Hamburg"]=st.radio("Have you ever been in Hamburg?", ["Choose an option",'Yes', 'No'])
    st.markdown('***')

    tempdata["been_in_Jerusalem"]=st.radio("Have you ever been in Jerusalem?", ["Choose an option",'Yes', 'No'])
    st.markdown('***')

    tempdata["been_in_TelAviv"]=st.radio("Have you ever been in Tel Aviv?", ["Choose an option",'Yes', 'No'])
    st.markdown('***')

    tempdata["been_to_Israel"]=st.radio("Have you ever been to Israel?", ["Choose an option",'Yes', 'No'])

    st.write('')
    st.write('**Please confirm that the data above is correct**')
    confirmation_button=st.button("I confirm!")
    if st.session_state.get('confirmation') != True:
        st.session_state['confirmation_button']=confirmation_button
    if st.session_state['confirmation_button']==True:
        tempdata["history"].append(tempdata["ID_number"])
        tempdata["history"].append(tempdata["group"])
        tempdata["history"].append(tempdata["gender"])
        tempdata["history"].append(tempdata["age"])
        tempdata["history"].append(tempdata["nationality"])
        tempdata["history"].append(tempdata["highest_degree_education"])
        tempdata["history"].append(tempdata["been_in_Berlin"])
        tempdata["history"].append(tempdata["been_in_Hamburg"])
        tempdata["history"].append(tempdata["been_in_Jerusalem"])
        tempdata["history"].append(tempdata["been_in_TelAviv"])
        tempdata["history"].append(tempdata["been_to_Israel"])
        tempdata["history"].append(tempdata["date"])
        tempdata["status"] =tempdata["Starting"]


# Introduction is displayed.
def Start():
    st.markdown('In the following you will see several Google Street View images. Each of them you will see **three times**.')
    st.markdown('On the **first** and the **third** times you will be asked to choose **one** of four cities where you think the image was taken. In addition, you will be asked to indicate your **confidence** in the correctness of your selection. \n\n The **second** time you see the image, the AI will state its guess, the explanation for its decision is shown. Furthermore, you will be asked to state your trust in the AI and whether you used in particular the same areas as the AI to form your decision.')
    starting_button=st.button("Let's start!")
    if st.session_state.get('Start') != True:
        st.session_state['starting_button']=starting_button
    if st.session_state['starting_button']==True:
        tempdata["status"]=(tempdata["Starting"] +1)
        tempdata["current_roundnumber"] +=1
        tempdata["AI_round"]=tempdata["Starting"]
        tempdata["round_status"]=tempdata["Starting"]

# Reset of the counting up variable so that the next round can be started.
def Reset():
        tempdata["status"]=(tempdata["Starting"] +1)
        tempdata["current_roundnumber"] +=1
        tempdata["AI_round"]=tempdata["Starting"]
        tempdata["round_status"]=tempdata["Starting"]

# Selection of the city and saving user's answer.
def selection_city():
    st.write('Your guess: Where has this Google Street View image been taken?')
    image=('Image {}.png'.format(str(tempdata["current_roundnumber"])))
    st.image(image, width=350)
    button_Tel_Aviv=st.button('Tel Aviv', key='Tel Aviv{rnumber}{rstatus}'.format(rnumber=(tempdata["current_roundnumber"]), rstatus=(tempdata["round_status"])))
    st.write()
    button_Jerusalem=st.button('Jerusalem', key='Jerusalem {rnumber}{rstatus}'.format(rnumber=(tempdata["current_roundnumber"]), rstatus=(tempdata["round_status"])))
    st.write()
    button_Berlin=st.button('Berlin', key='Berlin {rnumber}{rstatus}'.format(rnumber=(tempdata["current_roundnumber"]), rstatus=(tempdata["round_status"])))
    st.write()
    button_Hamburg=st.button('Hamburg', key='Hamburg {rnumber}{rstatus}'.format(rnumber=(tempdata["current_roundnumber"]), rstatus=(tempdata["round_status"])))
    if st.session_state.get('User_Guess') != True:
        st.session_state['button_Tel_Aviv'] = button_Tel_Aviv
        st.session_state['button_Jerusalem']=button_Jerusalem
        st.session_state['button_Berlin']=button_Berlin
        st.session_state['button_Hamburg']=button_Hamburg

    if st.session_state['button_Tel_Aviv']:
        tempdata["user_guess"].append('Tel Aviv')
        tempdata["user_guess_documentation"].append('Tel Aviv {rnumber}-{rstatus}'.format(rnumber=(tempdata["current_roundnumber"]), rstatus=(tempdata["round_status"])))
        tempdata["history"].append('Tel Aviv')
        tempdata["status"] += 1
    if st.session_state['button_Jerusalem']:
        tempdata["user_guess"].append('Jerusalem')
        tempdata["user_guess_documentation"].append('Jerusalem {rnumber}-{rstatus}'.format(rnumber=(tempdata["current_roundnumber"]), rstatus=(tempdata["round_status"])))
        tempdata["history"].append('Jerusalem')
        tempdata["status"] += 1
    if st.session_state['button_Berlin']:
        tempdata["user_guess"].append('Berlin')
        tempdata["user_guess_documentation"].append('Berlin {rnumber}-{rstatus}'.format(rnumber=(tempdata["current_roundnumber"]), rstatus=(tempdata["round_status"])))
        tempdata["history"].append('Berlin')
        tempdata["status"] += 1
    if st.session_state['button_Hamburg']:
        tempdata["user_guess"].append('Hamburg')
        tempdata["user_guess_documentation"].append('Hamburg {rnumber}-{rstatus}'.format(rnumber=(tempdata["current_roundnumber"]), rstatus=(tempdata["round_status"])))
        tempdata["history"].append('Hamburg')
        tempdata["status"] += 1

    # Saving collected data.
    with open(filename, "wb") as f: 
        pkle.dump(tempdata, f, pkle.HIGHEST_PROTOCOL)

    #st.write(tempdata)

# User's last city-guess is displayed.      
def show_selection():
    st.markdown("_Your guess is: **{user_guess}**._".format(user_guess=str(tempdata["user_guess"][-1])))
    tempdata["status"] += 1
    with open(filename, "wb") as f: 
        pkle.dump(tempdata, f, pkle.HIGHEST_PROTOCOL)

# Asking for user's confidence in the last city-selection.
def state_confidence():
    user_sureness1=st.radio("Please enter your confidence in your last decision. (1=no confidence; 5=full confidence)", ('not yet selected', '1', '2', '3','4', '5'), key='Confidence1{rnumber}{rstatus}'.format(rnumber=(tempdata["current_roundnumber"]), rstatus=(tempdata["round_status"])))
    tempdata["sureness_user_guess"].append(user_sureness1)
    #st.write(tempdata)


# If the user choosed a number of the confidence scale, the variable "AI_round" is counted up.
    if tempdata["sureness_user_guess"][-1] != 'not yet selected' and tempdata["status"]==5 and tempdata["round_status"]==1:
        st.write('##')
        tempdata["history"].append(tempdata["sureness_user_guess"][-1])
        button_ask_AI=st.button("What do you guess, AI?")
        tempdata["AI_round"] =2

# Asking for user's confidence after the AI stated its guess and the explanation was shown, so at the third time seeing the image.
def state_confidence_after_AI():
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{padding-left:2px;}</style>', unsafe_allow_html=True)
    st.markdown(
    """ <style>
            div[role="radiogroup"] >  :first-child{
                display: none !important;
            }
        </style>
        """,
    unsafe_allow_html=True)
    user_sureness2=st.radio("Please enter your confidence in your last decision. (1=no confidence; 5=full confidence)", ('not yet selected', '1', '2', '3','4', '5'), key='Confidence2{rnumber}{rstatus}'.format(rnumber=(tempdata["current_roundnumber"]), rstatus=(tempdata["round_status"])))
    tempdata["sureness_user_guess_after_AI"].append(user_sureness2)
    with open(filename, "wb") as f: 
        pkle.dump(tempdata, f, pkle.HIGHEST_PROTOCOL)

    if tempdata["sureness_user_guess_after_AI"][-1] != 'not yet selected' and tempdata["round_status"]==2:
        tempdata["history"].append(tempdata["sureness_user_guess_after_AI"][-1])
    with open(filename, "wb") as f: 
        pkle.dump(tempdata, f, pkle.HIGHEST_PROTOCOL)

# The second time the user sees the image. AI's guess and the explanation are shown. The user is asked for his trust in the AI and whether he used in particular the same areas of the picture as the AI.
def ask_AI():
    image=('Image {}.png'.format(str(tempdata["current_roundnumber"])))
    st.image(image, width=350)
    st.markdown('My guess is **{AI_guess}**.'. format(AI_guess=str(tempdata["AI_guess"][tempdata["current_roundnumber"]-1])))
    st.write('In particular, the colored areas below have helped me form my guess.')
    image_XAI=('Image-XAI-{}.png'.format(str(tempdata["current_roundnumber"])))
    st.image(image_XAI, width=350)
    st.markdown('')
    st.markdown('**Please indicate the extent to which you agree with each of the following statements.**')
    trust_AI=st.radio("I trust this AI to assess the correct city. (1=strongly disagree, 5=Strongly agree)", ('not yet selected', '1', '2', '3', '4', '5'), key='Trust_AI{rnumber}{rstatus}'.format(rnumber=(tempdata["current_roundnumber"]), rstatus=(tempdata["round_status"])))
    tempdata["trust_in_AI"].append(trust_AI)
    st.write()
    Decision_reason=st.radio("I also based my decision in particular on the colored areas.", ('not yet selected', 'Yes', 'No'), key='Decision_reason{rnumber}{rstatus}'.format(rnumber=(tempdata["current_roundnumber"]), rstatus=(tempdata["round_status"])))
    tempdata["Decision_reason"].append(Decision_reason)
    with open(filename, "wb") as f: 
        pkle.dump(tempdata, f, pkle.HIGHEST_PROTOCOL)
    if tempdata["trust_in_AI"][-1] != 'not yet selected' and tempdata["Decision_reason"][-1] != 'not yet selected':
        tempdata["history"].append(tempdata["trust_in_AI"][-1])
        tempdata["history"].append(tempdata["Decision_reason"][-1])
        tempdata["status"] +=1
        tempdata["round_status"]=2

    with open(filename, "wb") as f: 
        pkle.dump(tempdata, f, pkle.HIGHEST_PROTOCOL)

# Attention check. In this round, the user guesses only one time. 
if tempdata["current_roundnumber"] == 13 and tempdata["status"]==2 and tempdata["round_status"]==1: 
    st.markdown('')
    st.header("First Time")
    selection_city()


# User is thanked for participation. Collected Data is saved.
#'''For selection (Sel), trust, confidence (Conf), decision reason (Dec-R) applies: First number is the round number, the second number indicates whether it was chosed before (1) or after (2) seeing AI's advice. Thus, 11-1-Sel refers to the eleventh round (11) before seeing AI's advice (1).'''
if tempdata["current_roundnumber"]==13 and tempdata["status"]>=3 and tempdata["round_status"]==1:
    st.write("Thank you very much for your participation!")
    st.info('This app was developed on the basis of a research project at the University of Ulm.', icon="ℹ️")
    fields=['ID-Number', 'Group', 'Gender', 'Age', 'Nationality', 'Highest degree of education', 'Been Berlin', 'Been Hamburg', 'Been Israel', 'Been TelAviv', 'Been Jerusalem',  'been Israel', 'Date','1-1-Sel', '1-1-Conf', '1-2-Trust', '1-2-Dec-R', '1-2-Sel', '1-2-Conf', '2-1-Sel', '2-1-Conf', '2-2-Trust', '2-2-Dec-R', '2-2-Sel', '2-2-Conf', '3-1-Sel', '3-1-Conf', '3-2-Trust', '3-2-Dec-R', '3-2-Sel', '3-2-Conf', '4-1-Sel', '4-1-Conf', '4-2-Trust', '4-2-Dec-R', '4-2-Sel', '4-2-Conf','5-1-Sel', '5-1-Conf', '5-2-Trust', '5-2-Dec-R', '5-2-Sel', '5-2-Conf','6-1-Sel', '6-1-Conf', '6-2-Trust', '6-2-Dec-R', '6-2-Sel', '6-2-Conf','7-1-Sel', '7-1-Conf', '7-2-Trust', '7-2-Dec-R', '7-2-Sel', '7-2-Conf','8-1-Sel', '8-1-Conf', '8-2-Trust', '8-2-Dec-R', '8-2-Sel', '8-2-Conf','9-1-Sel', '9-1-Conf', '9-2-Trust', '9-2-Dec-R', '9-2-Sel', '9-2-Conf','10-1-Sel', '10-1-Conf', '10-2-Trust', '10-2-Dec-R', '10-2-Sel', '11-2-Conf','11-1-Sel', '11-1-Conf', '11-2-Trust', '11-2-Dec-R', '11-2-Sel', '11-2-Conf','12-1-Sel', '12-1-Conf', '12-2-Trust', '12-2-Dec-R', '12-2-Sel', '12-2-Conf','13-1-Sel']
    rows=[tempdata["history"]]
    with open('XAI_results', 'w') as f:
      
    # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)
    #st.write(tempdata)

# Twelve rounds: order of function calls and showing the headers
if tempdata["current_roundnumber"]==0 and tempdata["status"]==1:
    st.header("Introduction")
    Start()

if 13>tempdata["current_roundnumber"]>=1 and tempdata["status"]>=2 and tempdata["round_status"]==1:
    st.title("Guess the City")
    st.header("Round " +str(tempdata["current_roundnumber"]) +" - First Time")
    selection_city()

if 13>tempdata["current_roundnumber"]>=1 and tempdata["status"]>=3 and tempdata["round_status"]==1:
    show_selection()

if 13>tempdata["current_roundnumber"]>=1 and tempdata["status"]>=4 and tempdata["round_status"]==1:
    state_confidence()

if 13>tempdata["current_roundnumber"]>=1 and tempdata["status"]>=6 and tempdata["AI_round"]==2:
    st.markdown('')
    st.header("AI - Second Time")
    ask_AI()

if 13>tempdata["current_roundnumber"]>=1 and tempdata["status"]>=7 and tempdata["round_status"]==2:
    st.markdown('')
    st.header("Third Time")
    st.write("")
    selection_city()
    tempdata["AI_round"]=1
   

if 13>tempdata["current_roundnumber"]>=1 and tempdata["status"]>=10 and tempdata["round_status"]==2:
    show_selection() 
    
if 13>tempdata["current_roundnumber"]>=1 and tempdata["status"]>=11 and tempdata["round_status"]==2:    
    state_confidence_after_AI()

if 13>tempdata["current_roundnumber"]>=1 and tempdata["status"]>=12 and tempdata["round_status"]==2:
    next_round=st.button('Next round', key='next_', on_click=Reset())

with open(filename, "wb") as f: 
    pkle.dump(tempdata, f, pkle.HIGHEST_PROTOCOL)
    

with open(filename, "wb") as f: 
    pkle.dump(tempdata, f, pkle.HIGHEST_PROTOCOL)
