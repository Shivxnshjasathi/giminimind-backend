import os
import google.generativeai as genai
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Set up the API key and model
os.environ['GOOGLE_API_KEY'] = 'AIzaSyAPHtUCHKOZ2YAOOlPETWaVFaBAoVKhs6U'  # Replace with your actual API key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Set up the model
model = genai.GenerativeModel('gemini-pro')

# Function to get response from Gemini API
def get_gemini_response(prompt):
    response = model.generate_content(prompt)
    return response.text

# Define Flask route for chatbot interaction
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')

        if not user_message:
            return jsonify({'error': 'Message is required'}), 400

        # Initial context for the AI
        context = """
        You are a supportive and empathetic AI assistant designed to provide mental health support. 
        Your responses should be caring, non-judgmental, and aimed at promoting emotional well-being. 
        However, always remind the user that you are an AI and encourage them to seek professional help for serious concerns.
        """

        # Full prompt for the AI
        full_prompt = f"{context}\n\nUser: {user_message}\nAI:"

        # Get response from Gemini AI
        response = get_gemini_response(full_prompt)

        # Return the AI response in JSON format
        return jsonify({'response': response}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Start the Flask app
if __name__ == "__main__":
    app.run(port=5000, debug=True)
