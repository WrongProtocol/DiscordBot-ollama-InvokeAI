import asyncio
from invoke import Invoke
from invoke.api import BaseModels, ModelType, QueueApi
import random
import requests
from io import BytesIO
from PIL import Image

QUEUE_NAME = "d-bot-queue"
BATCH_NAME = "d-bot-batch"

def generate_random_seed():
    return random.randint(1, 3406498352)



async def create_hq(prompt):
    prompt = "Super Realism. " + prompt # this is because of the super realism lora 
    invoke = Invoke()
    queue = invoke.queue
    images = invoke.images
    queue.queue_id = QUEUE_NAME

    payload = {
        "batch": {
            "batch_id": "d-bot-batch",
            "origin": "api",
            "destination": "gallery",
            "graph": {
                "id": "flux_txt2img",
                "nodes": {
                    "flux_model_loader": {
                        "id": "flux_model_loader",
                        "type": "flux_model_loader",
                        "model": {
                            "key": "d180f224-e290-473a-b866-d3e574ff02fa",
                            "hash": "blake3:8e532c2cb80971c1fc56074e63adcfcaba7b2e1c7c79afda98a459aafd4f4b87",
                            "name": "FLUX Dev (Quantized)",
                            "base": "flux",
                            "type": "main",
                            "submodel_type": None
                        },
                        "t5_encoder_model": {
                            "key": "45703b29-2462-42e9-8dbc-22923fb88bb0",
                            "hash": "blake3:12f3f5d4856e684c627c0b5c403ace83a8e8baaf0fa6518cd230b5ec1c519107",
                            "name": "t5_base_encoder",
                            "base": "any",
                            "type": "t5_encoder",
                            "submodel_type": None
                        },
                        "clip_embed_model": {
                            "key": "23ea03d0-5a3e-4b79-8595-30c27f9a3801",
                            "hash": "blake3:17c19f0ef941c3b7609a9c94a659ca5364de0be364a91d4179f0e39ba17c3b70",
                            "name": "clip-vit-large-patch14",
                            "base": "any",
                            "type": "clip_embed",
                            "submodel_type": None
                        },
                        "vae_model": {
                            "key": "e7c4356e-2d0c-4414-96f5-2446dbc0b764",
                            "hash": "blake3:ce21cb76364aa6e2421311cf4a4b5eb052a76c4f1cd207b50703d8978198a068",
                            "name": "FLUX.1-schnell_ae",
                            "base": "flux",
                            "type": "vae",
                            "submodel_type": None
                        }
                    },
                    "flux_text_encoder": {
                        "id": "flux_text_encoder",
                        "type": "flux_text_encoder",
                        "prompt": prompt
                    },
                    "pos_cond_collect": {
                        "id": "pos_cond_collect",
                        "type": "collect"
                    },
                    "flux_denoise": {
                        "id": "flux_denoise",
                        "type": "flux_denoise",
                        "width": 1024,
                        "height": 1024,
                        "num_steps": 30,
                        "guidance": 4,
                        "seed": generate_random_seed()
                    },
                    "lora_selector": {
                        "id": "lora_selector",
                        "type": "lora_selector",
                        "lora": {
                            "key": "236bda59-08b0-4c87-9f4b-e45fa9f84de4",
                            "hash": "blake3:5f41e5aa3fe383f0e8af78280991a74a5a7641f8581099874d3ecfb964383261",
                            "name": "super-realism",
                            "base": "flux",
                            "type": "lora",
                            "submodel_type": None
                        },
                        "weight": 0.75
                    },
                    "lora_collector": {
                        "id": "lora_collector",
                        "type": "collect"
                    },
                    "flux_lora_collection_loader": {
                        "id": "flux_lora_collection_loader",
                        "type": "flux_lora_collection_loader"
                    },
                    "core_metadata": {
                        "id": "core_metadata",
                        "type": "core_metadata",
                        "generation_mode": "flux_txt2img",
                        "positive_prompt": prompt,
                        "width": 1024,
                        "height": 1024,
                        "seed": generate_random_seed(),
                        "steps": 30,
                        "guidance": 4,
                        "model": {
                            "key": "d180f224-e290-473a-b866-d3e574ff02fa",
                            "hash": "blake3:8e532c2cb80971c1fc56074e63adcfcaba7b2e1c7c79afda98a459aafd4f4b87",
                            "name": "FLUX Dev (Quantized)",
                            "base": "flux",
                            "type": "main",
                            "submodel_type": None
                        },
                        "loras": [
                            {
                                "model": {
                                    "key": "236bda59-08b0-4c87-9f4b-e45fa9f84de4",
                                    "hash": "blake3:5f41e5aa3fe383f0e8af78280991a74a5a7641f8581099874d3ecfb964383261",
                                    "name": "super-realism",
                                    "base": "flux",
                                    "type": "lora",
                                    "submodel_type": None
                                },
                                "weight": 0.75
                            }
                        ],
                        "vae": {
                            "key": "e7c4356e-2d0c-4414-96f5-2446dbc0b764",
                            "hash": "blake3:ce21cb76364aa6e2421311cf4a4b5eb052a76c4f1cd207b50703d8978198a068",
                            "name": "FLUX.1-schnell_ae",
                            "base": "flux",
                            "type": "vae",
                            "submodel_type": None
                        },
                        "t5_encoder": {
                            "key": "45703b29-2462-42e9-8dbc-22923fb88bb0",
                            "hash": "blake3:12f3f5d4856e684c627c0b5c403ace83a8e8baaf0fa6518cd230b5ec1c519107",
                            "name": "t5_base_encoder",
                            "base": "any",
                            "type": "t5_encoder"
                        },
                        "clip_embed_model": {
                            "key": "23ea03d0-5a3e-4b79-8595-30c27f9a3801",
                            "hash": "blake3:17c19f0ef941c3b7609a9c94a659ca5364de0be364a91d4179f0e39ba17c3b70",
                            "name": "clip-vit-large-patch14",
                            "base": "any",
                            "type": "clip_embed"
                        }
                    },
                    "canvas_output": {
                        "id": "canvas_output",
                        "type": "flux_vae_decode"
                    }
                },
                "edges": [
                    {
                        "source": {"node_id": "flux_model_loader", "field": "vae"},
                        "destination": {"node_id": "flux_denoise", "field": "controlnet_vae"}
                    },
                    {
                        "source": {"node_id": "flux_model_loader", "field": "vae"},
                        "destination": {"node_id": "canvas_output", "field": "vae"}
                    },
                    {
                        "source": {"node_id": "flux_model_loader", "field": "t5_encoder"},
                        "destination": {"node_id": "flux_text_encoder", "field": "t5_encoder"}
                    },
                    {
                        "source": {"node_id": "flux_model_loader", "field": "max_seq_len"},
                        "destination": {"node_id": "flux_text_encoder", "field": "t5_max_seq_len"}
                    },
                    {
                        "source": {"node_id": "flux_text_encoder", "field": "conditioning"},
                        "destination": {"node_id": "pos_cond_collect", "field": "item"}
                    },
                    {
                        "source": {"node_id": "pos_cond_collect", "field": "collection"},
                        "destination": {"node_id": "flux_denoise", "field": "positive_text_conditioning"}
                    },
                    {
                        "source": {"node_id": "flux_denoise", "field": "latents"},
                        "destination": {"node_id": "canvas_output", "field": "latents"}
                    },
                    {
                        "source": {"node_id": "lora_collector", "field": "collection"},
                        "destination": {"node_id": "flux_lora_collection_loader", "field": "loras"}
                    },
                    {
                        "source": {"node_id": "flux_model_loader", "field": "transformer"},
                        "destination": {"node_id": "flux_lora_collection_loader", "field": "transformer"}
                    },
                    {
                        "source": {"node_id": "flux_model_loader", "field": "clip"},
                        "destination": {"node_id": "flux_lora_collection_loader", "field": "clip"}
                    },
                    {
                        "source": {"node_id": "flux_lora_collection_loader", "field": "transformer"},
                        "destination": {"node_id": "flux_denoise", "field": "transformer"}
                    },
                    {
                        "source": {"node_id": "flux_lora_collection_loader", "field": "clip"},
                        "destination": {"node_id": "flux_text_encoder", "field": "clip"}
                    },
                    {
                        "source": {"node_id": "lora_selector", "field": "lora"},
                        "destination": {"node_id": "lora_collector", "field": "item"}
                    },
                    {
                        "source": {"node_id": "core_metadata", "field": "metadata"},
                        "destination": {"node_id": "canvas_output", "field": "metadata"}
                    }
                ]
            },
            "runs": 1
        },
        "prepend": False
    }
    queue_batch = await queue.enqueue_batch(payload)
    #print(f"queue_batch: {queue_batch}\n\n")
    queue_status = await queue.get_queue_status()
    # print(f"queue_status: {queue_status}\n\n")
    current_item = await queue.get_current_item()
    print(f"current_item : { current_item }\n\n")
    itemId = current_item.item_id
    while True:
        status = await queue.get_queue_item(itemId)#.completed_at
        print("image status:", status)
        
        if status.get('completed_at') is not None:
            break

        await asyncio.sleep(2)  # Wait 2 seconds before checking again
   
    print("image done")
    lastImageCreatedHopefully = await images.list_image_dtos(offset=0, limit=1)
    print(f"lastImageCreatedHopefully = {lastImageCreatedHopefully} \n\n")
    imgItem = lastImageCreatedHopefully.items[0]
    theImg = imgItem.image_name
    print(f"theImg = {theImg} \n\n")
    imgUrl = imgItem.image_url
    #img = await images.get_full(theImg)
    response = requests.get("http://127.0.0.1:9090/" + imgUrl)

    img_data = BytesIO(response.content)
    #img = Image.open(img_data)
    #img.show()
    return img_data

async def main():
    invoke = Invoke()

    print("Waiting for invoke...")
    version = await invoke.wait_invoke()
    print(f"Version: {version}")

    # models = await invoke.models.list(base_models=[BaseModels.SDXL], model_type=[ModelType.Main])
    # print(models)

    await create_hq("A dog sitting on the grass at sunset.")
    

if __name__ == "__main__":
    asyncio.run(main())