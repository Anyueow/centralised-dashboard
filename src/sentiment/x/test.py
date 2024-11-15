import os
from anthropic import Anthropic
import streamlit as st

print("debug")
# Set your xAI API key
api_key = st.secrets["XAI_API_KEY"]


# Initialize the Anthropic client with xAI's base URL
client = Anthropic(
    api_key=api_key,
    base_url="https://api.x.ai",
)

# Define the conversation
messages = [
    {
        "role": "user",
        "content": "make this funnier & sassier:For those not participating in BeerioKart or spectating (boo…..jk), and for those who will "
                   "claim an early loss and be kicked out of the bracket faster than they entered (aka me), "
                   "here are some casual happy hour spots for todayyy: ",

    },
]

# Create a chat completion
message = client.messages.create(
    model="grok-beta",
    max_tokens=128,
    system="You are Grok,a voice of the people's heinous tweets.",
    messages=messages,
)

# Print the assistant's response
print(message.content)
