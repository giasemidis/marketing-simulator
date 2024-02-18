import os
import json
from dotenv import load_dotenv, find_dotenv
import openai
from openai import OpenAI


if os.environ.get('OPENAI_API_KEY') is not None:
    openai.api_key = os.environ['OPENAI_API_KEY']
else:
    _ = load_dotenv(find_dotenv())  # read local .env file
    openai.api_key = os.environ['OPENAI_API_KEY']


def consumer_agent(
        brand_names, brand_messages,
        demographic=None, interests=None, habits=None
    ):
    client = OpenAI()
    messages = [
        {
            "role": "system",
            "content": (
                "You are a consumer that reacts to advertising messages by the campaign "
                "of brands "
                # f"of brands {brand_name}."
                f"The consumer is: {demographic}, "
                f"with interests: {interests}, "
                f"and has habits: {habits}, "
            )
        }
    ]
    if len(brand_names) == 1:
        messages.append({
            "role": "user",
            "content": (
                f"The marketing message of brand {brand_names[0]} is {brand_messages[0]}. "
                "What is your opinion about the brand? Also, return: "
                " * a sentiment score between -1 and 1 of the generated answer, "
                "with -1 being very negative sentiment, 0 being neutral and 1 being very "
                "positive, "
                " * a probability of purchase from the generated answer between 0 and 1 "
                "with 0 being no chance of buying and 1 certainly buying, "
                "in the following format:\n"
                '{"opinion": "<opinion generated>", "sentiment": <sentiment score>, '
                '"probability": <probability>}'
            )
        })
    elif len(brand_names) == 2:
        messages.append({
            "role": "user",
            "content": (
                f"The marketing message of brand {brand_names[0]} is {brand_messages[0]}. "
                f"The marketing message of the second brand {brand_names[1]} is {brand_messages[1]}. "
                "What is your opinion about the two brands? Also, return: "
                " * a sentiment score between -1 and 1 of the two generated answers, "
                "with -1 being very negative sentiment, 0 being neutral and 1 being very "
                "positive, "
                " * a probability of purchase from the two generated answers between 0 and 1 "
                "with 0 being no chance of buying and 1 certainly buying, given the competition between the two brands"
                "in the following format:\n"
                '{"<brand 1>": {"opinion": "<opinion generated>", "sentiment": <sentiment score>, '
                '"probability": <probability>}, "<brand 2>": {"opinion": "<opinion generated>", "sentiment": <sentiment score>, '
                '"probability": <probability>}}'
            )
        })
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=messages,
      temperature=0.0,
      max_tokens=256,
      top_p=0.5,
      frequency_penalty=0,
      presence_penalty=0,
      stop=None
    )
    r = json.loads(
        response.choices[0].message.content
    )
    return r
