# MeetGenie - AI Meeting Intelligence Platform

🚀 **Live Demo:** https://meetgenie.streamlit.app

MeetGenie is an AI-powered meeting intelligence platform that transforms meeting recordings and transcripts into structured, actionable insights. It automatically generates summaries, extracts key discussion points, identifies action items and decisions, assigns tasks, stores meeting archives, and enables email sharing of reports.

---

## Overview

MeetGenie helps teams save time by eliminating manual note-taking and meeting documentation. Simply upload a meeting recording or transcript, and the platform will generate a comprehensive meeting report within seconds.

### Key Benefits

* Automatic meeting transcription
* AI-generated summaries
* Action item extraction
* Decision tracking
* Task assignment detection
* Meeting history and search
* Email report sharing
* Cloud-based accessibility

---

## Live Deployment

The application is deployed and accessible online via Streamlit Cloud.

**Live Application:**
https://meetgenie.streamlit.app

No local installation is required for end users.

---

## Features

### Meeting Processing

* Upload meeting recordings/transcripts (`.mp4`, `.mp3`, `.wav`, `.txt`)
* Automatic speech-to-text transcription using Whisper
* AI-powered meeting summarization using Gemini

### Summary Generation

* Meeting Overview
* Key Discussion Points
* Action Items
* Decisions Made
* Task Assignments
* Next Steps

### Meeting Archive

* Save meeting summaries to SQLite database
* Maintain meeting history
* Search previously saved meetings
* Download summaries as PDF

### Email Integration

* Send meeting summaries directly via email
* Share reports with stakeholders
* Gmail SMTP integration

### Cloud Access

* Accessible from any browser
* Deployed on Streamlit Cloud
* Continuous deployment through GitHub

---

## Supported Input Formats

### Audio / Video

* MP4
* MP3
* WAV

### Text

* TXT

---

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI Models

* OpenAI Whisper (Speech-to-Text)
* Google Gemini API (Summarization)

### Database

* SQLite

### Email Service

* Gmail SMTP
* Yagmail

---

## System Architecture

```text
User Upload
      │
      ▼
Whisper Transcription
      │
      ▼
Gemini Analysis
      │
      ▼
Structured Summary Generation
      │
      ▼
SQLite Storage
      │
      ├── Meeting History
      ├── Search
      ├── Email Reports
      └── PDF Download
```

---

## Project Structure

```text
MeetGenie/
│
├── app.py
├── processor.py
├── transcriber.py
├── summarizer.py
├── database.py
├── email_sender.py
│
├── requirements.txt
├── packages.txt
├── .gitignore
├── README.md
│
└── meetings.db
```

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/sreejapal/Gmeet_summarizer.git
cd Gmeet_summarizer
```

### 2. Create Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## FFmpeg Setup

Whisper requires FFmpeg for audio processing.

### Windows

Download FFmpeg:

https://ffmpeg.org/download.html

Verify installation:

```bash
ffmpeg -version
```

---

## Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

### Gemini API Key

Generate an API key from:

https://aistudio.google.com/

### Gmail App Password

1. Enable Two-Step Verification
2. Open Google Account → Security
3. Create an App Password
4. Add it to the `.env` file

---

## Running Locally

```bash
streamlit run app.py
```

Application will start at:

```text
http://localhost:8501
```

---

## Usage

### Upload Recording

Supported:

* MP4
* MP3
* WAV

### Upload Transcript

Supported:

* TXT

### Generate Summary

The platform automatically:

1. Transcribes audio/video
2. Analyzes content using Gemini
3. Generates structured meeting insights

### Save Meeting

Click:

```text
Save Meeting
```

to store the summary in the database.

### Search Meetings

Use the Search feature to retrieve previous meeting reports.

### Send Email

1. Enter recipient email
2. Click Send Summary Email
3. Report is delivered instantly

---

## Example Workflow

```text
Upload Meeting Recording
          │
          ▼
Audio Transcription
          │
          ▼
AI Analysis
          │
          ▼
Meeting Summary
          │
          ▼
Save Report
          │
          ├── Search
          ├── History
          ├── Download
          └── Email
```

---

## Database Schema

Meetings are stored in SQLite.

Stored Data:

* Meeting ID
* Filename
* Timestamp
* Meeting Overview
* Full Summary JSON

Database File:

```text
meetings.db
```

---

## Deployment

### Platform

Streamlit Cloud

### Deployment Process

```text
GitHub Push
      │
      ▼
Streamlit Cloud
      │
      ▼
Automatic Build
      │
      ▼
Live Application Update
```