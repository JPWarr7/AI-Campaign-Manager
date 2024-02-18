from openai import OpenAI
client = OpenAI()

def summarization(links):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a skilled summarization writer, capable of reading articles and summarizing them into important and relevant content."},
        {"role": "user", "content": f'Give me a one-paragraph summarization for each of the following links in less than 1500 characters total. : {links}'}
    ]
    )
    return completion.choices[0].message.content

def text_generation(summary, perspective):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a skilled advertiser, capable of advertising a product from the perspective of any human."},
        {"role": "user", "content": f'In less than 1500 characters, compose an advertisement containing information from {summary} from the perspective of {perspective}.'}
    ]
    )
    return completion.choices[0].message.content

def image_generation(prompt):
    response = client.images.generate(
    model="dall-e-3",
    prompt= f'{prompt}',
    size="1024x1024",
    quality="standard",
    n=1,
    )
    return response.data[0].url
