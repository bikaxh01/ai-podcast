import mimetypes
import os
import struct
from dotenv import load_dotenv
from google import genai
from google.genai import types
import asyncio
import cloudinary.uploader
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from typing import List, Any
from pydub import AudioSegment
from pydantic import BaseModel, Field
import requests

load_dotenv()

API_KEY = os.getenv("GEMINI_API")
CLOUD_NAME = os.getenv("CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")


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
    os.makedirs(media_dir, exist_ok=True)
    file_path = os.path.join(media_dir, file_name)
    f = open(file_path, "wb")
    f.write(data)
    f.close()
    print(f"File saved to to: {file_name}")


def parse_doc(doc_path: str):
    loader = PyPDFLoader(doc_path)
    doc_chunks = loader.load()
    doc_string = " ".join(doc.page_content for doc in doc_chunks)

    return doc_string


def document_filter(doc_content: str, user_prompt: str):
    prompt = PromptTemplate(
        template="""

You are a highly experienced content writer and text-cleaning specialist, skilled in refining raw document data for voice-based educational podcasts.

You will receive:
- A User Prompt indicating how the content should be used (e.g., podcast tone, format, focus or any topic use want's to add).
- Raw Content, which has been extracted from a parsed PDF and may include formatting artifacts, noise, and broken structures.

 Your Task:

Analyze the User Prompt and design your cleanup approach accordingly. Then clean the Raw Content while strictly and add any content if user want's following the below rules:

 CLEANING RULES:

 Clean and filter the raw content by removing:
- Unnecessary symbols or characters (e.g., ■, ###, ...)
- Garbled or incomplete lines
- Repeated metadata (e.g., "Page 1", "Scanned by...", "Confidential", etc.)
- Accidental line breaks and visual formatting glitches

 Preserve the content exactly:
- Do NOT paraphrase, summarize, or alter the original message
- Do NOT skip meaningful content
- Only fix sentence flow or formatting when absolutely necessary for readability

 Reconstruct layout and tone with care:
- Maintain structure (headings, lists, sections)
- Clarify only where needed, without reinterpreting the content
- The cleaned content should read as clear, continuous prose, as if originally typed
Important Notes:
- Your role is clean-up only, not rewriting or optimizing for tone unless stated in the User Prompt
- Do not infer or inject meaning
 Input Format:
User Prompt:
    {user_prompt}
Raw Content:
     {raw_content}   
 Output Format:
[Return the cleaned and well-structured version of the raw content,
formatted clearly, preserving all meaning, and ready for use in a podcast or other media as guided by the User Prompt.]

        
        """,
        input_variables=["raw_content,user_prompt"],
    )

    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=API_KEY,
        thinking_budget=0,
        max_output_tokens=10000,
    )
    chain = prompt | model
    final_content = chain.invoke(
        {"raw_content": doc_content, "user_prompt": user_prompt}
    )

    return final_content.content


def generate_content(user_prompt: str):
    prompt = PromptTemplate(
        template="""
  You are an expert content writer. Your task is to generate detailed, high-quality content based on the user prompt.

If the user has not specified the target audience, default to beginner-friendly content. Ensure the explanation is clear, thorough, and easy to understand.

Important:
- Only focus on the topic provided by the user.
- Do NOT generate podcast scripts, dialogues, or audiobook-style content.
- Your output should be detailed, well-organized explanatory content.
- This content will be used in a later phase to generate a podcast script, so focus solely on delivering informative written material.

Include:
- A clear explanation of the main topic
- All relevant subtopics, covered in depth
- Real-world examples wherever appropriate to aid understanding


        User prompt:
        {user_prompt}
        """,
        input_variables=["user_prompt", user_prompt],
    )
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=API_KEY,
        thinking_budget=0,
        max_output_tokens=10000,
    )
    chain = prompt | model
    final_content = chain.invoke({"user_prompt": user_prompt}).content

    return final_content


async def generate(scene_script, script_sequence):
    print(f"""Generating audio for {script_sequence}🟢 \n""")

    client = genai.Client(
        api_key=os.environ.get("GEMINI_API"),
    )

    model = "gemini-2.5-flash-preview-tts"
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


class ProjectData(BaseModel):
    id: str
    file_url: str | None
    prompt: str


def get_final_content(project_data: ProjectData):

    if project_data["file_url"]:
        print("Parsing the doc")
        raw_data = parse_doc(project_data["file_url"])
        filtered_content = document_filter(raw_data, project_data["prompt"])
        return filtered_content
    else:
        print("User doc not found generating on prompt...")
        content = generate_content(project_data["prompt"])
    return content


class PodcastResponseFormat(BaseModel):
    """
    Use this output format
    Host: [Beginner-friendly question or comment] Or
    Guest: [Clear, detailed explanation with examples]
    """

    title: str = Field(description="short title for the podcast")
    description: str = Field(description="short description of podcast")
    response: List[str] = Field(
        description="This response list should contain the content eg: Host: [Beginner-friendly question or comment] or  Guest: [Clear, detailed explanation with examples] "
    )


def generate_podcast_script(content: str):
    prompt = PromptTemplate(
        template="""
        You are an expert content writer working for a podcast production company that produces high-quality, audio-based educational content.

Your task is to convert the provided content into a natural, engaging podcast-style script featuring two speakers:

Host:
- Curious, friendly, and relatable
- Asks beginner-friendly questions
- Guides the conversation and ensures clarity for the audience

Guest:
- Knowledgeable, warm, and articulate
- Breaks down concepts in simple language
- Explains complex terms with clear, relatable examples

Your Responsibilities:
- Convert the provided content into a detailed, expressive podcast conversation between the Host and Guest.
- Use a conversational and friendly tone throughout.
- Add natural expressions such as:
  “Ohh, I see.”, “Hmm, interesting.”, “That’s a good point.”, “Got it.” to keep the flow immersive and engaging.
- Ensure the conversation flows smoothly, gradually introducing and explaining each concept in an accessible way.
- For any technical or complex terms, ensure the Guest provides beginner-friendly examples.
- Cover the entire source content thoroughly and accurately—do not skip key points.
- Make sure the final script is long enough to support a 8–10 minute voiceover when read aloud.
- Avoid emojis and non-verbal sound effects unless necessary for comprehension.

Output format:
Host: [Beginner-friendly question or comment]   Or
Guest: [Clear, detailed explanation with examples]

Note: The podcast script should be engaging, informative, and easy to understand for a beginner audience, with clear expressions and explanations.

Content:
{content}
        """,
        input_variables=["content"],
    )

    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=API_KEY,
        thinking_budget=0,
        max_output_tokens=10000,
    )

    model_with_structure = model.with_structured_output(PodcastResponseFormat)
    chain = prompt | model_with_structure
    parser = PydanticOutputParser(pydantic_object=PodcastResponseFormat)
    final_content = chain.invoke({"content": content})
    return final_content


async def generate_podcast(script: List[str]):
    finalScript = [" ".join(script[i : i + 20]) for i in range(0, len(script), 20)]

    tasks = [generate(sc, i) for i, sc in enumerate(finalScript)]
    results = await asyncio.gather(*tasks)
    file_names = list(results)
    return file_names


def merge_media_files(files: list[str], project_id: str):

    merged_audio = AudioSegment.from_file(f"./media/{files[0]}", format="wav")
    for file in files[1:]:
        audio_data = AudioSegment.from_file(f"./media/{file}", format="wav")
        merged_audio += audio_data
    merged_audio.export(f"./media/{project_id}_final.wav", format="wav")
    print("Audio files merged successfully!")
    return f"{project_id}_final"


def upload_media(file_name: str, project_id: str):

    cloudinary.config(
        secure_url=True,
        cloud_name=CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET,
    )
    res = cloudinary.uploader.upload_large(
        f"./media/{file_name}.wav",
        resource_type="video",
        public_id=file_name,
        folder=f"EchoMind/{project_id}",
    )

    return res["secure_url"]


def update_project(project_id: str, data: Any):
    server_url = os.getenv("SERVER_URL")
    headers = {"Content-Type": "application/json"}
    response = requests.put(
        f"{server_url}/internal/update-podcast/{project_id}", json=data, headers=headers
    )

    if response.status_code == 200:
        data = response.json()

        return data["data"]
    else:
        print(f"Request failed with status code: {response.status_code}")
