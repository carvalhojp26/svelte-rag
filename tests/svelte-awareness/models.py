import ollama
import json

models = ["gemma3:latest", "mistral:latest", "llama3.2:latest", "deepseek-r1:1.5b", "codellama:latest", "qwen2.5-coder:0.5b", "tinyllama:latest", "yi:latest", "phi:latest", "ministral-3:3b"]
questions = ["In a paragraph, tell me what you know about Svelte.", "What is the latest version of Svelte? Answer with only the version number, nothing else."]
answers = {}

for model in models:
    answers[model] = {}
    for question in questions:
        response = ollama.chat(
            model = model,
            messages = [
                {'role': 'user', 'content': question}
            ]
        )
        answers[model][question] = response['message']['content']
with open('answers.json', 'w') as file:
    json.dump(answers, file, indent=4)