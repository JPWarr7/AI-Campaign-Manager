from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

client = OpenAI()

def summarization(links):
    """
    This function takes a list of links as input and generates a summarization
    for each link using OpenAI's GPT-3.5 model.

    Parameters:
        links (str): A list of URLs or links to articles.
            ex. 'link1.com link2.edu link3.org'
    Returns:
        str: A summarization of the content found at the provided links.
    Example:
        summarization(links)
    """
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a skilled summarization writer, capable of reading articles and summarizing them into important and relevant content."},
        {"role": "user", "content": f'Give me a one-paragraph summarization for each of the following links in less than 1500 characters total : {links}'}
    ],
    stream=True
    )

    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            yield str(chunk.choices[0].delta.content)

def text_generation(summary, perspective):
    """
    This function generates an advertisement text based on a given summary and perspective
    using OpenAI's GPT-3.5 model.

    Parameters:
        summary (str): A summary of the product or content to be advertised.
        perspective (str): The perspective from which the advertisement should be generated.

    Returns:
        str: An advertisement text containing information from the provided summary
             from the specified perspective.

    Example:
        text_generation("The latest smartphone offers cutting-edge features and sleek design.",
                        "a tech enthusiast")
    """
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a skilled social media advertiser, capable of advertising a product from the perspective of any human."},
        {"role": "user", "content": f'In less than 280 characters, compose an advertisement containing information from {summary} from the perspective of {perspective}.'}
    ],
    stream=True
    )

    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            yield str(chunk.choices[0].delta.content)

def image_generation(prompt):
    """
    This function generates an image based on the given prompt using OpenAI's DALL-E 3 model.

    Parameters:
        prompt (str): A prompt for generating the image.

    Returns:
        str: URL of the generated image.

    Example:
        image_generation("a cat sitting on a tree branch")
    """    
    response = client.images.generate(
    model="dall-e-3",
    prompt= f'{prompt}',
    size="1024x1024",
    quality="standard",
    n=1
    )
    return response.data[0].url

def image_regeneration(prompt, img_url, ad_text, perspective):
    """
    This function regenerates an image based on the given prompt and source image provided using OpenAI's DALL-E 2 model.

    Parameters:
        prompt (str): A prompt for providing feedback in which to regenerate the image.
        img_url (str): An image source link, which will be altered using the feedback prompt and DALL-E 2 model.

    Returns:
        str: URL of the regenerated image.

    Example:
        regenerate_image("remove the text from this image", "img url")
    """
    
    response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": "Please describe everything in this image"},
            {
            "type": "image_url",
            "image_url": {
                "url": f'{img_url}',
            },
            },
        ],
        }
    ],
    max_tokens=300,
    )
    output = response.choices[0]
    img_prompt = f'Generate an image like this {output} while adding this change: {prompt}. For context, this image was generated from this advertisement {ad_text} using this perspective {perspective}.'
    
    response = client.images.generate(
    model="dall-e-3",
    prompt= f'{img_prompt}',
    size="1024x1024",
    quality="standard",
    n=1
    )
    return response.data[0].url

def advertisement_regeneration(prompt, feedback, perspective, summarization):
    """
    This function regenerates text based on a given prompt and feedback
    using OpenAI's GPT-3.5 model.

    Parameters:
        prompt (str): The original prompt to which will be edited
        feedback (str): The feedback provided to the original prompt

    Returns:
        str: Text containing information from the provided prompt
             using the specified feedback.

    Example:
        text_generation("The latest smartphone offers cutting-edge features and sleek design.",
                        "Make this more interactive")
    """    
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a skilled advertiser, capable of advertising a product from the perspective of any human."},
        {"role": "user", "content": f'In less than 1500 characters, regenerate this prompt: {prompt}, by using this perspective {perspective} and taking into consideration this feedback: {feedback}. the prompt was generated from this summarization {summarization}'}
    ],
    stream=True
    )

    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            yield str(chunk.choices[0].delta.content)
            
def summary_regeneration(prompt, feedback, links):
    """
    This function regenerates text based on a given prompt and feedback
    using OpenAI's GPT-3.5 model.

    Parameters:
        prompt (str): The original prompt to which will be edited
        feedback (str): The feedback provided to the original prompt

    Returns:
        str: Text containing information from the provided prompt
             using the specified feedback.

    Example:
        text_generation("The latest smartphone offers cutting-edge features and sleek design.",
                        "Make this more interactive")
    """    
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a skilled summarization writer, capable of reading articles and summarizing them into important and relevant content."},
        {"role": "user", "content": f'Give me a one-paragraph summarization for each of the following links in less than 1500 characters total : {links} by regenerating this prompt: {prompt} and taking into consideration this feedback: {feedback}.'}
    ],
    stream=True
    )

    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            yield str(chunk.choices[0].delta.content)