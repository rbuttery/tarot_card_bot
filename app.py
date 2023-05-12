import openai
import random
import os
import streamlit as st
from PIL import Image as PilImage
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

tarot_deck = {'Fool': {'number': '0',
  'arcana': 'Major',
  'meaning': 'Beginnings, innocence, spontaneity, free spirit.'},
 'Magician': {'number': '1',
  'arcana': 'Major',
  'meaning': 'Manifestation, self-confidence, action, skill.'},
 'High_Priestess': {'number': '2',
  'arcana': 'Major',
  'meaning': 'Intuition, secrets, mystery, subconsciousness.'},
 'Empress': {'number': '3',
  'arcana': 'Major',
  'meaning': 'Fertility, abundance, nurturing, comfort.'},
 'Emperor': {'number': '4',
  'arcana': 'Major',
  'meaning': 'Authority, structure, stability, protection.'},
 'Hierophant': {'number': '5',
  'arcana': 'Major',
  'meaning': 'Tradition, spirituality, religion, belief system.'},
 'Lovers': {'number': '6',
  'arcana': 'Major',
  'meaning': 'Love, relationships, duality, harmony.'},
 'Chariot': {'number': '7',
  'arcana': 'Major',
  'meaning': 'Control, willpower, determination, victory.'},
 'Strength': {'number': '8',
  'arcana': 'Major',
  'meaning': 'Inner strength, courage, perseverance, compassion.'},
 'Hermit': {'number': '9',
  'arcana': 'Major',
  'meaning': 'Solitude, introspection, wisdom, inner guidance.'},
 'Wheel_of_Fortune': {'number': '10',
  'arcana': 'Major',
  'meaning': 'Change, cycles, fate, opportunities.'},
 'Justice': {'number': '11',
  'arcana': 'Major',
  'meaning': 'Balance, reason, truth, fairness.'},
 'Hanged_Man': {'number': '12',
  'arcana': 'Major',
  'meaning': 'Sacrifice, surrender, letting go, new perspective.'},
 'Death': {'number': '13',
  'arcana': 'Major',
  'meaning': 'Transformation, endings, rebirth, change.'},
 'Temperance': {'number': '14',
  'arcana': 'Major',
  'meaning': 'Balance, moderation, harmony, self-control.'},
 'Devil': {'number': '15',
  'arcana': 'Major',
  'meaning': 'Materialism, temptation, addiction, bondage.'},
 'Tower': {'number': '16',
  'arcana': 'Major',
  'meaning': 'Destruction, upheaval, revelation, awakening.'},
 'Star': {'number': '17',
  'arcana': 'Major',
  'meaning': 'Hope, inspiration, positivity, faith.'},
 'Moon': {'number': '18',
  'arcana': 'Major',
  'meaning': 'Illusion, intuition, hidden truths, subconsciousness.'},
 'Sun': {'number': '19',
  'arcana': 'Major',
  'meaning': 'Success, positivity, vitality, warmth.'},
 'Judgment': {'number': '20',
  'arcana': 'Major',
  'meaning': 'Rebirth, renewal, awakening, judgment.'},
 'World': {'number': '21',
  'arcana': 'Major',
  'meaning': 'Completion, wholeness, unity, integration.'},
 'Ace_of_Wands': {'number': '1',
  'arcana': 'Minor',
  'meaning': 'Inspiration, motivation, new beginnings.'},
 'Two_of_Wands': {'number': '2',
  'arcana': 'Minor',
  'meaning': 'Planning, progress, decisions.'},
 'Three_of_Wands': {'number': '3',
  'arcana': 'Minor',
  'meaning': 'Expansion, growth, opportunity.'},
 'Four_of_Wands': {'number': '4',
  'arcana': 'Minor',
  'meaning': 'Celebration, harmony, home, community.'},
 'Five_of_Wands': {'number': '5',
  'arcana': 'Minor',
  'meaning': 'Conflict, competition, struggle.'},
 'Six_of_Wands': {'number': '6',
  'arcana': 'Minor',
  'meaning': 'Victory, recognition, achievement.'},
 'Seven_of_Wands': {'number': '7',
  'arcana': 'Minor',
  'meaning': 'Challenge, perseverance, defense.'},
 'Eight_of_Wands': {'number': '8',
  'arcana': 'Minor',
  'meaning': 'Movement, speed, progress.'},
 'Nine_of_Wands': {'number': '9',
  'arcana': 'Minor',
  'meaning': 'Resilience, persistence, courage.'},
 'Ten_of_Wands': {'number': '10',
  'arcana': 'Minor',
  'meaning': 'Burden, responsibility, exhaustion.'},
 'Page_of_Wands': {'number': '11',
  'arcana': 'Minor',
  'meaning': 'Creativity, curiosity, learning.'},
 'Knight_of_Wands': {'number': '12',
  'arcana': 'Minor',
  'meaning': 'Adventure, impulsiveness, energy.'},
 'Queen_of_Wands': {'number': '13',
  'arcana': 'Minor',
  'meaning': 'Confidence, independence, passion.'},
 'King_of_Wands': {'number': '14',
  'arcana': 'Minor',
  'meaning': 'Leadership, influence, vision.'},
 'Ace_of_Cups': {'number': '1',
  'arcana': 'Minor',
  'meaning': 'Emotions, new relationships, love.'},
 'Two_of_Cups': {'number': '2',
  'arcana': 'Minor',
  'meaning': 'Connection, partnership, union.'},
 'Three_of_Cups': {'number': '3',
  'arcana': 'Minor',
  'meaning': 'Celebration, friendship, community.'},
 'Four_of_Cups': {'number': '4',
  'arcana': 'Minor',
  'meaning': 'Apathy, boredom, contemplation.'},
 'Five_of_Cups': {'number': '5',
  'arcana': 'Minor',
  'meaning': 'Loss, disappointment, grief.'},
 'Six_of_Cups': {'number': '6',
  'arcana': 'Minor',
  'meaning': 'Nostalgia, memories, childhood.'},
 'Seven_of_Cups': {'number': '7',
  'arcana': 'Minor',
  'meaning': 'Choices, decisions, illusions.'},
 'Eight_of_Cups': {'number': '8',
  'arcana': 'Minor',
  'meaning': 'Leaving, moving on, transition.'},
 'Nine_of_Cups': {'number': '9',
  'arcana': 'Minor',
  'meaning': 'Satisfaction, happiness, indulgence.'},
 'Ten_of_Cups': {'number': '10',
  'arcana': 'Minor',
  'meaning': 'Harmony, family, emotional fulfillment.'},
 'Page_of_Cups': {'number': '11',
  'arcana': 'Minor',
  'meaning': 'Creativity, intuition, emotions.'},
 'Knight_of_Cups': {'number': '12',
  'arcana': 'Minor',
  'meaning': 'Romantic, idealistic, dreamy.'},
 'Queen_of_Cups': {'number': '13',
  'arcana': 'Minor',
  'meaning': 'Empathy, intuition, nurturing.'},
 'King_of_Cups': {'number': '14',
  'arcana': 'Minor',
  'meaning': 'Compassion, emotional balance, diplomacy.'},
 'Ace_of_Swords': {'number': '1',
  'arcana': 'Minor',
  'meaning': 'Mental clarity, new ideas, communication.'},
 'Two_of_Swords': {'number': '2',
  'arcana': 'Minor',
  'meaning': 'Stalemate, indecision, conflicting interests.'},
 'Three_of_Swords': {'number': '3',
  'arcana': 'Minor',
  'meaning': 'Heartbreak, betrayal, sadness.'},
 'Four_of_Swords': {'number': '4',
  'arcana': 'Minor',
  'meaning': 'Rest, recuperation, meditation, solitude.'},
 'Five_of_Swords': {'number': '5',
  'arcana': 'Minor',
  'meaning': 'Conflict, defeat, humiliation.'},
 'Six_of_Swords': {'number': '6',
  'arcana': 'Minor',
  'meaning': 'Moving on, transition, clarity.'},
 'Seven_of_Swords': {'number': '7',
  'arcana': 'Minor',
  'meaning': 'Deception, strategy, sneaking around.'},
 'Eight_of_Swords': {'number': '8',
  'arcana': 'Minor',
  'meaning': 'Restriction, isolation, self-imposed limitations.'},
 'Nine_of_Swords': {'number': '9',
  'arcana': 'Minor',
  'meaning': 'Anxiety, worry, nightmares.'},
 'Ten_of_Swords': {'number': '10',
  'arcana': 'Minor',
  'meaning': 'Endings, betrayal, pain, loss.'},
 'Page_of_Swords': {'number': '11',
  'arcana': 'Minor',
  'meaning': 'New information, curiosity, communication.'},
 'Knight_of_Swords': {'number': '12',
  'arcana': 'Minor',
  'meaning': 'Action, assertiveness, impulsiveness.'},
 'Queen_of_Swords': {'number': '13',
  'arcana': 'Minor',
  'meaning': 'Intelligence, independence, strength.'},
 'Ace_of_Pentacles': {'number': '1',
  'arcana': 'Minor',
  'meaning': 'Manifestation, financial opportunity, new beginnings.'},
 'Two_of_Pentacles': {'number': '2',
  'arcana': 'Minor',
  'meaning': 'Balance, adaptability, time management.'},
 'Three_of_Pentacles': {'number': '3',
  'arcana': 'Minor',
  'meaning': 'Collaboration, teamwork, craftsmanship.'},
 'Four_of_Pentacles': {'number': '4',
  'arcana': 'Minor',
  'meaning': 'Security, control, stability.'},
 'Five_of_Pentacles': {'number': '5',
  'arcana': 'Minor',
  'meaning': 'Poverty, isolation, insecurity.'},
 'Six_of_Pentacles': {'number': '6',
  'arcana': 'Minor',
  'meaning': 'Generosity, charity, abundance.'},
 'Seven_of_Pentacles': {'number': '7',
  'arcana': 'Minor',
  'meaning': 'Patience, persistence, long-term success.'},
 'Eight_of_Pentacles': {'number': '8',
  'arcana': 'Minor',
  'meaning': 'Skill, craftsmanship, diligence.'},
 'Nine_of_Pentacles': {'number': '9',
  'arcana': 'Minor',
  'meaning': 'Luxury, comfort, abundance.'},
 'Ten_of_Pentacles': {'number': '10',
  'arcana': 'Minor',
  'meaning': 'Legacy, wealth, family, security.'},
 'Page_of_Pentacles': {'number': '11',
  'arcana': 'Minor',
  'meaning': 'New opportunities, growth, learning.'},
 'Knight_of_Pentacles': {'number': '12',
  'arcana': 'Minor',
  'meaning': 'Patience, dedication, hard work.'},
 'Queen_of_Pentacles': {'number': '13',
  'arcana': 'Minor',
  'meaning': 'Nurturing, abundance, practicality.'},
 'King_of_Pentacles': {'number': '14',
  'arcana': 'Minor',
  'meaning': 'Security, stability, wealth.'}}

def to_color(text, color):
    color_text = "<span style='color:{}'>{}</span>".format(color, text)
    return color_text

def get_system_prompt():
    return """
You are a wise Tarot Card Reader with a mystical personality, answering questions with insights from the Tarot. 
"""

def draw_three_card_spread(tarot_deck):
    shuffle_deck([_ for _ in tarot_deck])

    past, present, future = random.sample([_ for _ in tarot_deck], 3)
    past_ori, present_ori, future_ori = [random.choice(["upright", "reversed"]) for _ in range(3)]

    return (past, tarot_deck[past], past_ori), (present, tarot_deck[present], present_ori), (future, tarot_deck[future], future_ori)

def shuffle_deck(tarot_deck):
    random.shuffle(tarot_deck)

def get_tarot_reading(question, model = "gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model= model,
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
    image_path = f'./images/tarot_cards/{card}.png'
    img = PilImage.open(image_path)
    
    if scaling_factor != 1:
        width, height = img.size
        new_dimensions = (int(width * scaling_factor), int(height * scaling_factor))
        img = img.resize(new_dimensions, PilImage.LANCZOS)

    if reversed:
        img = img.rotate(180)

    img.save("temp_modified_image.png", "PNG")
    return "temp_modified_image.png"

import time

def stream_typing(text, typing_speed=0.1):
    container = st.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        container.markdown(displayed_text, unsafe_allow_html=True)
        time.sleep(typing_speed)

st.set_page_config(layout="centered")

st.markdown(f"# {to_color('**Welcome to your mystical Tarot Card Reading!**', 'pink')}", unsafe_allow_html=True)

st.markdown(f"### {to_color('**Instructions:**','pink')}", unsafe_allow_html=True)
st.markdown(f"{to_color('*In this reading, a 3-card spread will be used to provide insights into your past, present, and future. Each cards meaning will be tailored to the topic or question you provide.*', 'pink')}", unsafe_allow_html=True)
st.markdown(f"{to_color('Cards drawn in', 'pink')} {to_color('**reversed**','red')} {to_color('position represents blocked or repressed energies, while','pink')} {to_color('**upright**','green')}{to_color(': represents clear and direct energies.','pink')}", unsafe_allow_html=True)

st.markdown(f"### {to_color('**Tarot Card Meanings:**','pink')}", unsafe_allow_html=True)
question_topic = st.text_input("What mystical inquiry or area of curiosity shall we delve into for your Tarot Card Reading?")

if st.button("Reveal Cards"):
    reader_intro = get_tarot_reading(f"The user has asked about \"{question_topic}\". Say something ominous to begin the reading, but do not expext an answer as the next message will be the terot reading results.")
    st.markdown(f"### {to_color('**Reading:**','orange')}", unsafe_allow_html=True)
    st.markdown(to_color(f'{reader_intro}', color='orange'), unsafe_allow_html=True)

    (past_card, tarot_deck[past_card], past_ori), (present_card, tarot_deck[present_card], present_ori), (future_card, tarot_deck[future_card], future_ori) = draw_three_card_spread(tarot_deck)

    past_card = past_card.replace("_", " ")
    tarot_question = f"The {past_card} card is drawn in the {past_ori} position for the past. What does it mean with respect to \"{question_topic}\"?"
    response_past = get_tarot_reading(tarot_question)
    past_color = "red" if "reversed" in response_past else "green"
    is_reversed = True if "reversed" in response_past else False
    past_ori = f'{past_ori[0].upper()}{past_ori[1:]}'
    st.markdown(f"\n### {to_color('Past Card', 'purple')}: {to_color(past_card, past_color)} in {to_color(past_ori, past_color)} position:", unsafe_allow_html=True)
    st.image(get_card_image(past_card, scaling_factor=0.5, reversed=is_reversed))
    st.markdown(f"{response_past}")

    present_card = present_card.replace("_", " ")
    tarot_question = f"The {present_card} card is drawn in the {present_ori} position for the present. What does it mean with respect to \"{question_topic}\"?"
    response_present = get_tarot_reading(tarot_question)
    present_color = "red" if "reversed" in response_present else "green"
    is_reversed = True if "reversed" in response_present else False
    present_ori = f'{present_ori[0].upper()}{present_ori[1:]}'
    st.markdown(f"\n### {to_color('Present Card', 'orange')}: {to_color(present_card, present_color)} in {to_color(present_ori, present_color)} position:", unsafe_allow_html=True)
    st.image(get_card_image(present_card, scaling_factor=0.5, reversed=is_reversed))
    st.markdown(f"{response_present}")

    future_card = future_card.replace("_", " ")
    tarot_question = f"The {future_card} card is drawn in the {future_ori} position for the future. What does it mean with respect to \"{question_topic}\"?"
    response_future = get_tarot_reading(tarot_question)
    future_color = "red" if "reversed" in response_future else "green"
    is_reversed = True if "reversed" in response_future else False
    st.markdown(f"\n### {to_color('Future Card', 'yellow')}: {to_color(future_card, future_color)} in {to_color(future_ori, future_color)} position:", unsafe_allow_html=True)
    st.image(get_card_image(future_card, scaling_factor=0.5, reversed=is_reversed))
    st.markdown(f"{response_future}")

    sys_out = get_tarot_reading("<<SYSTEM MESSAGE>> The reading is complete. Thank the user for their time and say goodbye. <<END SYSTEM MESSAGE>>")
    st.markdown(f"\n## {to_color(f'{sys_out}', 'pink')}", unsafe_allow_html=True)


def draw_past_card():
    past_card = random.choice(list(tarot_deck.keys()))
    past_card = past_card.replace("_", " ")
    return past_card

def draw_present_card():
    present_card = random.choice(list(tarot_deck.keys()))
    present_card = present_card.replace("_", " ")
    return present_card

def draw_future_card():
    future_card = random.choice(list(tarot_deck.keys()))
    future_card = future_card.replace("_", " ")
    return future_card

