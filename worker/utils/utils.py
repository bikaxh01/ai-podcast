# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import mimetypes
import os
import re
import struct
from dotenv import load_dotenv
from google import genai
from google.genai import types
import asyncio
load_dotenv()


def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    sample_rate = parameters["rate"]
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",  # ChunkID
        chunk_size,  # ChunkSize (total file size - 8 bytes)
        b"WAVE",  # Format
        b"fmt ",  # Subchunk1ID
        16,  # Subchunk1Size (16 for PCM)
        1,  # AudioFormat (1 for PCM)
        num_channels,  # NumChannels
        sample_rate,  # SampleRate
        byte_rate,  # ByteRate
        block_align,  # BlockAlign
        bits_per_sample,  # BitsPerSample
        b"data",  # Subchunk2ID
        data_size,  # Subchunk2Size (size of audio data)
    )
    return header + audio_data


def parse_audio_mime_type(mime_type: str) -> dict[str, int | None]:
    bits_per_sample = 16
    rate = 24000

    # Extract rate from parameters
    parts = mime_type.split(";")
    for param in parts:  # Skip the main type part
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate_str = param.split("=", 1)[1]
                rate = int(rate_str)
            except (ValueError, IndexError):
                # Handle cases like "rate=" with no value or non-integer value
                pass  # Keep rate as default
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except (ValueError, IndexError):
                pass  # Keep bits_per_sample as default if conversion fails

    return {"bits_per_sample": bits_per_sample, "rate": rate}


def save_binary_file(file_name, data):
    media_dir = "./media"
    os.makedirs(media_dir,exist_ok=True)
    file_path = os.path.join(media_dir,file_name)
    f = open(file_path, "wb")
    f.write(data)
    f.close()
    print(f"File saved to to: {file_name}")


async def generate(scene_script,script_sequence):
    print(f"""Generating audio for {script_sequence}🟢 \n""")
    
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API"),
    )

    model = "gemini-2.5-pro-preview-tts"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=f"""Generate a podcast-style narration using the following text. The voice should reflect a calm, composed, and reassuring presence, projecting quiet authority and confidence. Use a sincere, empathetic tone with gentle authority—especially when delivering apologies or addressing sensitive topics. Maintain steady, moderate pacing: unhurried to convey care, yet efficient to reflect professionalism.

Speak with genuine empathy and warmth—particularly during lines such as “I’m very sorry for any disruption…” Use clear, precise pronunciation throughout, and give extra emphasis to key reassuring words like “smoothly,” “quickly,” and “promptly.”

Include brief, natural pauses after key phrases—especially after offering help or requesting information—to express attentiveness and invite listener engagement.

Format the output as natural, high-quality spoken audio suitable for a professional podcast episode. Ensure the delivery is engaging, trustworthy, and listener-friendly.

 \n{scene_script}"""
                ),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        response_modalities=[
            "audio",
        ],
        speech_config=types.SpeechConfig(
            multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                speaker_voice_configs=[
                    types.SpeakerVoiceConfig(
                        speaker="Host",
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name="Charon"
                            )
                        ),
                    ),
                    types.SpeakerVoiceConfig(
                        speaker="Guest",
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name="Iapetus"
                            )
                        ),
                    ),
                ]
            ),
        ),
    )

    response = await asyncio.to_thread(
        client.models.generate_content,
        model=model,
        contents=contents,
        config=generate_content_config,
    )

    inline_data = response.candidates[0].content.parts[0].inline_data
    data_buffer = inline_data.data
    file_extension = mimetypes.guess_extension(inline_data.mime_type)
    file_name = f"script_{script_sequence}"
    file_extension = ".wav"
    data_buffer = convert_to_wav(inline_data.data, inline_data.mime_type)
    save_binary_file(f"{file_name}{file_extension}", data_buffer)
    
    
    return f"{file_name}.wav"



