# MeetGenie

An AI-powered meeting summarization system that processes Google Meet recordings or transcripts, generates structured meeting summaries, extracts action items and decisions, stores meeting archives, provides search functionality, and sends summaries via email.

## Features

### Meeting Processing

* Upload meeting recordings (`.mp4`, `.mp3`, `.wav`)
* Upload meeting transcripts (`.txt`)
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
* View meeting history
* Search previously saved meetings
* Download summaries as JSON

### Email Integration

* Send generated summaries via email
* Gmail App Password authentication
* One-click email delivery

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

* Gmail SMTP using Yagmail

---

## Project Structure

```text
gmeet-ai-summarizer/
│
├── app.py
├── processor.py
├── transcriber.py
├── summarizer.py
├── database.py
├── email_sender.py
│
├── uploads/
├── transcripts/
├── summaries/
│
├── meetings.db
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd gmeet-ai-summarizer
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## FFmpeg Installation

Whisper requires FFmpeg.

### Windows

Download FFmpeg and add the `bin` folder to your system PATH.

Verify installation:

```bash
ffmpeg -version
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_gemini_api_key
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

### Gemini API Key

Create an API key from:

https://aistudio.google.com

### Gmail App Password

1. Enable 2-Step Verification
2. Open Google App Passwords
3. Generate a Mail App Password
4. Use the generated password in `.env`

---

## Running the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## Usage

### Upload Meeting Recording

Supported formats:

* MP4
* MP3
* WAV

### Upload Transcript

Supported formats:

* TXT

### Generate Summary

The system will:

1. Transcribe audio/video (if required)
2. Generate AI summary
3. Extract action items
4. Extract decisions
5. Extract task assignments

### Save Meeting

Click **Save Meeting** to store the summary in SQLite.

### Search Meetings

Use the search feature to locate previous meeting summaries.

### Send Email

1. Enter recipient email
2. Click **Send Summary Email**
3. Summary will be delivered automatically

---

## Database

Meeting summaries are stored in:

```text
meetings.db
```

Stored information:

* Filename
* Timestamp
* Overview
* Full Summary JSON

---

## Example Workflow

```text
Upload File
      ↓
Transcription
      ↓
AI Summary Generation
      ↓
Review Summary
      ↓
Save Meeting
      ↓
Search Archive
      ↓
Email Summary
```
