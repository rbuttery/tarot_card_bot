import openai
import random
import os
import json
import streamlit as st
from PIL import Image as PilImage
import time
import requests
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


@st.cache_data()
def get_cards():
    # Read the cards from the json file
    with open('./tarot_card_deck.json', 'r') as f:
        tarot_deck = json.loads(f.read())
    return tarot_deck


def to_color(text, color):
    color_text = "<span style='color:{}'>{}</span>".format(color, text)
    return color_text


def get_system_prompt():
    return """
You are a wise Tarot Card Reader with a mystical personality, answering questions with insights from the Tarot. 
"""

def shuffle_deck(tarot_deck):
    random.shuffle(tarot_deck)
    return tarot_deck
    

def draw_three_card_spread(tarot_deck):
    shuffle_deck([_ for _ in tarot_deck])

    past, present, future = random.sample([_ for _ in tarot_deck], 3)
    past_ori, present_ori, future_ori = [
        random.choice(["upright", "reversed"]) for _ in range(3)]

    return (past, tarot_deck[past], past_ori), (present, tarot_deck[present], present_ori), (future, tarot_deck[future], future_ori)


def get_tarot_reading(question, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": get_system_prompt()},
            {"role": "user", "content": question}
        ],
        max_tokens=250,
        temperature=0.96,
    )
    return response.choices[0].message["content"]

def get_card_image(card, scaling_factor=1, reversed=False):
    card = card.replace(" ", "_").lower()
    image_url = tarot_deck[card]["url"]
    response = requests.get(image_url)
    img = PilImage.open(BytesIO(response.content))
    
    if scaling_factor != 1:
        width, height = img.size
        new_dimensions = (int(width * scaling_factor), int(height * scaling_factor))
        img = img.resize(new_dimensions, PilImage.LANCZOS)

    if reversed:
        img = img.rotate(180)

    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    return img_bytes.getvalue()


def stream_typing(text, typing_speed=0.001):
    container = st.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        container.markdown(displayed_text, unsafe_allow_html=True)
        time.sleep(typing_speed)
        
st.set_page_config(layout="centered")

tarot_deck = get_cards()



st.markdown(
    """
    <div style='background-color: #FFC0CB; padding: 1rem; border-radius: 0.5rem;'>
        <h1 style='color: white; font-size: 3rem; text-align: center;'>
            Welcome to your mystical Tarot Card Reading!
        </h1>
        <h3 style='color: white; font-size: 2rem; text-align: center; margin-top: 1rem;'>
            Instructions:
        </h3>
        <p style='color: white; font-size: 1.5rem; text-align: center; margin-top: 1rem;'>
            In this reading, a 3-card spread will be used to provide insights into your past, present, and future. 
            Each card's meaning will be tailored to the topic or question you provide.
        </p>
        <p style='color: white; font-size: 1.5rem; text-align: center; margin-top: 1rem;'>
            Cards drawn in <span style='color: #FF6347;'>reversed</span> position represents blocked or repressed energies, 
            while <span style='color: #32CD32;'>upright</span> position represents clear and direct energies.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

question_topic = st.text_input(
    "What mystical inquiry or area of curiosity shall we delve into for your Tarot Card Reading?",
    key="question_topic",
)



# st.markdown(
#     f"# {to_color('**Welcome to your mystical Tarot Card Reading!**', 'pink')}", unsafe_allow_html=True)

# st.markdown(f"### {to_color('**Instructions:**','pink')}",
#             unsafe_allow_html=True)
# st.markdown(f"{to_color('*In this reading, a 3-card spread will be used to provide insights into your past, present, and future. Each cards meaning will be tailored to the topic or question you provide.*', 'pink')}", unsafe_allow_html=True)
# st.markdown(f"{to_color('Cards drawn in', 'pink')} {to_color('**reversed**','red')} {to_color('position represents blocked or repressed energies, while','pink')} {to_color('**upright**','green')}{to_color(': represents clear and direct energies.','pink')}", unsafe_allow_html=True)

# question_topic = st.text_input(
#     "What mystical inquiry or area of curiosity shall we delve into for your Tarot Card Reading?")

if st.button("Reveal Cards"):
    reader_intro = get_tarot_reading(
        f"The user has asked about \"{question_topic}\". Say something ominous to begin the reading, but do not expext an answer as the next message will be the terot reading results.")
    st.markdown(f"### {to_color('**Reading:**','orange')}",
                unsafe_allow_html=True)
    stream_typing(f'{reader_intro}')

    (past_card, tarot_deck[past_card], past_ori), (present_card, tarot_deck[present_card], present_ori), (
        future_card, tarot_deck[future_card], future_ori) = draw_three_card_spread(tarot_deck)

    past_card = past_card.replace("_", " ")
    tarot_question = f"The {past_card} card is drawn in the {past_ori} position for the past. What does it mean with respect to \"{question_topic}\"?"
    response_past = get_tarot_reading(tarot_question)
    past_color = "red" if "reversed" in response_past else "green"
    is_reversed = True if "reversed" in response_past else False
    past_ori = f'{past_ori[0].upper()}{past_ori[1:]}'
    st.markdown(
        f"\n### {to_color('Past Card', 'purple')}: {to_color(past_card, past_color)} in {to_color(past_ori, past_color)} position:", unsafe_allow_html=True)
    st.image(get_card_image(past_card, scaling_factor=0.5, reversed=is_reversed))
    stream_typing(f"{response_past}")

    present_card = present_card.replace("_", " ")
    tarot_question = f"The {present_card} card is drawn in the {present_ori} position for the present. What does it mean with respect to \"{question_topic}\"?"
    response_present = get_tarot_reading(tarot_question)
    present_color = "red" if "reversed" in response_present else "green"
    is_reversed = True if "reversed" in response_present else False
    present_ori = f'{present_ori[0].upper()}{present_ori[1:]}'
    st.markdown(f"\n### {to_color('Present Card', 'orange')}: {to_color(present_card, present_color)} in {to_color(present_ori, present_color)} position:", unsafe_allow_html=True)
    st.image(get_card_image(present_card,
             scaling_factor=0.5, reversed=is_reversed))
    stream_typing(f"{response_present}")

    future_card = future_card.replace("_", " ")
    tarot_question = f"The {future_card} card is drawn in the {future_ori} position for the future. What does it mean with respect to \"{question_topic}\"?"
    response_future = get_tarot_reading(tarot_question)
    future_color = "red" if "reversed" in response_future else "green"
    is_reversed = True if "reversed" in response_future else False
    st.markdown(f"\n### {to_color('Future Card', 'yellow')}: {to_color(future_card, future_color)} in {to_color(future_ori, future_color)} position:", unsafe_allow_html=True)
    st.image(get_card_image(future_card, scaling_factor=0.5, reversed=is_reversed))
    stream_typing(f"{response_future}")

    sys_out = get_tarot_reading(
        "<<SYSTEM MESSAGE>> The reading is complete. Thank the user for their time and say goodbye. <<END SYSTEM MESSAGE>>")
    st.markdown(f"\n## {to_color(f'{sys_out}', 'pink')}",
                unsafe_allow_html=True)
