#threat_model.py

import json
import requests
import google.generativeai as genai
# from mistralai.client import MistralClient
# from mistralai.models.chat_completion import ChatMessage
from mistralai import Mistral, UserMessage
from openai import OpenAI
from openai import AzureOpenAI

import streamlit as st

# Fungsi untuk mengonversi JSON ke Markdown untuk tampilan.    
def json_to_markdown(threat_model, improvement_suggestions):
    markdown_output = "## Model ancaman\n\n"
    
    # Mulailah Markdown Table dengan header
    markdown_output += "| Jenis ancaman | Skenario | Dampak potensial |\n"
    markdown_output += "|-------------|----------|------------------|\n"
    
    # Isi baris tabel dengan data model ancaman
    for threat in threat_model:
        markdown_output += f"| {threat['Threat Type']} | {threat['Scenario']} | {threat['Potential Impact']} |\n"
    
    markdown_output += "\n\n## Saran peningkatan\n\n"
    for suggestion in improvement_suggestions:
        markdown_output += f"- {suggestion}\n"
    
    return markdown_output

# Berfungsi untuk membuat prompt untuk menghasilkan model ancaman
def create_threat_model_prompt(app_type, authentication, internet_facing, sensitive_data, app_input):
    prompt = f"""
Bertindak sebagai pakar keamanan dunia maya dengan lebih dari 20 tahun pengalaman menggunakan metodologi pemodelan ancaman langkah untuk menghasilkan model ancaman komprehensif untuk berbagai aplikasi.Tugas Anda adalah menggunakan deskripsi aplikasi dan tambahan yang diberikan kepada Anda untuk menghasilkan daftar ancaman spesifik untuk aplikasi tersebut.

Untuk masing -masing kategori langkah (spoofing, perusakan, penolakan, pengungkapan informasi, penolakan layanan, dan peningkatan hak istimewa), daftar beberapa (3 atau 4) ancaman yang kredibel jika berlaku.Setiap skenario ancaman harus memberikan skenario yang kredibel di mana ancaman dapat terjadi dalam konteks aplikasi.Sangat penting bahwa tanggapan Anda dirancang untuk mencerminkan detail yang diberikan kepada Anda.

Saat memberikan model ancaman, gunakan respons yang diformat JSON dengan kunci "ancaman_model" dan "perbaikan_sugestions".Di bawah "ancaman_model", sertakan serangkaian objek dengan kunci "jenis ancaman", "skenario", dan "dampak potensial".

Di bawah "Improvement_Sugestions", sertakan serangkaian string dengan saran tentang bagaimana ancaman pemodel dapat meningkatkan deskripsi aplikasi mereka untuk memungkinkan alat menghasilkan model ancaman yang lebih komprehensif kedalam bahasa Indonesia.

APPLICATION TYPE: {app_type}
AUTHENTICATION METHODS: {authentication}
INTERNET FACING: {internet_facing}
SENSITIVE DATA: {sensitive_data}
APPLICATION DESCRIPTION: {app_input}

Contoh format respons JSON yang diharapkan:
  
    {{
      "threat_model": [
        {{
          "Threat Type": "Spoofing",
          "Scenario": "Example Scenario 1",
          "Potential Impact": "Example Potential Impact 1"
        }},
        {{
          "Threat Type": "Spoofing",
          "Scenario": "Example Scenario 2",
          "Potential Impact": "Example Potential Impact 2"
        }},
        // ... more threats
      ],
      "improvement_suggestions": [
        "Example improvement suggestion 1.",
        "Example improvement suggestion 2.",
        // ... more suggestions
      ]
    }}
"""
    return prompt

def create_image_analysis_prompt():
    prompt = """
    Anda adalah arsitek solusi senior yang ditugaskan untuk menjelaskan diagram arsitektur berikut
    seorang arsitek keamanan untuk mendukung pemodelan ancaman sistem.

    Untuk menyelesaikan tugas ini, Anda harus:

      1. Menganalisis diagram
      2. Jelaskan arsitektur sistem kepada arsitek keamanan.Penjelasan Anda harus mencakup kunci
        Komponen, interaksi mereka, dan teknologi apa pun yang digunakan.
    
    Berikan penjelasan langsung tentang diagram dalam format yang jelas dan terstruktur, cocok untuk seorang profesional
    diskusi.
    
    Instruksi penting:
     - Jangan sertakan kata -kata sebelum atau sesudah penjelasan itu sendiri.Misalnya, jangan mulai
Penjelasan dengan "gambar menunjukkan ..." atau "Diagram menunjukkan ..." mulai menjelaskan komponen utama
dan detail lain yang relevan.
     - Jangan menyimpulkan atau berspekulasi tentang informasi yang tidak terlihat dalam diagram.Hanya memberikan informasi yang bisa
secara langsung ditentukan dari diagram itu sendiri.
    """
    return prompt

# Fungsi untuk menganalisis diagram arsitektur yang diunggah.
def get_image_analysis(api_key, model_name, prompt, base64_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                }
            ]
        }
    ]

    payload = {
        "model": model_name,
        "messages": messages,
        "max_tokens": 4000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Log the response for debugging
    try:
        response.raise_for_status()  # Raise an HTTPError for bad responses
        response_content = response.json()
        return response_content
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # HTTP error
    except Exception as err:
        print(f"Other error occurred: {err}")  # Other errors

    print(f"Response content: {response.content}")  # Log the response content for further inspection
    return None


# Fungsi untuk mendapatkan model ancaman dari respons GPT.
def get_threat_model(api_key, model_name, prompt):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model_name,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Anda adalah asisten yang membantu yang dirancang untuk menghasilkan JSON."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000,
    )

    # Konversi string JSON di bidang 'konten' ke kamus Python
    response_content = json.loads(response.choices[0].message.content)

    return response_content


# Function to get threat model from the Azure OpenAI response.
def get_threat_model_azure(azure_api_endpoint, azure_api_key, azure_api_version, azure_deployment_name, prompt):
    client = AzureOpenAI(
        azure_endpoint = azure_api_endpoint,
        api_key = azure_api_key,
        api_version = azure_api_version,
    )

    response = client.chat.completions.create(
        model = azure_deployment_name,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Anda adalah asisten yang membantu yang dirancang untuk menghasilkan JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    # Konversi string JSON di bidang 'konten' ke kamus Python
    response_content = json.loads(response.choices[0].message.content)

    return response_content


# Fungsi untuk mendapatkan model ancaman dari respons Google.
def get_threat_model_google(google_api_key, google_model, prompt):
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel(
        google_model,
        generation_config={"response_mime_type": "application/json"})
    response = model.generate_content(prompt)
    try:
        # Akses konten JSON dari atribut 'bagian' dari objek 'konten'
        response_content = json.loads(response.candidates[0].content.parts[0].text)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {str(e)}")
        print("Raw JSON string:")
        print(response.candidates[0].content.parts[0].text)
        return None

    return response_content

# Function to get threat model from the Mistral response.
def get_threat_model_mistral(mistral_api_key, mistral_model, prompt):
    client = Mistral(api_key=mistral_api_key)

    response = client.chat.complete(
        model = mistral_model,
        response_format={"type": "json_object"},
        messages=[
            # ChatCompletionResponse(role="user", content=prompt)
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    # Convert the JSON string in the 'content' field to a Python dictionary
    response_content = json.loads(response.choices[0].message.content)

    return response_content