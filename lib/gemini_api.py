import google.generativeai as genai
from google import genai as genai_image
from google.genai import types
from PIL import Image
from io import BytesIO

def call_gemini(prompt_text, model_name):
    """
    Memanggil Gemini API dengan prompt dan model tertentu.

    Args:
        prompt_text (str): Prompt lengkap untuk dikirim ke model.
        model_name (str): Nama model yang akan digunakan.

    Returns:
        tuple: (Respon teks dari model, jumlah karakter input, jumlah karakter output)
               atau (None, 0, 0) jika terjadi error.
    """
    try:
        print(f"\n🤖 Menghubungi Gemini dengan model '{model_name}'... (ini mungkin butuh beberapa saat)")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt_text)
        
        input_chars = len(prompt_text)
        output_chars = len(response.text)

        return response.text, input_chars, output_chars
    except Exception as e:
        print(f"❌ Terjadi kesalahan saat menghubungi Gemini API: {e}")
        return None, 0, 0

def generate_image(prompt_text, model_name, api_key):
    """
    Memanggil Gemini API untuk membuat gambar.

    Args:
        prompt_text (str): Prompt teks yang mendeskripsikan gambar.
        model_name (str): Nama model yang akan digunakan (harus mampu membuat gambar).
        api_key (str): API key untuk otentikasi.

    Returns:
        PIL.Image.Image: Objek gambar, atau None jika terjadi error.
    """
    try:
        print(f"\n🎨 Menghubungi Gemini dengan model '{model_name}' untuk membuat gambar...")
        client = genai_image.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model_name,
            contents=prompt_text,
            config=types.GenerateContentConfig(
                 response_modalities=['TEXT', 'IMAGE']
            )
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                return Image.open(BytesIO(part.inline_data.data))
    except Exception as e:
        print(f"❌ Terjadi kesalahan saat membuat gambar: {e}")
    return None
