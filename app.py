from flask import Flask, request, jsonify
import openai
import json
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)


# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def split_paragraphs(text):
    """Splits the input text into individual paragraphs."""
    return text.split('\n\n')  # Assuming paragraphs are separated by double newlines

@app.route('/api/correct', methods=['POST'])
def correct_text():
    data = request.get_json()
    input_text = data.get('text')

    if not input_text:
        return jsonify({"error": "Please provide text for correction."}), 400

    try:
        paragraphs = split_paragraphs(input_text)
        corrected_paragraphs = []
        details = {
            "spelling": [],
            "grammar": [],
            "better_usage_suggestions": [],
        }

        for paragraph in paragraphs:
            if not paragraph.strip():
                continue

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": f"""
                        Detect the language of the following text. If it's in a language other than English (for example, Telugu), translate it to English and correct grammar, spelling, and usage and present the result in a formal, professional tone,check the tense and grammar of languages and give output. If the input is already in English, perform corrections directly.
                    
                        {{
                            "spelling": "<List each incorrect word with the correct word in parentheses.>",
                            "grammar": "<Describe any grammatical mistakes.>",
                            "better_usage_suggestions": "<Suggestions for improvements.>",
                            "corrected_text": "<Return the corrected paragraph with correct punctuation.>"
                        }}
                        Paragraph: {paragraph}
                        """
                    }
                ],
                temperature=0
            )
            corrected_response = response['choices'][0]['message']['content']

            try:
                result = json.loads(corrected_response)
                corrected_paragraphs.append(result['corrected_text'])

                # Append specific feedback or leave empty if no feedback is provided
                details["spelling"].append(result.get("spelling", "").strip())
                details["grammar"].append(result.get("grammar", "").strip())
                details["better_usage_suggestions"].append(result.get("better_usage_suggestions", "").strip())

            except json.JSONDecodeError:
                logging.error("JSON decoding failed for response paragraph.")
                return jsonify({"error": "Failed to process the correction output. Please try again later."}), 500

        # Combine corrected paragraphs with double newlines to maintain structure
        full_corrected_text = "\n\n".join(corrected_paragraphs)

        # Set spelling message to indicate if issues were found or not
        final_spelling = "Spelling mistakes found:\n" + "\n".join([msg for msg in details["spelling"] if msg]) if any(details["spelling"]) else "No spelling mistakes found"
        
        # Grammar and usage suggestions - display only actual messages or "No issues found" if empty
        final_grammar = "\n".join([msg for msg in details["grammar"] if msg]) or "No grammar mistakes found"
        final_better_usage = "\n".join([msg for msg in details["better_usage_suggestions"] if msg]) or "No suggestions available"

        return jsonify({
            "corrected_text": full_corrected_text,
            "spelling": final_spelling,
            "grammar": final_grammar,
            "better_usage_suggestions": final_better_usage
        })

    except openai.error.RateLimitError:
        logging.error("API quota exceeded.")
        return jsonify({"error": "Service is temporarily unavailable. Please try again later."}), 429
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500
    saran
if __name__ == '__main__':
    app.run(debug=True, port=5000)
<<<<<<< HEAD
how are you
thank you 
=======
SyntaxWarning
>>>>>>> saran

