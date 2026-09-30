import io
import json
import os

import streamlit as st
from google import genai
from google.genai import types
from PIL import Image

TEXT_MODEL = "gemini-2.5-flash"
IMAGE_MODEL = "gemini-2.5-flash-image"

st.set_page_config(page_title="ComicCraft-AI", page_icon="🎨", layout="wide")
st.title("🎨 ComicCraft-AI")
st.caption("AI comic story creator powered by Gemini models")

# ---------- Sidebar ----------
api_key = st.sidebar.text_input(
    "Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", "")
)
genre = st.sidebar.selectbox(
    "Genre", ["Adventure", "Sci-Fi", "Comedy", "Fantasy", "Mystery", "Moral story"]
)
style = st.sidebar.selectbox(
    "Art style", ["Colorful cartoon", "Manga", "Retro pop-art", "Watercolor", "Superhero comic"]
)
language = st.sidebar.selectbox("Dialogue language", ["English", "Tamil", "Hindi"])
panels = st.sidebar.slider("Number of panels", 3, 8, 4)

idea = st.text_area(
    "Your story idea",
    placeholder="A little robot in Chennai learns to make filter coffee...",
    height=100,
)


def get_client():
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
        st.stop()
    return genai.Client(api_key=api_key)


def generate_script(client):
    prompt = f"""
You are a comic writer. Create a {panels}-panel {genre} comic based on this idea:
"{idea}"

Return ONLY JSON in this format:
{{
  "title": "comic title",
  "character_sheet": "consistent visual description of main characters",
  "panels": [
    {{"scene": "visual description of the panel",
      "caption": "short narration",
      "dialogue": "character line in {language}"}}
  ]
}}
"""
    resp = client.models.generate_content(
        model=TEXT_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    return json.loads(resp.text)


def generate_panel_image(client, character_sheet, panel):
    prompt = (
        f"Comic panel, {style} style. Characters: {character_sheet}. "
        f"Scene: {panel['scene']}. No text or speech bubbles in the image."
    )
    resp = client.models.generate_content(model=IMAGE_MODEL, contents=prompt)
    for part in resp.candidates[0].content.parts:
        if part.inline_data:
            return Image.open(io.BytesIO(part.inline_data.data))
    return None


if st.button("✨ Create Comic", type="primary", disabled=not idea.strip()):
    client = get_client()
    with st.spinner("Writing the script..."):
        story = generate_script(client)

    st.header(story["title"])
    cols = st.columns(2)
    for i, panel in enumerate(story["panels"]):
        with cols[i % 2]:
            with st.spinner(f"Drawing panel {i + 1}..."):
                img = generate_panel_image(client, story["character_sheet"], panel)
            if img:
                st.image(img, use_container_width=True)
            else:
                st.warning("Image could not be generated for this panel.")
            st.markdown(f"*{panel['caption']}*")
            st.markdown(f"💬 **{panel['dialogue']}**")
            st.divider()

    st.download_button(
        "⬇️ Download script (JSON)",
        json.dumps(story, ensure_ascii=False, indent=2),
        file_name="comic_script.json",
    )
