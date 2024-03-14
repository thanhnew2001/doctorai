# from transformers import AutoTokenizer
model_name = "michaelfeil/ct2fast-phi-1_5"


from hf_hub_ctranslate2 import GeneratorCT2fromHfHub
model = GeneratorCT2fromHfHub(
        # load in int8 on CUDA
        model_name_or_path=model_name,
        device="cuda",
        compute_type="int8_float16",
        # tokenizer=AutoTokenizer.from_pretrained("{ORG}/{NAME}")
)
outputs = model.generate(
    text=["def fibonnaci(", "User: How are you doing? Bot:"],
    max_length=64,
    include_prompt_in_result=False
)
print(outputs)
