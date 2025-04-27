# Soap_notes-generation_RAG


## Step 1: Create and Set Up the Project Environment

### 1. Install Python
Ensure that you have Python 3.7 or higher installed. You can check this by running:

```
python --version
```
### 2. Create a Virtual Environment (Optional but Recommended)
Create a new virtual environment to keep the dependencies isolated:

```
python -m venv venv

```
Activate it:

On Windows:

```
.\venv\Scripts\activate
```
On macOS/Linux:

```
source venv/bin/activate
```
### 3 : Install Required Libraries
Next, install all the required libraries to run the FastAPI app and the Streamlit front-end. You can use pip to install them.

Create a requirements.txt file with the following content:

```
fastapi==0.95.0
uvicorn==0.22.0
pydantic==1.10.2
datasets==2.9.0
langchain==0.0.136
faiss-cpu==1.7.4
openai==0.27.0
requests==2.28.2
streamlit==1.19.0
Pillow==9.3.0
```
Install the dependencies:
```
pip install -r requirements.txt

```
### 3: Set Up the FastAPI Backend (fast_api.py)
Create a new file named fast_api.py and paste the provided code into it. This file will set up the FastAPI server.

Make sure to:

Replace the OPENAI_API_KEY with your own OpenAI API key.

Ensure that the soap_notes dataset is available on the datasets library (the code uses the adesouza1/soap_notes dataset).

Start the FastAPI server using uvicorn.

To run the FastAPI server:
```
uvicorn fast_api:app --reload
```
This will start the FastAPI server locally at http://localhost:8000.

### 4: Set Up the Streamlit Frontend (streamlit_app.py)
Create a new file named streamlit_app.py and paste the provided Streamlit code into it. This file will allow you to interact with the FastAPI backend via a clean, modern UI.

To run the Streamlit app:

```
streamlit run streamlit_app.py

```
This will open the Streamlit frontend in your browser at http://localhost:8501. Here, you can input a doctor-patient conversation, which will then be sent to the FastAPI server to generate a SOAP note.

### 5: Check API Functionality
The FastAPI app exposes an endpoint at POST /generate_soap_note. When a conversation is sent as a JSON payload, it will use the provided prompt template and generate a SOAP note by retrieving relevant past SOAP notes from the FAISS vector store.

### 6: Accessing the FastAPI Server and Frontend
The FastAPI server should be accessible at http://localhost:8000.

The Streamlit frontend should be accessible at http://localhost:8501.

When you enter a doctor-patient conversation in the Streamlit app and press the "Generate SOAP Note" button, it will send a request to the FastAPI server. The FastAPI server will generate the SOAP note based on the conversation and the trained model, and it will return the SOAP note as a response.

Troubleshooting
API Errors: If there are issues with the API, you might see error messages from the FastAPI server. Common issues include:

Invalid OpenAI API key.

Network connectivity issues with the datasets or OpenAI API.

Missing Dataset: If the dataset isn't available or loading properly, ensure that the datasets library is able to fetch adesouza1/soap_notes.

Library Versions: If there are compatibility issues, check the versions of libraries in requirements.txt and ensure that they match your environment.
