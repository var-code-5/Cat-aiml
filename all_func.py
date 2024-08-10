import re
import spacy
from organized1 import *
from testing import *
from dateutil import parser

from spacy.tokens import Token
from spacy.language import Language

nlp = spacy.load('en_core_web_lg')
sample_text = nlp(sample_text)

custom_colours = {"brown", "black", "grey", "yellow", "orange", "ash", "clean"}
Token.set_extension("colour", default="")

@Language.component('color_pos_tagger')
def color_pos_tagger(doc):
    for token in doc:
        if token.text.lower() in custom_colours:
            token._.colour = "COLOUR"
        else:
            token._.colour = token.pos_
    return doc
nlp.add_pipe('color_pos_tagger', before="tagger")

def find_number(span, identity_end):
    value = None
    for num_match in re.finditer(r'[0-9]+', span, re.I):
        if num_match.start() > identity_end:
            value = span[num_match.start():num_match.end()]
            return value
        else: value = None
    return value
        

# Function to extract numerical and condition-based values
# def extract_num_value(span, ctr):
#     value = None
#     # Look for numerical values
#     num_matches = re.findall(r'[0-9]+', span)
#     if num_matches:
#         value = num_matches[ctr]
#     else: value = None
#     return value

# Function to extract condition-based values
def negative_condition(span):
    condition_matches = re.findall(r'\b(low|needs replacement|bad|dirty|rust|worn)\b', span, re.I)
    if condition_matches:
        return condition_matches[0].capitalize()
    else: return "Not good"

# Checks if a metal piece is dented, rusted or is leaking
def other_condition_metal(span):
    condition_matches = re.findall(r'\b(rust|dent|damage|leak)\b', span, re.I)
    if condition_matches:
        return condition_matches[0].capitalize()
    else: return "No Damage"

# checks for the liquid level
def liquid_check(span):
    condition_matches = re.findall(r'\b(high|low|medium|okay)\b')
    if condition_matches:
        return condition_matches[0].capitalize()
    return None

# Function to assign condition based on sentiment analysis
def assign_condition(text: str):
    sentiment = sid.polarity_scores(text)['compound']
    
    if 0.2 <= sentiment:
        condition = "Excellent"
    elif 0.1 <= sentiment < 0.2:
        condition = "Good"
    elif sentiment < -0.1: 
        condition = negative_condition(text)
    else: condition = "Okay"
    
    return condition

# Function to extract the date from text
# def extract_date(text):
#     # Use dateutil's parser to find a date in the text
#     try:
#         date = parser.parse(text, fuzzy=True)
#         return date.strftime("%d-%B-%Y")
#     except ValueError:
#         return None
