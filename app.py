from flask import Flask, request, jsonify
from happytransformer import HappyTextToText, TTSettings

# Initialize Flask app
app = Flask(__name__)

# Initialize HappyTextToText with T5 model for grammar correction
happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
args = TTSettings(num_beams=5, min_length=1)

# Route for correcting a single sentence, supports both GET and POST methods
@app.route('/correct_grammar', methods=['GET', 'POST'])
def correct_grammar():
    # Get sentence from request
    if request.method == 'POST':
        sentence = request.json.get('sentence', '')
    else:  # GET request
        sentence = request.args.get('sentence', '')

    if not sentence:
        return jsonify({'error': 'No sentence provided'}), 400

    # Add prefix required by the HappyTextToText model
    prefixed_sentence = "grammar: " + sentence

    # Generate corrected sentence
    result = happy_tt.generate_text(prefixed_sentence, args=args)
    corrected_sentence = result.text.strip()

    # Return corrected sentence
    return jsonify({'corrected_sentence': corrected_sentence})

# New route for correcting a list of sentences, supports both GET and POST methods
@app.route('/correct_grammar_bulk', methods=['GET', 'POST'])
def correct_grammar_bulk():
    if request.method == 'POST':
        sentences = request.json.get('sentences', [])
    else:  # GET request
        sentences = request.args.getlist('sentences')

    if not sentences:
        return jsonify({'error': 'No sentences provided'}), 400

    corrected_sentences = []
    for sentence in sentences:
        # Add prefix required by the HappyTextToText model
        prefixed_sentence = "grammar: " + sentence
        # Generate corrected sentence
        result = happy_tt.generate_text(prefixed_sentence, args=args)
        corrected_sentence = result.text.strip()
        corrected_sentences.append(corrected_sentence)

    # Return list of corrected sentences
    return jsonify({'corrected_sentences': corrected_sentences})

@app.route('/generate_code', methods=['GET'])
def generate_code():
    # Get multiple prompts from request
    prompts = request.args.getlist('prompts')  # This will get a list of all 'prompts' in the query string

    corrected_sentences = []
    for prompt in prompts:
        print(prompt)
        # Remove the specific leading text from the prompt and strip whitespace
        cleaned_prompt = prompt.replace("Correct english in the following text, do not add any punctuation or extra text.", "").strip()
        
        # Prefix the cleaned prompt before sending to the model
        prefixed_sentence = "grammar: " + cleaned_prompt
        # Generate corrected sentence
        result = happy_tt.generate_text(prefixed_sentence, args=args)
        corrected_sentence = result.text.strip()
        print(corrected_sentence)
        corrected_sentences.append(corrected_sentence)

    print(corrected_sentences)
    # Return corrected sentences
    return jsonify(corrected_sentences)


# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
