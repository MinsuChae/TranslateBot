import json
from transformers import AutoTokenizer, AutoModelForCausalLM

SUPPORT_LANGUAGES = ['en','ko']
MODEL = "Minsu-Chae/gemma-2b-translate"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL)
def translate(**kwargs)->str | None:
    if 'msg' not in kwargs:
        return "!translate original_language target_language text\n.It support only english(en) and korean(ko)."
    if 'original' not in kwargs or 'target' not in kwargs :
        if 'option' in kwargs:
            msg = kwargs['msg']
            parsing = msg.split(maxsplit=1)
            parsing = [text.strip() for text in parsing]

            original = kwargs['option'].lower()
            target = parsing[0].lower()
            msg = parsing[1]
        else:
            return "!translate original_language target_language text\n.It support only english(en) and korean(ko)."
    else:
        original = kwargs['original'].lower()
        target = kwargs['target'].lower()
        msg = kwargs['msg']

    if original == target:
        return "Two languages are same."
    elif original not in SUPPORT_LANGUAGES or target not in SUPPORT_LANGUAGES:
        return "It support only english(en) and korean(ko)."

    with open("translate_prompt.json","r") as file:
        template = json.load(file)

    input_text = template[target].format(msg)
    input_ids = tokenizer(input_text, return_tensors="pt")

    outputs = model.generate(**input_ids)
    translate_msg = tokenizer.decode(outputs[0])
    del input_text
    del input_ids
    del outputs
    return translate_msg

