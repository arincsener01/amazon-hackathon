import os
from chatbot.chatbot import Chatbot
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_KEY


# app = Flask(__name__)

# @app.route("/chat", methods=["POST"])
# def chat():
#     req_json = request.json
#     question = req_json.get("question")
#     codebase = req_json.get("codebase")

#     if not question or not codebase:
#         return {"error": "Missing question or codebase"}, 400

#     chatbot = Chatbot(codebase)
#     response = chatbot.get_response(question)
#     return response

# if __name__ == "__main__":
#     app.run(debug=True)
chatbot = Chatbot("backend")
response = chatbot.get_response("How is the weather in Ankara?")
print(response)