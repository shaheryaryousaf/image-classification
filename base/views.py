from django.shortcuts import render, redirect
from .forms import ImageForm
from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import openai
openai.api_key = "YOUR_OPENAI_API"


def index(request):
    form = ImageForm()
    predicted_classes = []  # Initialize as an empty list
    image_url = None

    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form_instance = form.save()
            image_path = form_instance.image.path
            image_url = form_instance.image.url

            # Image Classification
            image = Image.open(image_path)
            processor = ViTImageProcessor.from_pretrained(
                'google/vit-base-patch16-224')
            model = ViTForImageClassification.from_pretrained(
                'google/vit-base-patch16-224')
            inputs = processor(images=image, return_tensors="pt")
            outputs = model(**inputs)
            logits = outputs.logits

            # Get the top predicted class
            top_class_idx = logits.argmax(-1).item()
            top_class_labels = model.config.id2label[top_class_idx].split(", ")

            for class_label in top_class_labels:
                prompt = f"Identify and return the 2 lines detail of the animal type: {class_label}"
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a Zoologist with 15 years of experience and you will return the output of given prompt."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1
                )
                description = response['choices'][0]['message']['content']
                predicted_classes.append(
                    {'label': class_label, 'description': description})

    context = {
        'form': form,
        'predicted_classes': predicted_classes,
        'image_url': image_url
    }
    return render(request, 'index.html', context)
