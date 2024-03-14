
# Import necessary libraries
from flask import Flask, request, jsonify
from hf_hub_ctranslate2 import GeneratorCT2fromHfHub
from transformers import AutoTokenizer


# Initialize Flask app
app = Flask(__name__)

model_name = "michaelfeil/ct2fast-gpt-j-6b"
# use either TranslatorCT2fromHfHub or GeneratorCT2fromHfHub here, depending on model.
model = GeneratorCT2fromHfHub(
        # load in int8 on CUDA
        model_name_or_path=model_name, 
        device="cuda",
        compute_type="int8_float16",
        tokenizer=AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6b")
)

# Define the route for generating corrected code
@app.route('/generate_code', methods=['GET'])
def generate_code():
    # Get prompts from request
    prompts = request.args.getlist('prompts')

    corrected_sentences = []
    for prompt in prompts:              
        # Generate corrected sentences using the model
        outputs = model.generate(text=[prefixed_sentence], max_length=64, include_prompt_in_result=False)

    # Return corrected sentences as a list
    return jsonify(outputs)

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
