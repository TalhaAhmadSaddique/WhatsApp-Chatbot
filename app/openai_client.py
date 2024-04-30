import os
import openai
from dotenv import load_dotenv
load_dotenv()

class OpenAIClient:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        print(openai.api_key)
        print ("\nopenai key is" + openai.api_key + " and its type is " + openai.api_type)

    def chatbot(self, prompt):
        # response = openai.Completion.create(
        # model="text-davinci-003",
        # prompt=prompt,
        # temperature=0.0,
        # max_tokens=256,
        # top_p=1,
        # frequency_penalty=0,
        # presence_penalty=0
        # )
        response = prompt.upper()

        print ("response form openai is :\n" + str(response) + "\n")
        # return response.choices[0].text
        return response

if __name__ == "__main__":
    client = OpenAIClient()
    response = client.chatbot("how are you")
    print (response)
    