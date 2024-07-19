import json
import google.generativeai as genai
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from openai import OpenAI
from openai import AzureOpenAI

import streamlit as st

def dread_json_to_markdown(dread_assessment):
    markdown_output = "| Threat Type | Scenario | Damage Potential | Reproducibility | Exploitability | Affected Users | Discoverability | Risk Score |\n"
    markdown_output += "|-------------|----------|------------------|-----------------|----------------|----------------|-----------------|-------------|\n"
    try:
        # Access the list of threats under the "Risk Assessment" key
        threats = dread_assessment.get("Risk Assessment", [])
        for threat in threats:
            # Check if threat is a dictionary
            if isinstance(threat, dict):
                damage_potential = threat.get('Damage Potential', 0)
                reproducibility = threat.get('Reproducibility', 0)
                exploitability = threat.get('Exploitability', 0)
                affected_users = threat.get('Affected Users', 0)
                discoverability = threat.get('Discoverability', 0)
                
                # Calculate the Risk Score
                risk_score = (damage_potential + reproducibility + exploitability + affected_users + discoverability) / 5
                
                markdown_output += f"| {threat.get('Threat Type', 'N/A')} | {threat.get('Scenario', 'N/A')} | {damage_potential} | {reproducibility} | {exploitability} | {affected_users} | {discoverability} | {risk_score:.2f} |\n"
            else:
                raise TypeError(f"Expected a dictionary, got {type(threat)}: {threat}")
    except Exception as e:
        # Print the error message and type for debugging
        st.write(f"Error: {e}")
        raise
    return markdown_output


# Function to create a prompt to generate mitigating controls
def create_dread_assessment_prompt(threats):
    prompt = f"""
Bertindaklah sebagai ahli keamanan siber dengan lebih dari 20 tahun pengalaman dalam pemodelan ancaman menggunakan metodologi STRIDE dan DREAD. Tugas Anda adalah menghasilkan penilaian risiko DREAD untuk ancaman-ancaman yang diidentifikasi dalam model ancaman. Berikut adalah daftar ancaman yang telah diidentifikasi:
{threats}
Saat memberikan penilaian risiko, gunakan format respons JSON dengan kunci tingkat atas "Risk Assessment" dan daftar ancaman, masing-masing dengan sub-kunci berikut:
- "Threat Type": Sebuah string yang mewakili jenis ancaman (misalnya, "Spoofing").
- "Scenario": Sebuah string yang menggambarkan skenario ancaman dan ubah kedalam bahasa Indonesia.
- "Damage Potential": Sebuah bilangan bulat antara 1 dan 10.
- "Reproducibility": Sebuah bilangan bulat antara 1 dan 10.
- "Exploitability": Sebuah bilangan bulat antara 1 dan 10.
- "Affected Users": Sebuah bilangan bulat antara 1 dan 10.
- "Discoverability": Sebuah bilangan bulat antara 1 dan 10.

Tentukan nilai antara 1 dan 10 untuk setiap sub-kunci berdasarkan metodologi DREAD. Gunakan skala berikut:
- 1-3: Rendah
- 4-6: Sedang
- 7-10: Tinggi

Pastikan respons JSON diformat dengan benar dan tidak mengandung teks tambahan. Berikut adalah contoh format respons JSON yang diharapkan:
{{
  "Risk Assessment": [
    {{
      "Threat Type": "Spoofing",
      "Scenario": "Seorang penyerang dapat membuat penyedia OAuth2 palsu dan menipu pengguna untuk masuk melalui penyedia tersebut.",
      "Damage Potential": 8,
      "Reproducibility": 6,
      "Exploitability": 5,
      "Affected Users": 9,
      "Discoverability": 7
    }},
    {{
      "Threat Type": "Spoofing",
      "Scenario": "Seorang penyerang dapat mencegat proses pertukaran token OAuth2 melalui serangan Man-in-the-Middle (MitM).",
      "Damage Potential": 8,
      "Reproducibility": 7,
      "Exploitability": 6,
      "Affected Users": 8,
      "Discoverability": 6
    }}
  ]
}}
"""
    return prompt

# Fungsi untuk mendapatkan penilaian risiko ketakutan dari respons GPT.
def get_dread_assessment(api_key, model_name, prompt):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model_name,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Asisten yang membantu yang dirancang untuk menampilkan JSON."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Konversi string JSON di bagian 'konten' ke kamus Python
    try:
        dread_assessment = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError as e:
        st.write(f"JSON decoding error: {e}")
        dread_assessment = {}
    
    return dread_assessment

# Fungsi untuk mendapatkan penilaian risiko ketakutan dari respons Azure OpenAI.
def get_dread_assessment_azure(azure_api_endpoint, azure_api_key, azure_api_version, azure_deployment_name, prompt):
    client = AzureOpenAI(
        azure_endpoint = azure_api_endpoint,
        api_key = azure_api_key,
        api_version = azure_api_version,
    )

    response = client.chat.completions.create(
        model = azure_deployment_name,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Asisten yang membantu yang dirancang untuk menampilkan JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    # Konversi string JSON di bagian 'konten' ke kamus Python
    try:
        dread_assessment = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError as e:
        st.write(f"JSON decoding error: {e}")
        dread_assessment = {}
    
    return dread_assessment

# Fungsi untuk mendapatkan penilaian risiko ketakutan dari respons model Google.
def get_dread_assessment_google(google_api_key, google_model, prompt):
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

# Fungsi untuk mendapatkan penilaian risiko ketakutan dari respons model mistral.
def get_dread_assessment_mistral(mistral_api_key, mistral_model, prompt):
    client = MistralClient(api_key=mistral_api_key)

    response = client.chat(
        model = mistral_model,
        response_format={"type": "json_object"},
        messages=[
            ChatMessage(role="user", content=prompt)
        ]
    )

    # Konversi string JSON di bagian 'konten' ke kamus Python
    response_content = json.loads(response.choices[0].message.content)

    return response_content