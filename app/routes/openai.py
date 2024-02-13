from openai import OpenAI
client = OpenAI()

# myLinks = "https://www.sneakerfreaker.com/news/state-of-the-sneakersphere-survey-results-2023#:~:text=Some%20of%20the%20most%20surprising,voters%20feeling%20negatively%20towards%20them https://www.gq-magazine.co.uk/article/best-sneakers-2023 https://www.byrdie.com/fall-sneaker-trends-2023-8361991 "

# myPerspective = "Donald Trump"

def summarization(links):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a skilled summarization writer, capable of reading articles and summarizing them into important and relevant content."},
        {"role": "user", "content": f'Give me a one-paragraph summarization for each of the following links in less than 2500 characters total. : {links}'}
    ]
    )
    return completion.choices[0].message.content

# mySummary = summarization(myLinks)

#print(mySummary)

def text_generation(summary, perspective):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a skilled advertiser, capable of advertising a product from the perspective of any human."},
        {"role": "user", "content": f'In less than 2000 characters, compose an advertisement containing information from {summary} from the perspective of {perspective}.'}
    ]
    )
    return completion.choices[0].message.content

# myAdvertisement =  text_generation(mySummary, myPerspective)
#print(myAdvertisement)

# myImagePrompt = "Generate an image capturing the spirit of the following text" + myAdvertisement

def image_generation(prompt):
    response = client.images.generate(
    model="dall-e-3",
    prompt= f'{prompt}',
    size="1024x1024",
    quality="standard",
    n=1,
    )
    return response.data[0].url

# myImage = image_generation(myImagePrompt)
# print(myImage)