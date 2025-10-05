import streamlit as st
import streamlit.components.v1 as components
from gtts import gTTS
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
import tempfile
import os
from PIL import Image, ImageDraw, ImageFont

import cv2

st.title("🧠 Describe Paper")

st.subheader("Auto-Generated Summary")
st.text_area("Summary", "This will contain the NLP-generated summary...", height=200)

st.subheader("Key Terms / Concepts")
st.text_area("Key Terms", "Add extracted keywords here...")

st.subheader("Findings")
st.text_area("Findings", "Key discoveries or insights...")

st.subheader("Flowchart")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Flowchart_example.svg/1200px-Flowchart_example.svg.png", caption="Auto-generated structure", width=500)

st.subheader("Gallery")
components.html(
    """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {box-sizing: border-box;}
body {font-family: Verdana, sans-serif;}
.mySlides {display: none;}
img {vertical-align: middle;}

/* Slideshow container */
.slideshow-container {
  max-width: 1000px;
  position: relative;
  margin: auto;
}

/* Caption text */
.text {
  color: #f2f2f2;
  font-size: 15px;
  padding: 8px 12px;
  position: absolute;
  bottom: 8px;
  width: 100%;
  text-align: center;
}

/* Number text (1/3 etc) */
.numbertext {
  color: #f2f2f2;
  font-size: 12px;
  padding: 8px 12px;
  position: absolute;
  top: 0;
}

/* The dots/bullets/indicators */
.dot {
  height: 15px;
  width: 15px;
  margin: 0 2px;
  background-color: #bbb;
  border-radius: 50%;
  display: inline-block;
  transition: background-color 0.6s ease;
}

.active {
  background-color: #717171;
}

/* Fading animation */
.fade {
  animation-name: fade;
  animation-duration: 1.5s;
}

@keyframes fade {
  from {opacity: .4} 
  to {opacity: 1}
}

/* On smaller screens, decrease text size */
@media only screen and (max-width: 300px) {
  .text {font-size: 11px}
}
</style>
</head>
<body>

<div class="slideshow-container">

<div class="mySlides fade">
  <div class="numbertext">1 / 3</div>
  <img src="https://unsplash.com/photos/GJ8ZQV7eGmU/download?force=true&w=1920" style="width:100%">
  <div class="text">Caption Text</div>
</div>

<div class="mySlides fade">
  <div class="numbertext">2 / 3</div>
  <img src="https://unsplash.com/photos/eHlVZcSrjfg/download?force=true&w=1920" style="width:100%">
  <div class="text">Caption Two</div>
</div>

<div class="mySlides fade">
  <div class="numbertext">3 / 3</div>
  <img src="https://unsplash.com/photos/zVhYcSjd7-Q/download?force=true&w=1920" style="width:100%">
  <div class="text">Caption Three</div>
</div>

</div>
<br>

<div style="text-align:center">
  <span class="dot"></span> 
  <span class="dot"></span> 
  <span class="dot"></span> 
</div>

<script>
let slideIndex = 0;
showSlides();

function showSlides() {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
  }
  slideIndex++;
  if (slideIndex > slides.length) {slideIndex = 1}    
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " active";
  setTimeout(showSlides, 2000); // Change image every 2 seconds
}
</script>

</body>
</html> 

    """,
    height=600,
)


summary_text = st.text_area("Text Summary for Narration", value="")
# with open("data/videos/subway_surfers.mp4") as file:
#     background_video = file

background_video = "data/videos/subway_surfers.mp4"
# background_video = cv2.VideoCapture('../../data/videos/subway_surfers.mp4')  # Provide your local or downloaded video path


if st.button("🎬 Generate Video"):
    with st.spinner("Generating narration and video..."):

        # Step 1: Convert text to speech
        tts = gTTS(summary_text)
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_audio.name)

        # Step 2: Load base video
        video = VideoFileClip(background_video).subclip(0, 15).without_audio()

        # Step 3: Load generated speech and fit video length
        audio = AudioFileClip(temp_audio.name)
        video = video.set_audio(audio).fx(lambda clip: clip.loop(duration=audio.duration))

        # Step 4: Add subtitles (simple line wrapping)
        caption_clip = TextClip(
            summary_text,
            fontsize=40,
            color="white",
            bg_color="rgba(0,0,0,0.5)",
            size=(video.w - 100, None),
            method="caption",
            align="center"
        ).set_position(("center", video.h - 150)).set_duration(audio.duration)

        final_video = CompositeVideoClip([video, caption_clip])

        # Step 5: Write output
        output_path = os.path.join(tempfile.gettempdir(), "narrated_subway.mp4")
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

        st.success("✅ Video generated successfully!")
        st.video(output_path)


if st.button("Next → Connect NASA Resources"):
    st.switch_page("pages/3_Connect_Paper.py")
