# 🎨 ComicCraft-AI

An AI comic story creator built with **Google Gemini models** and **Streamlit**.
Enter a story idea, pick a genre and art style, and get a multi-panel comic with captions and dialogue.

*Project submitted under Vetri Thiran Payirchi Thittam.*

## Features
- Story script generation (title, characters, panel scenes, captions, dialogue) using `gemini-2.5-flash`
- Panel image generation using `gemini-2.5-flash-image`
- Genre, art style, panel count and dialogue language (English / Tamil / Hindi) options
- Consistent characters via a shared character sheet across panels
- Download the script as JSON

## Tech Stack
Python, Streamlit, Google GenAI SDK, Pillow

## Setup
1. Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set the key (or paste it in the app sidebar):
   ```bash
   export GEMINI_API_KEY="your_key_here"      # Windows: set GEMINI_API_KEY=your_key_here
   ```
4. Run:
   ```bash
   streamlit run app.py
   ```

## How it works
1. **Script step**: Gemini text model returns a JSON script for the requested number of panels.
2. **Art step**: For each panel, Gemini image model draws the scene using the character sheet and chosen style.
3. **Display**: Streamlit shows the panels in a grid with captions and dialogue.

## Project Structure
```
app.py            # Streamlit app + Gemini calls
requirements.txt  # Dependencies
README.md         # Documentation
```

## Future Improvements
- Speech bubbles drawn onto images
- Export the comic as PDF
- Multiple characters with reference images
