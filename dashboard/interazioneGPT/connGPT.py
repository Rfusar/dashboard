import openai


def interact_with_chatgpt_prova(user, system, API_KEY, maxContent, creativita):
    openai.api_key = API_KEY

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        max_tokens=maxContent,  # Puoi regolare questo valore per ottenere risposte più lunghe o più corte (N token)
        temperature=creativita,  # Puoi regolare questo valore per controllare la "creatività" delle risposte
    )

     

    return [response['choices'][0]['message']['content'], response['usage']['total_tokens']]