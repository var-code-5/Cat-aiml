inspection_form = {
    "TIRE": {
        "Left Front Tire Pressure": None,
        "Right Front Tire Pressure": None,
        "Left Rear Tire Pressure": None,
        "Right Rear Tire Pressure": None,
        "Tire Condition": None,
        "Overall Tire Summary": None,
        "Attached Images": None
    },
    "BATTERY": {
        "Battery Make": None,
        "Battery Replacement Date": None,
        "Battery Voltage": None,
        "Battery Water Level": None,
        "Condition of Battery": None,
        "Battery Leak/Rust": None,
        "Battery Overall Summary": None,
        "Attached Images": None
    },
    "EXTERIOR": {
        "Exterior Rust/Dent/Damage": None,
        "Oil Leak in Suspension": None,
        "Overall Exterior Summary": None,
        "Attached Images": None
    },
    "BRAKE": {
        "Brake Fluid Level": None,
        "Front Brake Condition": None,
        "Rear Brake Condition": None,
        "Emergency Brake Condition": None,
        "Overall Brake Summary": None,
        "Attached Images": None
    },
    "ENGINE": {
        "Rust/Dents/Damage in Engine": None,
        "Engine Oil Condition": None,
        "Engine Oil Color": None,
        "Brake Fluid Condition": None,
        "Brake Fluid Color": None,
        "Oil Leak in Engine": None,
        "Overall Engine Summary": None,
        "Attached Images": None
    }
}

from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

custom_words = {
    'worn': -0.24,
    'dent': -0.12,
    'rust': -0.35,
    'leak': -2.0,
    'damage': -2.0,
    'good': 1.4,
    'excellent': 2.0,
    'new': 1.2,
    'clean': 1.5,
    'smooth': 1.5,
}
sid.lexicon.update(custom_words)