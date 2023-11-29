import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
# from transformers import Blip2Processor, Blip2ForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base",torch_dtype=torch.float16).to("mps")
# processor = Blip2Processor.from_pretrained("Salesforce/blip2-flan-t5-xl")
# model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-flan-t5-xl",torch_dtype=torch.float16).to("cuda")

def generate_caption(pil_image, question):
    global previous_caption
    try:
        inputs = processor(pil_image, text=question, return_tensors="pt").to("mps", torch.float16)
        out = model.generate(**inputs, max_new_tokens=1000)
        caption = processor.decode(out[0], skip_special_tokens=True)
        # caption= processor.batch_decode(out, skip_special_tokens=True)[0].strip()
        previous_caption = caption
        return caption
    except:
        return "Unable to process image."
