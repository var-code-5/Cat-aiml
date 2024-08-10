from all_func import *

def each_outcome(sample_text):
    
    if re.search(r'\b(navigate|open|goto|go to)\b', sample_text.text, re.I) == None:
        outcomes = {}
        # Battery Section
        if re.search(r'battery', sample_text.text, re.I):
            
            if re.search(r'make', sample_text.text, re.I):
                for ent in sample_text.ents:
                    if str(ent.label_) == "ORG":
                        outcomes['Battery Make'] = ent.text
            
            if re.search(r'date', sample_text.text, re.I):
                
                try:
                    date = parser.parse(sample_text.text, fuzzy=True)
                    battery_date = date.strftime("%d-%B-%Y")
                except ValueError:
                    battery_date = None
                
                outcomes['Battery Replacement Date'] = battery_date

            voltage_search = re.search(r'voltage', sample_text.text, re.I)
            if voltage_search:
                outcomes['Battery Voltage'] = find_number(sample_text.text, voltage_search.end()) + " volts"

            if re.search(r'water', sample_text.text, re.I):
                outcomes['Battery Water Level'] = liquid_check(sample_text.text)
            
            if re.search(r'condition', sample_text.text, re.I):
                outcomes['Condition of Battery'] = assign_condition(sample_text.text)
                
                if outcomes['Condition of Battery'] in ['Good', 'Okay', 'Excellent']:
                    outcomes['Battery Leak/Rust'] = "No"
                else: outcomes['Batter Leak/Rust'] = "Yes, " + other_condition_metal(sample_text.text)


        # Tire Section
        if re.search(r'tire|tires', sample_text.text, re.I):
            non_sentiment_item = ["left front", "right front", "left rear", "right rear"]

            # word with sentiment
            if re.search(r'condition|conditions', sample_text.text, re.I):
                outcomes["Tire Condition"] = assign_condition(sample_text.text)

            # non sentiment words
            for position in non_sentiment_item:
                found_matches = re.search(position, sample_text.text, re.I)

                if found_matches:
                    found_text = sample_text.text[found_matches.start():found_matches.end()]
                    outcomes[position.title() + " Tire Pressure"] = find_number(sample_text.text, found_matches.end())
                else: 
                    outcomes[position.title() + " Tire Pressure"] = None

        # Exterior Section
        if re.search(r'exterior', sample_text.text, re.I):
            
            damaged_part = re.findall(r'\b(rust|dent|damage)\b', sample_text.text, re.I) 
            if len(damaged_part) != 0:
                damaged_part = list(set(damaged_part))
                damaged_part = ' '.join(damaged_part)
                outcomes['Exterior Rust/Dent/Damage'] = "No" if re.search(r"\b(no rust|isn't rusted|no damage|no dent|isn't dented|isn't damage)\b", sample_text.text, re.I) else "Yes, " + damaged_part
            else:
                outcomes['Exterior Rust/Dent/Damage'] = "No"

            outcomes['Oil Leak in Suspension'] = "No" if re.search(r"\b(no oil leak|no leak|isn't leak)\b", sample_text.text, re.I) else "Yes"

        # Engine Section
        if re.search(r'engine', sample_text.text, re.I):
                
            damaged_part = re.findall(r'\b(rust|dent|damage)\b', sample_text.text, re.I) 
            if len(damaged_part) != 0:
                damaged_part = list(set(damaged_part))
                damaged_part = ' '.join(damaged_part)
                outcomes['Engine Rust/Dent/Damage'] = "No" if re.search(r"\b(no rust|not rusted|isn't rusted|isn't dented|isn't damage|isn't rust)\b", sample_text.text, re.I) else "Yes, " + damaged_part
            else:
                outcomes['Engine Rust/Dent/Damage'] = "No"

            for token in sample_text:
                if token._.colour == "COLOUR":
                    outcomes['Engine Oil Colour'] = token.text
                    break
                else: outcomes['Engine Oil Colour'] = None
            
            if re.search(r'oil', sample_text.text, re.I):
                outcomes['Engine Oil condition'] = assign_condition(sample_text.text)
                outcomes['Any Oil Leak in Engine'] = "No" if outcomes['Engine Oil condition'] in ['Good', 'Okay', 'Excellent'] else "Yes"

        # Brake Section
        if re.search(r'brake', sample_text.text, re.I):
            if negative_condition(sample_text.text):
                outcomes['Brake Fluid Level'] = negative_condition(sample_text.text)  

    else:
        keywords = r'\b(tire|tires|battery|batteries|exterior|exteriors|brake|brakes|engine|engines|header)\b'
        outcomes = []

        for match in re.finditer(keywords, sample_text.text, re.I):
            outcomes.append(sample_text.text[match.start():match.end()])

        for i in range(0, len(outcomes)):
            word = outcomes[i]
            word = word[:-1] if word[-1].lower() == 's' else word
            outcomes[i] = word

        # returns the list of parts the user wants to see the info of
        outcomes = list(set(outcomes))

    return outcomes

print(each_outcome(sample_text))