import requests
from bs4 import BeautifulSoup
import openai

# setup API
openai.api_key = 'API KEY'

# Function to get the head tags  and image information of a URL
def get_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = []

    # Retrieve headlines and associated images
    headlines = soup.find_all(['h1', 'h2', 'h3'])
    for headline in headlines:
        headline_text = headline.get_text().strip()
        image_info = headline.find_next('img')
        if image_info:
            image_src = image_info.get('src')
            content.append({'headline': headline_text, 'image_src': image_src})
        else:
            content.append({'headline': headline_text, 'image_src': None})

    return content

# Function to ask a question to ChatGPT
def ask_question(question):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=question,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.0,
        top_p=1.0
    )
    answer = response.choices[0].text.strip()
    return answer

# Main function
def main():
    # Get the URL from user input
    url = input("Enter a URL to crawl: ")

    # Get the headlines and image information from the URL
    content = get_content(url)

    question = f"What is the website about?"
    # Send the headlines and image information to ChatGPT and ask the question
    for item in content:
        question += f" {item['headline']}."

    answer = ask_question(question)
    print("question:", question)
    print("Answer:", answer)
    print()
# Run the main function
if __name__ == '__main__':
    main()
