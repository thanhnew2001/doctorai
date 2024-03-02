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
    corrected_sentence = result.text

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
        corrected_sentence = result.text
        corrected_sentences.append(corrected_sentence)

    # Return list of corrected sentences
    return jsonify({'corrected_sentences': corrected_sentences})

# New route for generating corrected sentences based on prompts
@app.route('/generate_code', methods=['GET'])
def generate_code():
    # Get prompts from request
    prompts = request.args.get('prompts', '')
    max_length = int(request.args.get('max_length', 50))  # Convert max_length to integer

    # Split the prompts into individual sentences based on your defined structure
    sentences = prompts
    corrected_sentences = []
    for sentence in sentences:
        if sentence:  # Check if sentence is not empty
            # Add prefix required by the HappyTextToText model
            prefixed_sentence = "grammar: " + sentence.strip()  # Remove leading/trailing whitespace
            # Generate corrected sentence
            result = happy_tt.generate_text(prefixed_sentence, args=args)
            corrected_sentence = result.text
            corrected_sentences.append(corrected_sentence)

    # Return list of corrected sentences, adhering to the max_length parameter if necessary
    return jsonify(corrected_sentences)

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
