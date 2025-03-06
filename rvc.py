# Carmine Silano
# 3/6/2025
# This hooks into RVC HF2 gradio server to generate audio

from gradio_client import Client
import asyncio

async def rvc_tts(tts_text):
        
    client = Client("http://localhost:7866/")
    result, result2 = client.predict(
            tts_voice="en-US-AvaNeural-Female",
            tts_text=tts_text,
            play_tts=False,
            api_name="/infer_tts_audio"
    )
    print(result[0])
    return result[0]


#just for testing
if __name__ == "__main__":
    asyncio.run(rvc_tts("this is a test"))