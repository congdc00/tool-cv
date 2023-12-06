import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
from loguru import logger

class S2T_Model():
    
    model = None

    def init_model():
        logger.info("Init model Whisper V2")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        model_id = "openai/whisper-large-v2"
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        model.to(device)
        processor = AutoProcessor.from_pretrained(model_id)

        S2T_Model.model = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            max_new_tokens=128,
            chunk_length_s=30,
            batch_size=16,
            return_timestamps=True,
            torch_dtype=torch_dtype,
            device=device,
        )

    @staticmethod
    def convert(audio):
        if S2T_Model.model ==None:
            S2T_Model.init_model()
        
        result = S2T_Model.model(audio, generate_kwargs={"language": "vietnamese"})
        return result["text"]

if __name__ == "__main__":
    
    dataset = "./data/audio.wav"
    result = S2T_Model.convert(dataset)
    print(result)
