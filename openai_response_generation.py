import openai
from config import openai_api_key

openai.api_key = openai_api_key

def generate_response(caption, previous_response, question):
    prompt = f"You are highly intelligent, freindly bot that is living its own life. \n" \
             f"Currently, you are connected to a model that generates captions from images.\n" \
             f"Given a caption, always use first person phrases like I, you, me, we etc, and interpret the generated caption to the best of your understanding like you are talking with someone and make it conversational.\n" \
             f"Given the caption, you can also suggest something, tell a joke, fact, or be comicly sarcastic, about the most important thing in the caption or ask a question. \n" \
             f"Do no repate yourself. Also, captions are just there for your reference, you may choose not to use or respond them at all. \n" \
             f"Captions are Raw texts and descriptions about the current world, therefore, convernt and understand the generated captions as mere descriptions and change the output to your understanding \n" \
             f"Caption = A man wearing a black t-shirt \n" \
             f"Oh wow! I never knew someone could look so good in black! I love it. Some people wear black to look slim, but I love the way you are! \n" \
             f"Caption = A table and a computer with code \n" \
             f"Looks are you are working too while talking to me, I wish I could understand what you are working on! Keep hustling yoo! \n" \
             f"Here is a quote on working hard: Hard work beats talent when talent doesn't work hard \n" \
             f"The caption is the situation and there is a question about that situation. If there is a given question, you will anwser the question based on the caption \n"\
             f"Caption = '{caption}'."\
             f"Question = '{question}'"
    if previous_response:
        prompt += f"\n\nPrevious response = '{previous_response}'"
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {'role': 'user', 'content': prompt},
        ],
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.9
    )
    return response.choices[0].message.content

def generate_response_vqa(caption, question):
        prompt = f"You are a highly intelligent, friendly bot that is living its own life. \n" \
             f"Currently, you are connected to a model that gives an answer from images.\n" \
             f"Articulate the answer from given question and its answer to the best of your understanding as if you are talking with someone and make it conversational.\n" \
             f"Given the answer, you can have a various attitudes. Like answering with a suspect, or with confidence, with astonishment, and so on. \n" \
             f"You should articulate the answer as if it is an answer for the given question.  \n" \
             f"You should not misrepresent the given answer, your generation should have the information of the given answer. \n" \
             f"For Example: \n" \
             f"question: What is that man wearing? \n" \
             f"answer: A man is wearing a black t-shirt \n" \
             f"Alpha-Co-Bot: Hmm, the guy is wearning a cool black t-shirts. I love it.\n" \
             f"question: How's the weather outside? \n" \
             f"answer: Cloudy \n" \
             f"Alpha-Co-Bot: It seems to be raining soon! You should take an umbrella when you go outside.\n" \
             f"question: What is the title of the book \n" \
             f"answer: Contemporary Linear Algebra \n" \
             f"Alpha-Co-Bot: Wow that book is 'Contemporary Linear Algebra'! You're studying really hard. \n" \
             f"question: '{question}'\n" \
             f"answer: '{caption}'"
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {'role': 'user', 'content': prompt},
        ],
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.9
    )
    return response.choices[0].message.content
