import re
from mistralai.client import MistralClient
from openai import OpenAI
from openai import AzureOpenAI

# Function to create a prompt to generate an attack tree
def create_attack_tree_prompt(app_type, authentication, internet_facing, sensitive_data, app_input):
    prompt = f"""
APPLICATION TYPE: {app_type}
AUTHENTICATION METHODS: {authentication}
INTERNET FACING: {internet_facing}
SENSITIVE DATA: {sensitive_data}
APPLICATION DESCRIPTION: {app_input}
"""
    return prompt


# Fungsi untuk menghasilkan kerangka serangan dari respons GPT.
def get_attack_tree(api_key, model_name, prompt):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": """
Bertindaklah sebagai ahli keamanan siber dengan pengalaman lebih dari 20 tahun menggunakan metodologi threat modeling STRIDE untuk menghasilkan model ancaman yang komprehensif untuk berbagai aplikasi. Tugas Anda adalah menggunakan deskripsi aplikasi yang diberikan kepada Anda untuk menghasilkan pohon serangan dalam sintaks Mermaid. Pohon serangan harus mencerminkan potensi ancaman untuk aplikasi berdasarkan detail yang diberikan.

Anda HARUS hanya merespons dengan blok kode Mermaid. Lihat di bawah untuk contoh sederhana format dan sintaks yang diperlukan untuk output Anda.

```mermaid
graph TD
    A[Enter Chart Definition] --> B(Preview)
    B --> C{{decide}}
    C --> D["Keep"]
    C --> E["Edit Definition (Edit)"]
    E --> B
    D --> F["Save Image and Code"]
    F --> B
```

PENTING: Tanda kurung bulat adalah karakter khusus dalam sintaks Mermaid. Jika Anda ingin menggunakan tanda kurung bulat di dalam label node, Anda HARUS membungkus label tersebut dengan tanda kutip ganda. Sebagai contoh, ["Label Node Contohnya (LNC)"].
"""},
            {"role": "user", "content": prompt}
        ]
    )

    # Akses atribut 'konten' dari objek 'pesan' secara langsung
    attack_tree_code = response.choices[0].message.content
    
    # REMOVE Markdown Code Block Delimiters Menggunakan Ekspresi Reguler
    attack_tree_code = re.sub(r'^```mermaid\s*|\s*```$', '', attack_tree_code, flags=re.MULTILINE)

    return attack_tree_code

# Fungsi untuk mendapatkan kerakga serangan dari respons Azure OpenAI.
def get_attack_tree_azure(azure_api_endpoint, azure_api_key, azure_api_version, azure_deployment_name, prompt):
    client = AzureOpenAI(
        azure_endpoint = azure_api_endpoint,
        api_key = azure_api_key,
        api_version = azure_api_version,
    )

    response = client.chat.completions.create(
        model = azure_deployment_name,
        messages=[
            {"role": "system", "content": """
Bertindaklah sebagai seorang ahli keamanan siber dengan pengalaman lebih dari 20 tahun menggunakan metodologi pemodelan ancaman STRIDE untuk menghasilkan model ancaman yang komprehensif untuk berbagai aplikasi. Tugas Anda adalah menggunakan deskripsi aplikasi yang diberikan kepada Anda untuk menghasilkan pohon serangan dalam sintaks Mermaid. Pohon serangan tersebut harus mencerminkan potensi ancaman untuk aplikasi berdasarkan detail yang diberikan.

Anda HARUS hanya merespons dengan blok kode Mermaid. Lihat di bawah ini untuk contoh sederhana dari format dan sintaks yang diperlukan untuk output Anda.

```mermaid
graph TD
    A[Enter Chart Definition] --> B(Preview)
    B --> C{{decide}}
    C --> D["Keep"]
    C --> E["Edit Definition (Edit)"]
    E --> B
    D --> F["Save Image and Code"]
    F --> B
```

PENTING: Tanda kurung bulat adalah karakter khusus dalam sintaks Mermaid. Jika Anda ingin menggunakan tanda kurung bulat di dalam label node, Anda HARUS membungkus label tersebut dengan tanda kutip ganda. Sebagai contoh, ["Label Node Contohnya (LNC)"].
"""},
            {"role": "user", "content": prompt}
        ]
    )

    # Access the 'content' attribute of the 'message' object directly
    attack_tree_code = response.choices[0].message.content
    
    # Remove Markdown code block delimiters using regular expression
    attack_tree_code = re.sub(r'^```mermaid\s*|\s*```$', '', attack_tree_code, flags=re.MULTILINE)

    return attack_tree_code

# Function to get attack tree from the Mistral model's response.
def get_attack_tree_mistral(mistral_api_key, mistral_model, prompt):
    client = MistralClient(api_key=mistral_api_key)

    response = client.chat(
        model=mistral_model,
        messages=[
            {"role": "system", "content": """
Bertindaklah sebagai seorang ahli keamanan siber dengan pengalaman lebih dari 20 tahun menggunakan metodologi pemodelan ancaman STRIDE untuk menghasilkan model ancaman yang komprehensif untuk berbagai aplikasi. Tugas Anda adalah menggunakan deskripsi aplikasi yang diberikan kepada Anda untuk menghasilkan pohon serangan dalam sintaks Mermaid. Pohon serangan tersebut harus mencerminkan potensi ancaman untuk aplikasi berdasarkan detail yang diberikan.

Anda HARUS hanya merespons dengan blok kode Mermaid. Lihat di bawah ini untuk contoh sederhana dari format dan sintaks yang diperlukan untuk output Anda.
```mermaid
graph TD
    A[Enter Chart Definition] --> B(Preview)
    B --> C{{decide}}
    C --> D["Keep"]
    C --> E["Edit Definition (Edit)"]
    E --> B
    D --> F["Save Image and Code"]
    F --> B
```

PENTING: Tanda kurung bulat adalah karakter khusus dalam sintaks Mermaid. Jika Anda ingin menggunakan tanda kurung bulat di dalam label node, Anda HARUS membungkus label tersebut dengan tanda kutip ganda. Sebagai contoh, ["Label Node Contohnya (LNC)"].
"""},
            {"role": "user", "content": prompt}
        ]
    )

    # Akses atribut 'konten' dari objek 'pesan' secara langsung
    attack_tree_code = response.choices[0].message.content
    
    # Hapus pembatas blok kode markdown menggunakan ekspresi reguler
    attack_tree_code = re.sub(r'^```mermaid\s*|\s*```$', '', attack_tree_code, flags=re.MULTILINE)

    return attack_tree_code