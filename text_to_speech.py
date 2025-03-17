from gtts import gTTS
import os
import subprocess  # For opening audio file in Windows
from pydub import AudioSegment
from pydub.playback import play

def text_to_speech(text, filename="news_audio.mp3"):
    """
    Converts text into Hindi speech and saves it as an MP3 file.

    Args:
        text (str): The text to be converted into speech.
        filename (str): The name of the output MP3 file.

    Returns:
        str: The filename of the generated audio.
    """
    if not text.strip():
        print("Error: No text provided for speech conversion.")
        return None

    # Ensure the file is saved in the current directory
    output_path = os.path.join(os.getcwd(), filename)

    # Convert text to Hindi speech
    tts = gTTS(text, lang="hi")
    tts.save(output_path)

    print(f"✅ Hindi speech saved at: {output_path}")

    # Load and play the saved MP3 file
    try:
        audio = AudioSegment.from_file(output_path, format="mp3")
        play(audio)
    except Exception as e:
        print(f"⚠️ Error playing audio: {e}")
        print("📂 Opening file manually...")
        if os.name == "nt":  # Windows
            os.startfile(output_path)
        else:  # macOS/Linux
            subprocess.run(["open", output_path])

    return output_path

# Test the function
if __name__ == "__main__":
    sample_text = "टेस्ला कंपनी ने अपनी नई इलेक्ट्रिक कार जारी की है जो बहुत सफल हो रही है।"
    audio_file = text_to_speech(sample_text)

    if audio_file:
        print(f"🎵 Playing audio from: {audio_file}")
