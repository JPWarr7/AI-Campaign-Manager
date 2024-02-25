from openai import OpenAI
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
        {"role": "system", "content": "You are a skilled advertiser, capable of advertising a product from the perspective of any human."},
        {"role": "user", "content": f'In less than 1500 characters, compose an advertisement containing information from {summary} from the perspective of {perspective}.'}
    ],
    stream=True
    )

    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            yield str(chunk.choices[0].delta.content)

def image_generation(prompt):
    """
    This function generates an image based on the given prompt using OpenAI's DALL-E model.

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
