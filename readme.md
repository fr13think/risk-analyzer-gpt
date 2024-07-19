## Risk Analyzer GPT

Risk Analyzer GPT adalah alat pemodelan ancaman bertenaga AI yang memanfaatkan model bahasa besar (LLM) untuk menghasilkan model ancaman dan menyerang pohon untuk aplikasi yang diberikan berdasarkan metodologi langkah.Pengguna memberikan detail aplikasi, seperti jenis aplikasi, metode otentikasi, dan apakah aplikasi tersebut menghadap ke internet atau memproses data sensitif.Model kemudian menghasilkan outputnya berdasarkan informasi yang disediakan.

## Installation

### Option 1: Cloning the Repository

1. Clone this repository:

    ```bash
    git clone https://github.com/fr13think/risk-analyzer-gpt.git
    ```

2. Change to the cloned repository directory:

    ```bash
    cd risk-analyzer-gpt
    ```

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

### Option 2: Using Docker Container

1. Pull the Docker image from Docker Hub:

    ```bash
    docker pull fr13think/stridegpt:latest
    ```

## Usage

### Option 1: Running the Streamlit App Locally

1. Run the Streamlit app:

    ```bash
    streamlit run main.py
    ```

2. Open the app in your web browser using the provided URL.

3. Follow the steps in the Streamlit interface to use Risk Analyzer GPT.

### Option 2: Using Docker Container

1. Run the Docker container:

    ```bash
    docker run -p 8501:8501 fr13think/stridegpt
    ```
    This command will start the container and map port 8501 (default for Streamlit apps) from the container to your host machine.

2. Open a web browser and navigate to `http://localhost:8501` to access the app running inside the container.

3. Follow the steps in the Streamlit interface to use Rizk Analyzer GPT.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)