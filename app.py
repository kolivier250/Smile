from flask import Flask, request, jsonify, send_from_directory
import json
import openai

app = Flask(__name__)

# Load structured FAQs from JSON file
with open('structured_faqs.json', 'r', encoding='utf-8') as file:
    faq_data = json.load(file)

# Set up OpenAI API key
import os
openai.api_key = os.getenv('OPENAI_API_KEY')
def get_answer_from_gpt(question):
    # Combine FAQs into a single prompt
    prompt = "Answer the following question based on the FAQs:\n\n"
    for category, faqs in faq_data.items():
        prompt += f"{category}:\n"
        for faq in faqs:
            prompt += f"Q: {faq['question']}\nA: {faq['answer']}\n\n"

    prompt += f"Q: {question}\nA:"

    # Get response from OpenAI GPT
    response = openai.Completion.create(
        engine="text-davinci-003",  # Use GPT-3.5
        prompt=prompt,
        max_tokens=150
    )

    return response.choices[0].text.strip()

@app.route('/ask', methods=['GET'])
def ask():
    # Get the question from the query parameters
    question = request.args.get('question')

    # Use OpenAI GPT to get the answer
    answer = get_answer_from_gpt(question)

    return jsonify({
        "question": question,
        "answer": answer
    })

@app.route('/search', methods=['GET'])
def search():
    # Get the keyword from the query parameters
    keyword = request.args.get('keyword')

    # Search for the keyword in the FAQs
    results = []
    for category, faqs in faq_data.items():
        for faq in faqs:
            if keyword.lower() in faq['question'].lower() or keyword.lower() in faq['answer'].lower():
                results.append({
                    "category": category,
                    "question": faq['question'],
                    "answer": faq['answer']
                })

    return jsonify(results)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
    from dotenv import load_dotenv

    load_dotenv()  # Load environment variables from .env file