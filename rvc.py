# Carmine Silano
# 3/6/2025
# This hooks into RVC HF2 gradio server to generate audio

from gradio_client import Client, handle_file
import asyncio

SERVER="http://localhost:7866/"
async def rvc_tts(tts_text):
        
    client = Client(SERVER)
    result, result2 = client.predict(
            tts_voice="en-US-AvaNeural-Female",
            tts_text=tts_text,
            play_tts=False,
            api_name="/infer_tts_audio"
    )
    print(result[0])
    return result[0]

async def rvc_erika(audio_path, pitch_adjust):

    client = Client(SERVER)
    result = client.predict(
            audio_files=[handle_file(audio_path)],
            file_m=handle_file(r"models\Erika300\Erika.pth"),
            pitch_alg="rmvpe+",
            pitch_lvl=8 + pitch_adjust,
            file_index=handle_file(r"models\Erika300\Erika.index"),
            index_inf=0.75, #index influence 0-1
            r_m_f=3, # respiration median filtering 1-5
            e_r=0.25, # envelope ratio 0-1
            c_b_p=0.5, # consonant breath protection 0-1
            active_noise_reduce=False,
            audio_effects=False,
            api_name="/run"
    )
    print(result)
    return result

async def rvc_cyrone(audio_path, pitch_adjust):

    client = Client(SERVER)
    result = client.predict(
            audio_files=[handle_file(audio_path)],
            file_m=handle_file(r"models\Tyrone500\tyrone500.pth"),
            pitch_alg="rmvpe+",
            pitch_lvl=-4 + pitch_adjust,
            file_index=handle_file(r"models\Tyrone500\tyrone500.index"),
            index_inf=0.75, #index influence 0-1
            r_m_f=3, # respiration median filtering 1-5
            e_r=0.25, # envelope ratio 0-1
            c_b_p=0.5, # consonant breath protection 0-1
            active_noise_reduce=False,
            audio_effects=False,
            api_name="/run"
    )
    print(result)
    return result
#just for testing
if __name__ == "__main__":
    asyncio.run(rvc_tts("this is a test"))