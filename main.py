#main.py

import base64
import streamlit as st
import streamlit.components.v1 as components

from threat_model import create_threat_model_prompt, get_threat_model, get_threat_model_azure, get_threat_model_google, get_threat_model_mistral, json_to_markdown, get_image_analysis, create_image_analysis_prompt
from attack_tree import create_attack_tree_prompt, get_attack_tree, get_attack_tree_azure, get_attack_tree_mistral
from mitigations import create_mitigations_prompt, get_mitigations, get_mitigations_azure, get_mitigations_google, get_mitigations_mistral
from test_cases import create_test_cases_prompt, get_test_cases, get_test_cases_azure, get_test_cases_google, get_test_cases_mistral
from dread import create_dread_assessment_prompt, get_dread_assessment, get_dread_assessment_azure, get_dread_assessment_google, get_dread_assessment_mistral, dread_json_to_markdown

html_code = """
    <meta name="dicoding:email" content="yudhae@gmail.com">
"""

# ------------------ Helper Functions ------------------ #

# Fungsi untuk mendapatkan input pengguna dari deskripsi aplikasi dan detail utama
def get_input():
       input_text = st.text_area(
           label="Jelaskan aplikasi yang akan didemokan",
           placeholder="Masukkan detail aplikasi Anda ...",
           height=150,
           key="app_desc",
           help="Harap berikan deskripsi yang detail tentang aplikasi, termasuk tujuan aplikasi, teknologi yang digunakan, dan informasi lain yang relevan.",
       )

       st.session_state['app_input'] = input_text

       return input_text

# Fungsi membuat diagram Mermaid
def mermaid(code: str, height: int = 500) -> None:
    components.html(
        f"""
        <pre class="mermaid" style="height: {height}px;">
            {code}
        </pre>

        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
        """,
        height=height,
    )


# ------------------ Streamlit UI Configuration ------------------ #

st.set_page_config(
    page_title="RISK ANALYZER GPT",
    page_icon=":shield:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------ Sidebar ------------------ #

st.sidebar.image("Logoo.png")

# Tambahkan instruksi tentang cara menggunakan aplikasi ke bilah sisi
st.sidebar.header("Cara Penggunaan Risk Analyzer GPT")

with st.sidebar:
    # Tambahkan bidang input pemilihan model ke bilah samping
    model_provider = st.selectbox(
        "Pilih penyediaan model pilihan Anda (disarankan Menggunakan Mistral API karena Gratis):",
        ["OpenAI API", "Azure OpenAI Service", "Google AI API", "Mistral API"],
        key="model_provider",
        help="Pilih penyedia model yang ingin Anda gunakan.Ini akan menentukan model yang tersedia untuk seleksi.",
    )

    if model_provider == "OpenAI API":
        st.markdown(
        """
    1. Masukkan [OpenAI API key](https://platform.openai.com/account/api-keys) dan pilih di bawah ini 🔑
    2. Berikan rincian aplikasi yang ingin Anda hasilkan terhadap bentuk serangan  📝
    3. Menghasilkan daftar ancaman, menyerang pohon dan/atau mengurangi kontrol untuk aplikasi Anda 🚀
    """
    )
        # Tambahkan bidang input kunci API OpenAI ke bilah samping
        openai_api_key = st.text_input(
            "Masukkan OpenAI API Key Anda:",
            type="password",
            help="Anda dapat menemukan openai API Key Anda di [OpenAI dashboard](https://platform.openai.com/account/api-keys).",
        )

        # Tambahkan bidang input pemilihan model ke bilah samping
        selected_model = st.selectbox(
            "Pilih model yang ingin Anda gunakan:",
            ["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
            key="selected_model",
            help="OpenAI telah pindah ke peningkatan model berkelanjutan menjadi `GPT-3.5-turbo`,` GPT-4` dan `GPT-4-turbo` ke versi terbaru yang tersedia dari setiap model.",
        )

    if model_provider == "Azure OpenAI Service":
        st.markdown(
        """
    1. Masukkan API Key Openai Azure Anda, Titik Akhir dan Nama Penempatan di bawah ini 🔑
    2. Berikan rincian aplikasi yang ingin Anda hasilkan terhadap bentuk serangan  📝
    3. Menghasilkan daftar ancaman, menyerang pohon dan/atau mengurangi kontrol untuk aplikasi Anda 🚀
    """
    )

        # Tambahkan bidang input kunci API Azure OpenAi ke bilah samping
        azure_api_key = st.text_input(
            "Azure OpenAI API key:",
            type="password",
            help="You can find your Azure OpenAI API key on the [Azure portal](https://portal.azure.com/).",
        )
        
        # Tambahkan bidang input titik akhir Azure OpenAi ke bilah samping
        azure_api_endpoint = st.text_input(
            "Azure OpenAI endpoint:",
            help="Example endpoint: https://YOUR_RESOURCE_NAME.openai.azure.com/",
        )

        # Tambahkan bidang input nama penyebaran Azure OpenAi ke bilah samping
        azure_deployment_name = st.text_input(
            "Nama Deployment:",
        )
        
        st.info("Harap dicatat bahwa Anda harus menggunakan penyebaran model preview 1106.")

        azure_api_version = '2023-12-01-preview' # Update this as needed

        st.write(f"Azure API Version: {azure_api_version}")

    if model_provider == "Google AI API":
        st.markdown(
        """
    1. Masukkan [Google AI API Key Anda] (https://makersuite.google.com/app/apikey) dan model di bawah ini🔑
    2. Berikan rincian aplikasi yang ingin Anda hasilkan terhadap bentuk serangan  📝
    3. Menghasilkan daftar ancaman, menyerang pohon dan/atau mengurangi kontrol untuk aplikasi Anda 🚀
    """
    )
        # Tambahkan bidang input kunci API OpenAI ke bilah samping
        google_api_key = st.text_input(
            "Masukkan Google AI API key:",
            type="password",
            help="Anda dapat menghasilkan kunci API Google AI di [Google AI Studio](https://makersuite.google.com/app/apikey).",
        )

        # Tambahkan bidang input pemilihan model ke bilah samping
        google_model = st.selectbox(
            "Pilih model yang ingin Anda gunakan:",
            ["gemini-1.5-pro-latest"],
            key="selected_model",
        )

    if model_provider == "Mistral API":
        st.markdown(
        """
    1. Masukkan [Mistral API Key] Anda (https://console.mistral.ai/api-keys/) akses link tersbut untuk memperoleh 🔑
    2. Berikan rincian aplikasi yang ingin Anda hasilkan terhadap bentuk serangan  📝
    3. Menghasilkan daftar ancaman, menyerang pohon dan/atau mengurangi kontrol untuk aplikasi Anda 🚀
    """
    )
        # ADD Openai API Key Input Field ke bilah samping
        mistral_api_key = st.text_input(
            "Masukkan Mistral API key:",
            type="password",
            help="Anda dapat menghasilkan kunci API Mistral di [Mistral console](https://console.mistral.ai/api-keys/).",
        )

        # Tambahkan bidang input pemilihan model ke bilah samping
        mistral_model = st.selectbox(
            "Pilih model yang ingin Anda gunakan:",
            ["mistral-large-latest", "mistral-small-latest"],
            key="selected_model",
        )

    st.markdown("""---""")

# Tambahkan bagian "Tentang" ke bilah samping
st.sidebar.header("About")

with st.sidebar:
    st.markdown(
        "Selamat datang di Risk Analyzer GPT, aplikasi risk analyzer berbasis AI yang dirancang untuk membantu Anda menghasilkan model ancaman menggunakan teknologi AI."
    )
    st.markdown(
        "Pemodelan ancaman adalah aktivitas utama dalam siklus pengembangan perangkat lunak, tetapi sering diabaikan atau dijalankan dengan buruk.Risk Analyzer GPT bertujuan untuk membantu tim menghasilkan model ancaman yang lebih komprehensif dengan memanfaatkan (LLM) untuk menghasilkan daftar ancaman, kerangka serangan dan/atau mitigasi kontrol untuk aplikasi berdasarkan detail yang disediakan."
    )
    st.markdown("Created by [Yudha Elfransyah](https://id.linkedin.com/in/yudha-elfransyah-b6913737/).")
    st.markdown("<meta name="dicoding:email" content="yudhae@gmail.com">")
    # Tambahkan tautan "Star on GitHub" ke bilah sisi
    st.sidebar.markdown(
        "⭐ Star on GitHub: [![Star on GitHub](https://img.shields.io/github/stars/fr13think/risk-analyzer-gpt?style=social)](https://github.com/fr13think/risk-analyzer-gpt)"
    )
    st.markdown("""---""")


# Tambahkan "Contoh Deskripsi Aplikasi" ke bilah sisi
st.sidebar.header("Contoh Deskripsi Aplikasi")

with st.sidebar:
    st.markdown(
        "Di bawah ini adalah contoh deskripsi aplikasi yang dapat Anda gunakan untuk menguji langkah GPT:"
    )
    st.markdown(
        "> Aplikasi web yang memungkinkan pengguna untuk membuat, menyimpan, dan berbagi catatan pribadi. Aplikasi ini dibangun menggunakan kerangka kerja React Frontend dan backend Node.js dengan database MongoDB. Pengguna dapat mendaftar untuk akun dan masuk menggunakan OAuth2 dengan Google atau Facebook. Catatan dienkripsi saat istirahat dan hanya dapat diakses oleh pengguna yang membuatnya. Aplikasi ini juga mendukung kolaborasi real-time pada catatan dengan pengguna lain."
    )
    st.markdown("""---""")

# Add "FAQs" section to the sidebar
st.sidebar.header("FAQs")

with st.sidebar:
    st.markdown(
        """
    ### **Apa Risk Analyzer GPT itu?**
    Risk Analyzer GPT adalah metodologi pemodelan ancaman yang membantu mengidentifikasi dan mengkategorikan risiko keamanan potensial dalam aplikasi perangkat lunak.
    """
    )
    st.markdown(
        """
    ### **Bagaimana cara kerja GPT bekerja?**
    Saat Anda memasukkan deskripsi aplikasi dan detail lain yang relevan, alat ini akan menggunakan model GPT untuk menghasilkan model ancaman untuk aplikasi Anda.Model ini menggunakan deskripsi dan detail aplikasi untuk menghasilkan daftar ancaman potensial dan kemudian mengkategorikan setiap ancaman sesuai dengan metodologi langkah.
    """
    )
    st.markdown(
        """
    ### **Apakah Anda menyimpan detail aplikasi yang disediakan?**
    Tidak, Langkah Risk Analyzer GPT tidak menyimpan deskripsi aplikasi Anda atau detail lainnya.Semua data yang dimasukkan dihapus setelah Anda menutup tab browser.
    """
    )
    st.markdown(
        """
    ### **Mengapa butuh waktu lama untuk menghasilkan model ancaman?**
    Jika Anda menggunakan kunci API OpenAI gratis, perlu waktu untuk menghasilkan model ancaman.Ini karena kunci API gratis memiliki batas tingkat yang ketat.Untuk mempercepat prosesnya, Anda dapat menggunakan kunci API berbayar.
    """
    )
    st.markdown(
        """
    ### **Apakah model ancaman 100% akurat?**
    Tidak, model ancaman tidak 100% akurat.Stride GPT menggunakan Large Language Models (LLM) GPT untuk menghasilkan outputnya.Model GPT sangat kuat, tetapi kadang -kadang membuat kesalahan dan rentan terhadap '100% ketidakpastian' (menghasilkan konten yang tidak relevan atau tidak akurat).Harap gunakan output hanya sebagai titik awal untuk mengidentifikasi dan mengatasi potensi risiko keamanan dalam aplikasi Anda.
    """
    )
    st.markdown(
        """
    ### **Bagaimana cara meningkatkan keakuratan model ancaman?**
    Anda dapat meningkatkan keakuratan model ancaman dengan memberikan deskripsi terperinci tentang aplikasi dan memilih jenis aplikasi yang benar, metode otentikasi, dan detail relevan lainnya.Semakin banyak informasi yang Anda berikan, semakin akurat model ancaman.
    """
    )


# ------------------ Main App UI ------------------ #

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Model ancaman", "Kerangka Serangan", "Mitigasi", "DREAD", "Bentuk Kasus"])

with tab1:
    st.markdown("""
Model ancaman membantu mengidentifikasi dan mengevaluasi potensi ancaman keamanan terhadap aplikasi / sistem.Ini memberikan pendekatan sistematis untuk 
Memahami kemungkinan kerentanan dan vektor serangan.Gunakan tab ini untuk menghasilkan model ancaman menggunakan metodologi langkah.
""")
    st.markdown("""---""")
    
    # Dua tata letak kolom untuk konten aplikasi utama
    col1, col2 = st.columns([1, 1])

    # Inisialisasi app_input dalam status sesi jika tidak ada
    if 'app_input' not in st.session_state:
        st.session_state['app_input'] = ''

    # Jika Penyedia Model adalah OpenAI API dan modelnya adalah GPT-4-Turbo atau GPT-4O
    with col1:
        if model_provider == "OpenAI API" and selected_model in ["gpt-4-turbo", "gpt-4o"]:
            uploaded_file = st.file_uploader("Upload architecture diagram", type=["jpg", "jpeg", "png"])

            if uploaded_file is not None:
                if not openai_api_key:
                    st.error("Harap masukkan OpenAI API key Anda untuk menganalisis gambar.")
                else:
                    if 'uploaded_file' not in st.session_state or st.session_state.uploaded_file != uploaded_file:
                        st.session_state.uploaded_file = uploaded_file
                        with st.spinner("Menganalisis gambar yang diunggah..."):
                            def encode_image(uploaded_file):
                                return base64.b64encode(uploaded_file.read()).decode('utf-8')

                            base64_image = encode_image(uploaded_file)

                            image_analysis_prompt = create_image_analysis_prompt()

                            try:
                                image_analysis_output = get_image_analysis(openai_api_key, selected_model, image_analysis_prompt, base64_image)
                                if image_analysis_output and 'choices' in image_analysis_output and image_analysis_output['choices'][0]['message']['content']:
                                    image_analysis_content = image_analysis_output['choices'][0]['message']['content']
                                    st.session_state.image_analysis_content = image_analysis_content
                                    # Perbarui status sesi app_input
                                    st.session_state['app_input'] = image_analysis_content
                                else:
                                    st.error("Gagal menganalisis gambar.Silakan periksa kunci API dan coba lagi.")
                            except KeyError as e:
                                st.error("Gagal menganalisis gambar.Silakan periksa kunci API dan coba lagi.")
                                print(f"Error: {e}")
                            except Exception as e:
                                st.error("Terjadi kesalahan yang tidak terduga saat menganalisis gambar.")
                                print(f"Error: {e}")

            # Gunakan text_area dengan nilai keadaan sesi dan perbarui status sesi saat perubahan
            app_input = st.text_area(
                label="Jelaskan aplikasi yang akan dimodelkan",
                value=st.session_state['app_input'],
                key="app_input_widget",
                help="Harap berikan deskripsi terperinci tentang aplikasi, termasuk tujuan aplikasi, teknologi yang digunakan, dan informasi lain yang relevan.",
            )
            # Perbarui keadaan sesi hanya jika konten area teks telah berubah
            if app_input != st.session_state['app_input']:
                st.session_state['app_input'] = app_input

        else:
            # Untuk penyedia atau model model lainnya, gunakan fungsi get_input ()
            app_input = get_input()
            # Update session state
            st.session_state['app_input'] = app_input

    # Pastikan app_input selalu up to date dalam keadaan sesi
    app_input = st.session_state['app_input']



        # Buat bidang input untuk detail tambahan
    with col2:
            app_type = st.selectbox(
                label="Select the application type",
                options=[
                    "Web application",
                    "Mobile application",
                    "Desktop application",
                    "Cloud application",
                    "IoT application",
                    "Other",
                ],
                key="app_type",
            )

            sensitive_data = st.selectbox(
                label="Apa tingkat sensitivitas tertinggi dari data yang diproses oleh aplikasi?",
                options=[
                    "Sangat rahasia",
                    "Rahasia",
                    "Rahasia",
                    "Terbatas",
                    "Tidak diklasifikasikan",
                    "Tidak ada",
                ],
                key="sensitive_data",
            )

        # Create input fields for internet_facing and authentication
            internet_facing = st.selectbox(
                label="Apakah aplikasi menggunakan internet?",
                options=["Yes", "No"],
                key="internet_facing",
            )

            authentication = st.multiselect(
                "Metode otentikasi apa yang didukung oleh aplikasi?",
                ["SSO", "MFA", "OAUTH2", "Basic", "Tidak ada"],
                key="authentication",
            )



    # ------------------ Threat Model Generation ------------------ #

    # Buat tombol kirim untuk pemodelan ancaman
    threat_model_submit_button = st.button(label="Generate Threat Model")

    # Jika tombol Model Ancaman Generate diklik dan pengguna telah memberikan deskripsi aplikasi
    if threat_model_submit_button and st.session_state.get('app_input'):
        app_input = st.session_state['app_input']  # Ambil dari keadaan sesi
# Menghasilkan prompt menggunakan fungsi create_prompt
        threat_model_prompt = create_threat_model_prompt(app_type, authentication, internet_facing, sensitive_data, app_input)

        # Tunjukkan pemintal saat menghasilkan model ancaman
        with st.spinner("Menganalisis potensi ancaman ..."):
            max_retries = 3
            retry_count = 0
            while retry_count < max_retries:
                try:
                    # Hubungkan fungsi get_threat_model yang relevan dengan prompt yang dihasilkan
                    if model_provider == "Azure OpenAI Service":
                        model_output = get_threat_model_azure(azure_api_endpoint, azure_api_key, azure_api_version, azure_deployment_name, threat_model_prompt)
                    elif model_provider == "OpenAI API":
                        model_output = get_threat_model(openai_api_key, selected_model, threat_model_prompt)
                    elif model_provider == "Google AI API":
                        model_output = get_threat_model_google(google_api_key, google_model, threat_model_prompt)
                    elif model_provider == "Mistral API":
                        model_output = get_threat_model_mistral(mistral_api_key, mistral_model, threat_model_prompt)

                    # Mengakses model ancaman dan saran peningkatan dari konten yang diuraikan
                    threat_model = model_output.get("threat_model", [])
                    improvement_suggestions = model_output.get("improvement_suggestions", [])

                    # Simpan model ancaman ke status sesi untuk digunakan nanti dalam mitigasi
                    st.session_state['threat_model'] = threat_model
                    break  # Keluar dari loop jika berhasil
                except Exception as e:
                    retry_count += 1
                    if retry_count == max_retries:
                        st.error(f"Error generating threat model after {max_retries} attempts: {e}")
                        threat_model = []
                        improvement_suggestions = []
                    else:
                        st.warning(f"Error generating threat model. Retrying attempt {retry_count+1}/{max_retries}...")

        # Konversi model ancaman JSON menjadi penurunan harga
        markdown_output = json_to_markdown(threat_model, improvement_suggestions)

        # Tampilkan model ancaman dalam penurunan harga
        st.markdown(markdown_output)

        # Tambahkan tombol untuk memungkinkan pengguna mengunduh output sebagai file markdown
        st.download_button(
            label="Unduh model ancaman",
            data=markdown_output,
            file_name="export_threat_model.md",
            mime="text/markdown",
       )

# Jika tombol Kirim diklik dan pengguna belum memberikan deskripsi aplikasi
if threat_model_submit_button and not st.session_state.get('app_input'):
    st.error("Harap masukkan detail aplikasi Anda sebelum mengirimkan.")



# ------------------ Attack Tree Generation ------------------ #

with tab2:
    st.markdown("""
Pohon serangan adalah cara terstruktur untuk menganalisis keamanan suatu sistem.Mereka mewakili potensi skenario serangan dalam format hierarkis, dengan tujuan akhir penyerang di akar dan berbagai jalur untuk mencapai tujuan itu sebagai cabang.Ini membantu dalam memahami kerentanan sistem dan memprioritaskan upaya mitigasi.
""")
    st.markdown("""---""")
    if model_provider == "Google AI API":
        st.warning("⚠️Filter keselamatan Google mencegah generasi pohon serangan yang andal.Harap gunakan penyedia model yang berbeda.")
    else:
        if model_provider == "Mistral API" and mistral_model == "mistral-small-latest":
            st.warning("⚠️ Mistral Small tidak andal menghasilkan kode putri duyung yang benar secara sintaksis.Harap gunakan model besar mistral untuk menghasilkan pohon serangan, atau pilih penyedia model yang berbeda. ")
        
        # Buat tombol Kirim untuk Pohon Serangan
        attack_tree_submit_button = st.button(label="Generate Attack Tree")
        
        # Jika tombol Generate Attack Tree diklik dan pengguna telah memberikan deskripsi aplikasi
        if attack_tree_submit_button and st.session_state.get('app_input'):
            app_input = st.session_state.get('app_input')
            # Menghasilkan prompt menggunakan fungsi create_attack_tree_prompt
            attack_tree_prompt = create_attack_tree_prompt(app_type, authentication, internet_facing, sensitive_data, app_input)

            # Tunjukkan pemintal saat menghasilkan pohon serangan
            with st.spinner("Menghasilkan Pohon Serangan ..."):
                try:
                    # Hubungi fungsi get_attack_tree yang relevan dengan prompt yang dihasilkan
                    if model_provider == "Azure OpenAI Service":
                        mermaid_code = get_attack_tree_azure(azure_api_endpoint, azure_api_key, azure_api_version, azure_deployment_name, attack_tree_prompt)
                    elif model_provider == "OpenAI API":
                        mermaid_code = get_attack_tree(openai_api_key, selected_model, attack_tree_prompt)
                    elif model_provider == "Mistral API":
                        mermaid_code = get_attack_tree_mistral(mistral_api_key, mistral_model, attack_tree_prompt)

                    # Tampilkan kode pohon serangan yang dihasilkan
                    st.write("Kerangka Kode Pohon Serangan:")
                    st.code(mermaid_code)

                    # Visualisasikan Pohon Serangan Menggunakan Komponen Kustom Mermaid
                    st.write("Pratinjau Diagram Pohon Serangan:")
                    mermaid(mermaid_code)
                    
                    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
                    
                    with col1:              
                        # Tambahkan tombol untuk memungkinkan pengguna mengunduh kode putri duyung
                        st.download_button(
                            label="Unduh kode diagram",
                            data=mermaid_code,
                            file_name="export_attack_tree.md",
                            mime="text/plain",
                            help="Unduh kode putri duyung untuk diagram serangan pohon."
                        )

                    with col2:
                        # Tambahkan tombol untuk memungkinkan pengguna membuka Editor Langsung Putri Duyung
                        mermaid_live_button = st.link_button("Open Mermaid Live", "https://mermaid.live")
                    
                    with col3:
                        # Blank placeholder
                        st.write("")
                    
                    with col4:
                        # Blank placeholder
                        st.write("")
                    
                    with col5:
                        # Blank placeholder
                        st.write("")

                except Exception as e:
                    st.error(f"Kesalahan menghasilkan pohon serangan: {e}")


# ------------------ Mitigations Generation ------------------ #

with tab3:
    st.markdown("""
Gunakan tab ini untuk menghasilkan mitigasi potensial untuk ancaman yang diidentifikasi dalam model ancaman.Mitigasi adalah kontrol keamanan atau
Penanggulangan yang dapat membantu mengurangi kemungkinan atau dampak dari ancaman keamanan.Mitigasi yang dihasilkan dapat digunakan untuk meningkatkan
Postur keamanan aplikasi dan melindungi terhadap potensi serangan.
""")
    st.markdown("""---""")
    
    # Buat tombol Kirim untuk mitigasi
    mitigations_submit_button = st.button(label="Saran mitigasi")

    # Jika tombol Mitigasi Saran diklik dan pengguna telah mengidentifikasi ancaman
    if mitigations_submit_button:
        # Periksa apakah ada data ancaman_model
        if 'threat_model' in st.session_state and st.session_state['threat_model']:
            # Konversi data ancaman_model menjadi daftar penurunan harga
            threats_markdown = json_to_markdown(st.session_state['threat_model'], [])
            # Menghasilkan prompt menggunakan fungsi create_mitigations_prompt
            mitigations_prompt = create_mitigations_prompt(threats_markdown)

            # Tunjukkan pemintal sambil menyarankan mitigasi
            with st.spinner("Menyarankan mitigasi ..."):
                max_retries = 3
                retry_count = 0
                while retry_count < max_retries:
                    try:
                        # Panggil fungsi get_mitigations yang relevan dengan prompt yang dihasilkan
                        if model_provider == "Azure OpenAI Service":
                            mitigations_markdown = get_mitigations_azure(azure_api_endpoint, azure_api_key, azure_api_version, azure_deployment_name, mitigations_prompt)
                        elif model_provider == "OpenAI API":
                            mitigations_markdown = get_mitigations(openai_api_key, selected_model, mitigations_prompt)
                        elif model_provider == "Google AI API":
                            mitigations_markdown = get_mitigations_google(google_api_key, google_model, mitigations_prompt)
                        elif model_provider == "Mistral API":
                            mitigations_markdown = get_mitigations_mistral(mistral_api_key, mistral_model, mitigations_prompt)

                        # Tampilkan mitigasi yang disarankan dalam penurunan harga
                        st.markdown(mitigations_markdown)
                        break  # Keluar dari loop jika berhasil
                    except Exception as e:
                        retry_count += 1
                        if retry_count == max_retries:
                            st.error(f"Kesalahan menyarankan mitigasi setelahnya {max_retries} upaya: {e}")
                            mitigations_markdown = ""
                        else:
                            st.warning(f"Kesalahan menyarankan mitigasi.Mencoba lagi upaya {retry_count+1}/{max_retries}...")
            
            st.markdown("")

            # Tambahkan tombol untuk memungkinkan pengguna mengunduh mitigasi sebagai file markdown
            st.download_button(
                label="Download Mitigations",
                data=mitigations_markdown,
                file_name="export_mitigations.md",
                mime="text/markdown",
            )
        else:
            st.error("Harap hasilkan model ancaman terlebih dahulu sebelum menyarankan mitigasi.")

# ------------------ DREAD Risk Assessment Generation ------------------ #
with tab4:
    st.markdown("""
DREAD adalah metode untuk mengevaluasi dan memprioritaskan risiko yang terkait dengan ancaman keamanan.Ini menilai ancaman berdasarkan ** Damage Potential** Potensi Kerusakan, 
** Reproducibility ** seberapa mudah ancaman, ** Exploitability ** seberapa mudah bagi penyerang, ** Affected Users ** seberapa banyak pengguna yang akan terkena dampak, dan ** Discoverability ** seberapa mudah ancaman dapat dideteksi. DREAD membantu dalam menentukan tingkat risiko keseluruhan dan 
Berfokus pada ancaman paling kritis terlebih dahulu. Gunakan tab ini untuk melakukan penilaian risiko DREAD untuk aplikasi / sistem Anda.
""")
    st.markdown("""---""")
    
    # Buat tombol kirim untuk penilaian risiko DREAD
    dread_assessment_submit_button = st.button(label="Menghasilkan penilaian risiko DREAD")
    # Jika tombol Penilaian Risiko Generate Dread diklik dan pengguna telah mengidentifikasi ancaman
    if dread_assessment_submit_button:
        # Check if threat_model data exists
        if 'threat_model' in st.session_state and st.session_state['threat_model']:
            # Convert the threat_model data into a Markdown list
            threats_markdown = json_to_markdown(st.session_state['threat_model'], [])
            # Generate the prompt using the create_dread_assessment_prompt function
            dread_assessment_prompt = create_dread_assessment_prompt(threats_markdown)
            # Show a spinner while generating DREAD Risk Assessment
            with st.spinner("Menghasilkan Penilaian Risiko Dread ..."):
                max_retries = 3
                retry_count = 0
                while retry_count < max_retries:
                    try:
                        # Hubungi fungsi get_dread_assessment yang relevan dengan prompt yang dihasilkan
                        if model_provider == "Azure OpenAI Service":
                            dread_assessment = get_dread_assessment_azure(azure_api_endpoint, azure_api_key, azure_api_version, azure_deployment_name, dread_assessment_prompt)
                        elif model_provider == "OpenAI API":
                            dread_assessment = get_dread_assessment(openai_api_key, selected_model, dread_assessment_prompt)
                        elif model_provider == "Google AI API":
                            dread_assessment = get_dread_assessment_google(google_api_key, google_model, dread_assessment_prompt)
                        elif model_provider == "Mistral API":
                            dread_assessment = get_dread_assessment_mistral(mistral_api_key, mistral_model, dread_assessment_prompt)
                        # Simpan DREAD ke status sesi untuk digunakan nanti dalam kasus uji
                        st.session_state['dread_assessment'] = dread_assessment
                        break  # Keluar dari loop jika berhasil
                    except Exception as e:
                        retry_count += 1
                        if retry_count == max_retries:
                            st.error(f"Kesalahan menghasilkan penilaian risiko DREAD setelah {max_retries} upaya: {e}")
                            dread_assessment = []
                        else:
                            st.warning(f"Kesalahan menghasilkan penilaian risiko DREAD.Mencoba lagi upaya {retry_count+1}/{max_retries}...")
            # Convert the DREAD assessment JSON to Markdown
            dread_assessment_markdown = dread_json_to_markdown(dread_assessment)
            # Display the DREAD assessment in Markdown
            st.markdown(dread_assessment_markdown)
            # Add a button to allow the user to download the test cases as a Markdown file
            st.download_button(
                label="Unduh Penilaian Risiko Dread",
                data=dread_assessment_markdown,
                file_name="export_dread_assessment.md",
                mime="text/markdown",
            )
        else:
            st.error("Harap hasilkan model ancaman terlebih dahulu sebelum meminta penilaian risiko DREAD.")


# ------------------ Test Cases Generation ------------------ #

with tab5:
    st.markdown("""
Kasus uji digunakan untuk memvalidasi keamanan aplikasi dan memastikan bahwa kerentanan potensial diidentifikasi dan 
ditangani. Pada bagian ini memungkinkan Anda untuk menghasilkan kasus uji menggunakan sintaks Gherkin. Gherkin menyediakan cara terstruktur untuk menggambarkan aplikasi 
Perilaku dalam teks biasa, menggunakan sintaks sederhana dari pernyataan yang diberikan-kemudian. Ini membantu dalam membuat tes yang jelas dan dapat dieksekusi 
skenario.
""")
    st.markdown("""---""")
                
    # CBuat tombol kirim untuk kasus uji
    test_cases_submit_button = st.button(label="Menghasilkan kasus uji")

    # Jika tombol Generate Test Case diklik dan pengguna telah mengidentifikasi ancaman
    if test_cases_submit_button:
        # Periksa apakah ada data ancaman_model
        if 'threat_model' in st.session_state and st.session_state['threat_model']:
            # Convert the threat_model data into a Markdown list
            threats_markdown = json_to_markdown(st.session_state['threat_model'], [])
            # Generate the prompt using the create_test_cases_prompt function
            test_cases_prompt = create_test_cases_prompt(threats_markdown)

            # Tunjukkan pemintal saat menghasilkan test case
            with st.spinner("Menghasilkan kasus uji ..."):
                max_retries = 3
                retry_count = 0
                while retry_count < max_retries:
                    try:
                        # Panggil ke fungsi get_test_cases yang relevan dengan prompt yang dihasilkan
                        if model_provider == "Azure OpenAI Service":
                            test_cases_markdown = get_test_cases_azure(azure_api_endpoint, azure_api_key, azure_api_version, azure_deployment_name, test_cases_prompt)
                        elif model_provider == "OpenAI API":
                            test_cases_markdown = get_test_cases(openai_api_key, selected_model, test_cases_prompt)
                        elif model_provider == "Google AI API":
                            test_cases_markdown = get_test_cases_google(google_api_key, google_model, test_cases_prompt)
                        elif model_provider == "Mistral API":
                            test_cases_markdown = get_test_cases_mistral(mistral_api_key, mistral_model, test_cases_prompt)

                        # Display the suggested mitigations in Markdown
                        st.markdown(test_cases_markdown)
                        break  # Exit the loop if successful
                    except Exception as e:
                        retry_count += 1
                        if retry_count == max_retries:
                            st.error(f"Kasus uji yang menghasilkan kesalahan setelah{max_retries} upaya: {e}")
                            test_cases_markdown = ""
                        else:
                            st.warning(f"Kasus uji yang menghasilkan kesalahan.Mencoba lagi upaya {retry_count+1}/{max_retries}...")
            
            st.markdown("")

            # Tambahkan tombol untuk memungkinkan pengguna mengunduh kasus uji sebagai file penurunan harga
            st.download_button(
                label="Download Test Cases",
                data=test_cases_markdown,
                file_name="export_test_case.md",
                mime="text/markdown",
            )
        else:
            st.error("Harap hasilkan model ancaman terlebih dahulu sebelum meminta kasus uji.")