from flask import Flask, render_template
from flask_sse import sse

from openai import OpenAI

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"  # Configure Redis for flask-sse
app.register_blueprint(sse, url_prefix="/stream")  # Register the SSE blueprint

client = OpenAI()

# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/start_chat")
def start_chat():
    output =''
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Say this is a test"}],
        stream=True,
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            sse.publish(chunk.choices[0].delta.content, type="chat")
            output += chunk
    return "", 204  # No content

# if __name__ == "__main__":
#     app.run(debug=True)
