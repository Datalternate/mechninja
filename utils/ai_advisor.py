import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_recommendations(ecu_info, fault_codes):
    prompt = f"""
    You're a car diagnostics assistant. Based on this ECU info and fault codes, give repair advice and performance tips.

    ECU Info:
    {ecu_info}

    Fault Codes:
    {fault_codes}

    Respond clearly and concisely.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )

    return response.choices[0].message.content
