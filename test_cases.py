import google.generativeai as genai
from mistralai.client import MistralClient
from openai import OpenAI
from openai import AzureOpenAI

# Fungsi untuk membuat prompt untuk menghasilkan kontrol yang meringankan
def create_test_cases_prompt(threats):
    prompt = f"""
Bertindak sebagai pakar keamanan dunia maya dengan pengalaman lebih dari 20 tahun menggunakan metodologi pemodelan ancaman langkah.
Tugas Anda adalah menyediakan kasus uji Gherkin untuk ancaman yang diidentifikasi dalam model ancaman.Itu sangat penting
Respons Anda dirancang untuk mencerminkan detail ancaman.

Di bawah ini adalah daftar ancaman yang diidentifikasi:
{threats}

Gunakan deskripsi ancaman dalam langkah 'yang diberikan' sehingga kasus uji khusus untuk ancaman yang diidentifikasi.
Masukkan sintaks Gherkin di dalam triple backticks (`` `) untuk memformat kasus uji dalam penurunan harga. Tambahkan judul untuk setiap test case. Ubahlah hasil respon dari bahasa Inggris kedalam bahasa Indonesia.
Misalnya:

    ```gherkin
    Diberikan pengguna dengan akun yang valid
    Saat pengguna masuk
    Maka pengguna harus dapat mengakses sistem
    ```

Tanggapan Anda (jangan tambahkan teks pengantar, cukup berikan kasus uji gherkin):
"""
    return prompt


# Fungsi untuk mendapatkan kasus tes dari respons GPT.
def get_test_cases(api_key, model_name, prompt):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model = model_name,
        messages=[
            {"role": "system", "content": "Anda adalah asisten yang membantu yang menyediakan kasus uji gherkin Markdown format kedalam bahasa Indonesia."},
            {"role": "user", "content": prompt}
        ]
    )

    # Mengakses konten secara langsung karena responsnya akan dalam format teks
    test_cases = response.choices[0].message.content

    return test_cases

# Fungsi untuk mendapatkan mitigasi dari respons Azure Openai.
def get_test_cases_azure(azure_api_endpoint, azure_api_key, azure_api_version, azure_deployment_name, prompt):
    client = AzureOpenAI(
        azure_endpoint = azure_api_endpoint,
        api_key = azure_api_key,
        api_version = azure_api_version,
    )

    response = client.chat.completions.create(
        model = azure_deployment_name,
        messages=[
            {"role": "system", "content": "Anda adalah asisten yang membantu yang menyediakan kasus uji gherkin Markdown format kedalam bahasa Indonesia."},
            {"role": "user", "content": prompt}
        ]
    )

    # Mengakses konten secara langsung karena responsnya akan dalam format teks
    test_cases = response.choices[0].message.content

    return test_cases

# Fungsi untuk mendapatkan kasus tes dari respons model Google.
def get_test_cases_google(google_api_key, google_model, prompt):
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel(
        google_model,
        system_instruction="Anda adalah asisten yang membantu yang menyediakan kasus uji gherkin Markdown format kedalam bahasa Indonesia.",
    )
    response = model.generate_content(prompt)
    
    # Mengakses konten secara langsung karena responsnya akan dalam format teks
    test_cases = response.candidates[0].content.parts[0].text

    return test_cases

# Fungsi untuk mendapatkan kasus tes dari respons model Mistral.
def get_test_cases_mistral(mistral_api_key, mistral_model, prompt):
    client = MistralClient(api_key=mistral_api_key)

    response = client.chat(
        model = mistral_model,
        messages=[
            {"role": "system", "content": "Anda adalah asisten yang membantu yang menyediakan kasus uji gherkin Markdown format kedalam bahasa Indonesia."},
            {"role": "user", "content": prompt}
        ]
    )

    # Access the content directly as the response will be in text format
    test_cases = response.choices[0].message.content

    return test_cases