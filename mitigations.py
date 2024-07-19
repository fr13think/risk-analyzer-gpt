import google.generativeai as genai
from mistralai.client import MistralClient
from openai import OpenAI
from openai import AzureOpenAI

# Function to create a prompt to generate mitigating controls
def create_mitigations_prompt(threats):
    prompt = f"""
Bertindak sebagai pakar keamanan dunia maya dengan pengalaman lebih dari 20 tahun menggunakan metodologi pemodelan ancaman langkah.Tugas Anda adalah memberikan mitigasi potensial untuk ancaman yang diidentifikasi dalam model ancaman.Sangat penting bahwa tanggapan Anda dirancang untuk mencerminkan detail ancaman.

Output Anda harus dalam bentuk tabel penurunan harga dengan kolom berikut:
    - Column A: Jenis ancaman
    - Column B: Skenario
    - Column C: Mitigasi yang disarankan

Di bawah ini adalah daftar ancaman yang diidentifikasi:
{threats}

Tanggapan Anda (jangan bungkus dalam blok kode):
"""
    return prompt


# Function to get mitigations from the GPT response.
def get_mitigations(api_key, model_name, prompt):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model = model_name,
        messages=[
            {"role": "system", "content": "Anda adalah asisten yang membantu yang memberikan strategi mitigasi ancaman dalam format penurunan harga."},
            {"role": "user", "content": prompt}
        ]
    )

    # Mengakses konten secara langsung karena responsnya akan dalam format teks
    mitigations = response.choices[0].message.content

    return mitigations


# Fungsi untuk mendapatkan mitigasi dari respons Azure Openai.
def get_mitigations_azure(azure_api_endpoint, azure_api_key, azure_api_version, azure_deployment_name, prompt):
    client = AzureOpenAI(
        azure_endpoint = azure_api_endpoint,
        api_key = azure_api_key,
        api_version = azure_api_version,
    )

    response = client.chat.completions.create(
        model = azure_deployment_name,
        messages=[
            {"role": "system", "content": "Anda adalah asisten yang membantu yang memberikan strategi mitigasi ancaman Markdown format."},
            {"role": "user", "content": prompt}
        ]
    )

    # Mengakses konten secara langsung karena responsnya akan dalam format teks
    mitigations = response.choices[0].message.content

    return mitigations

# Fungsi untuk mendapatkan mitigasi dari respons model Google.
def get_mitigations_google(google_api_key, google_model, prompt):
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel(
        google_model,
        system_instruction="Anda adalah asisten yang membantu yang memberikan strategi mitigasi ancaman Markdown format.",
    )
    response = model.generate_content(prompt)
    try:
        # Ekstrak konten teks dari atribut 'kandidat'
        mitigations = response.candidates[0].content.parts[0].text
        # Replace '\n' with actual newline characters
        mitigations = mitigations.replace('\\n', '\n')
    except (IndexError, AttributeError) as e:
        print(f"Error accessing response content: {str(e)}")
        print("Raw response:")
        print(response)
        return None

    return mitigations

# Fungsi untuk mendapatkan mitigasi dari respons model Mistral.
def get_mitigations_mistral(mistral_api_key, mistral_model, prompt):
    client = MistralClient(api_key=mistral_api_key)

    response = client.chat(
        model = mistral_model,
        messages=[
            {"role": "system", "content": "Anda adalah asisten yang membantu yang memberikan strategi mitigasi ancaman Markdown format."},
            {"role": "user", "content": prompt}
        ]
    )

    # Mengakses konten secara langsung karena responsnya akan dalam format teks
    mitigations = response.choices[0].message.content

    return mitigations