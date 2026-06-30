# Filmy  

**Filmy** is a Django-based web application that helps users discover and explore Bollywood movies. It combines a searchable movie database with an AI-powered recommendation system using LLaMA 2 via Ollama.  


---

## Features
- **Browse and search** through a curated Bollywood movie database.
- View **detailed movie information** with posters and trailers.
- **AI Movie Recommender** powered by **LLaMA 2** – generates personalized Bollywood movie recommendations.
- Minimal, clean UI for a smooth experience.  

---

## Tech Stack
- **Backend:** Django (Python)  
- **Frontend:** HTML, TailwindCSS, Vanilla JS  
- **AI Integration:** LLaMA 2 via [Ollama](https://ollama.ai/)  
- **Database:** MySQL (with exportable **movie.json** for portabilityL)  

---

## Installation & Setup  
1. Clone the repo  
	```bash  
    git clone https://github.com/<your-username>/InvestMentor.git  
    cd InvestMentor

2. Setup virtual environment  
    ```bash
	python -m venv venv # On Windows  
	source venv/bin/activate # On Mac/Linux  

3. Install dependencies  
    ```bash
	pip install Django  
	pip install mysqlclient
    pip install requests
	
4. Database setup  
- This project uses MySQL as the default database.
- Apply migrations:
    ```bash
	python manage.py migrate  
- Load movie data from the provided movie.json:
    ```bash
    python manage.py loaddata movie.json

5. Start Django server 
    ```bash
	python manage.py runserver   
- Now visit http://127.0.0.1:8000/

## LLaMA 2 Integration (via Ollama)
The AI Roadmap Generator depends on Ollama to run LLaMA locally.

1. Install Ollama
- Download and install from Ollama.ai
- Verify installation:  
    ```bash
	ollama --version

2. Pull the LLaMA 2 model
    ```bash
	ollama pull llama2

3. Run Ollama server
- In a separate terminal (before using roadmap): 
    ```bash
	ollama run llama2
