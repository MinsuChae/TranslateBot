import json
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

SUPPORT_LANGUAGES = ['en','ko']
MODEL = "Minsu-Chae/gemma-2b-translate"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL)
translate_generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
TOKEN = "<pad>Translate text:"

def translate(**kwargs)->str | None:
    if 'msg' not in kwargs:
        return "!translate target_language text\n.It support only english(en) and korean(ko)."
    if 'option' not in kwargs :
        return "!translate target_language text\n.It support only english(en) and korean(ko)."
    else:
        target = kwargs['option'].lower()
        msg = kwargs['msg']

    if target not in SUPPORT_LANGUAGES:
        return "It support only english(en) and korean(ko)."

    with open("function/translate_prompt.json","r") as file:
        template = json.load(file)

    input_text = template[target].format(msg)
    outputs = translate_generator(input_text, max_length=len(input_text)+50, num_beams=5, early_stopping=True, temperature=0.7)[0]['generated_text']
    translate_text = outputs[outputs.find(TOKEN)+len(TOKEN):]
    del input_text
    del outputs
    return translate_text

