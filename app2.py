# Import necessary libraries
from flask import Flask, request, jsonify
from hf_hub_ctranslate2 import GeneratorCT2fromHfHub

# Initialize Flask app
app = Flask(__name__)

# Define the model name
model_name = "michaelfeil/ct2fast-Llama-2-7b-hf"

# Initialize the model
model = GeneratorCT2fromHfHub(
    model_name_or_path=model_name,
    device="cuda",  # Specify the device (e.g., "cuda" for GPU)
    compute_type="int8_float16"  # Specify the compute type
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
