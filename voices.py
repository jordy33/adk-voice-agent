import os
from google.cloud import texttospeech_v1beta1 as texttospeech

# Configura la autenticación (comenta la línea que no necesites)
# Para usar un archivo de clave de servicio:
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/ruta/a/tu/key.json"
# Para usar credenciales de gcloud snap:
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.expanduser("~/snap/google-cloud-cli/current/.config/gcloud/application_default_credentials.json")

def synthesize_text_to_mp3(text, voice_name, gender, output_filename):
    """Sintetiza texto en un archivo MP3 usando una voz específica."""
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="es-US",  # La API proporciona voces de 'es-US' para 'es-MX'
        name=voice_name,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    with open(output_filename, "wb") as out_file:
        out_file.write(response.audio_content)
        print(f'Contenido de audio escrito en "{output_filename}"')

# Define el texto a sintetizar
alerta_text = "Alerta: se ha activado el botón de pánico del dispositivo GPS. Atención inmediata requerida."

# Petición para obtener todas las voces disponibles en la región de México/Latinoamérica (es-US)
client = texttospeech.TextToSpeechClient()
response = client.list_voices(language_code="es-MX")

print("Generando archivos MP3 para voces disponibles (es-US)...")
for voice in response.voices:
    voice_name = voice.name
    voice_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender).name
    
    # Formato del nombre del archivo: voz_nombre-genero.mp3
    filename = f"voz_{voice_name.replace('-', '_')}_{voice_gender}.mp3"

    print(f"Sintetizando con la voz: {voice_name}...")
    synthesize_text_to_mp3(alerta_text, voice_name, voice_gender, filename)

print("\nProceso completado.")