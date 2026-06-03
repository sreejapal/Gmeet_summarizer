# Google Meet AI Summarizer

## Overview

Google Meet AI Summarizer is an AI-powered web application that helps users analyze meeting recordings and transcripts. The system automatically generates concise summaries, extracts action items, identifies key discussion points, detects decisions made during meetings, and suggests next steps.

## Features

* Upload meeting recordings (MP4, MP3, WAV)
* Upload meeting transcripts (TXT)
* Automatic speech-to-text transcription using Whisper
* AI-generated meeting summaries using Gemini
* Key discussion point extraction
* Action item extraction
* Decision detection
* Task assignment detection
* Download summary as JSON

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI Models

* OpenAI Whisper
* Google Gemini 2.5 Flash

### Libraries & Tools

* PyTorch
* FFmpeg
* Python Dotenv

---

## Installation

### Clone the Repository

```bash
git clone <repository-url>
cd Gmeet_summarizer
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install FFmpeg

Download FFmpeg and add the `bin` folder to your system PATH.

Verify installation:

```bash
ffmpeg -version
```

### Configure Environment Variables

Create a `.env` file in the project root directory:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Generate a Gemini API key from Google AI Studio.

---

## Running the Application

```bash
streamlit run app.py
```

The application will launch in your default web browser.

---

## Project Structure

```text
Gmeet_summarizer/
│
├── app.py
├── processor.py
├── summarizer.py
├── transcriber.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── transcripts/
├── summaries/
│
└── venv/
```

---

## Workflow

```text
Meeting Recording / Transcript
            ↓
       Transcription
        (Whisper)
            ↓
        Transcript
            ↓
      AI Analysis
       (Gemini)
            ↓
Structured Summary
            ↓
     Results Page
```

---

## Generated Output

The application returns structured meeting insights in JSON format:

```json
{
    "overview": "",
    "discussion_points": [],
    "action_items": [],
    "decisions": [],
    "task_assignments": [],
    "next_steps": []
}
```
