import os
import json
import re
import base64
import argparse
import time
from datetime import timedelta
from tqdm import tqdm
from openai import OpenAI
import cv2
import requests

class GPT4Analyzer:
    def __init__(self, video_dir):

        self.video_dir = video_dir
 
        
    def extract_key_frames(self, video_path, interval=1):
  
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * interval)
        
        frames = []
        count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            if count % frame_interval == 0:
                _, buffer = cv2.imencode('.jpg', frame)
                frames.append(base64.b64encode(buffer).decode('utf-8'))
                
            count += 1
        
        cap.release()
        return frames[:10]  

    def analyze_video(self, entry):
        """Analyze a single video with full tracking"""
        start_time = time.perf_counter()
        video_id = entry["video_id"]
        video_path = os.path.join(self.video_dir, f"{video_id}.mp4")
        input_tokens = 0
        output_tokens = 0
        max_retries = 20
        retry_delay = 3
        error_log = []

        try:
            if not os.path.exists(video_path):
                return None, "Video file missing", 0.0, 0, 0

            # Extract key frames
            frame_base64 = self.extract_key_frames(video_path)
            if not frame_base64:
                return None, "No valid frames extracted", 0.0, 0, 0

            # Build messages
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert in affective computing and very good at handling tasks related to emotion recognition."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"""\
                        I will first give you some ground truth information about the emotion in a video: \
                        visual clue, audio clue, and emotion label. I will also give you a model prediction. \
                        Please help me rate the performance of the prediction. 

                        Rating Requirements:
                        1. Rate each step using 0 or 1 (0=wrong, 1=correct)
                        2. For the last step, your rating should be 1 if the predicted emotion matches the ground truth emotion label, otherwise 0. Don't consider visual/audio cues at this step
                        3. For each other step, only consider predictions clearly contradicting visual/audio cues as incorrect
                        4. Ensure the number of steps in your rating is equal to that in the model prediction
                        5. Output format: <score>Step 1: 0/1, Step 2: 1/1,...</score>

                        Input Data:
                        - Visual clue: The video frames (images)
                        - Audio clue: '{entry['audio_clue']}'
                        - Emotion label: '{entry['ground_truth']}'
                        - Model prediction: '{entry['step']}'

                        Example Output: 
                        <score>Step 1: 1/1, Step 2: 0/1, Step 3: 0/1</score>"""
                    },
                        *[{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}} 
                        for b64 in frame_base64]
                    ]
                }
            ]

            url = ""
            GPT_AUTHORIZATION = ""
            headers = {
                "content-type": "application/json",
                "Authorization": f"{GPT_AUTHORIZATION}"
            }
            payload = {
                "model": "gpt-4o-2024-11-20",
                "messages": messages,
                "n": 1,
                "temperature": 0.0,
            }
            # Retry loop
            for attempt in range(max_retries):
                try:
                    response = requests.post(
                        url,
                        json=payload,
                        headers=headers
                    )
                    response.raise_for_status()
                    
                    resp_data = json.loads(response.text)
                    if "error" in resp_data:
                        raise Exception(f"API error: {resp_data['error']['message']}")
                    
                    input_tokens = resp_data["usage"]["prompt_tokens"]
                    output_tokens = resp_data["usage"]["completion_tokens"]
                    
                    processing_time = time.perf_counter() - start_time
                    return (
                        resp_data["choices"][0]["message"]["content"],
                        None,
                        processing_time,
                        input_tokens,
                        output_tokens
                    )
                    
                except Exception as e:
                    error_log.append(str(e))
                    print(f"Attempt {attempt+1} failed: {str(e)}")
                    if attempt < max_retries - 1:
                        sleep_time = retry_delay
                        print(f"Retrying in {sleep_time}s...")
                        time.sleep(sleep_time)
            
            raise Exception(f"All {max_retries} attempts failed. Errors: {', '.join(error_log)}")
            
        except Exception as e:
            processing_time = time.perf_counter() - start_time
            print(f"Final error: {str(e)}")
            return None, str(e), processing_time, 0, 0

class EvaluationPipeline:
    def __init__(self, video_dir):
        self.analyzer = GPT4Analyzer(video_dir)
    
    def process_dataset(self, audio_json, response_json, output_json):
        """Batch process dataset with full metrics"""
        total_start = time.perf_counter()
        
        with open(response_json, 'r') as f:
            step_data = json.load(f)
        
        with open(audio_json, 'r') as f:
            audio_data = json.load(f)

        audio_dict = {item["video_id"]: item for item in audio_data}

        dataset = []

        for step_item in step_data:
            video_id = step_item["video_id"]
            
            audio_item = audio_dict.get(video_id)
            
            if audio_item:
                merged_item = {
                    "video_id": video_id,
                    "audio_clue": audio_item["audio_clue"],
                    "ground_truth": step_item["ground_truth"],
                    "model_response": step_item["model_response"],
                    "step": step_item["step"]
                }
                dataset.append(merged_item)
            else:
                print(f"Warning: Missing audio data for video {video_id}")

        #dataset = dataset[:10]
        
        results = []
        total_processing_time = 0.0
        total_input_tokens = 0
        total_output_tokens = 0
        
        for item in tqdm(dataset, desc="Processing Videos"):
            raw_response, error, proc_time, in_toks, out_toks = self.analyzer.analyze_video(item)
            
            total_processing_time += proc_time
            total_input_tokens += in_toks
            total_output_tokens += out_toks
            
            result = {
                "video_id": item['video_id'],
                "ground_truth": item['ground_truth'],
                "model_response": item["model_response"],
                "step": item["step"],
                "score": raw_response,
                "input_tokens": in_toks,
                "output_tokens": out_toks
            }
            results.append(result)
        
        # Save results
        with open(output_json, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Calculate statistics
        total_time = time.perf_counter() - total_start
        avg_time = total_processing_time / len(dataset)
        avg_input_tokens = total_input_tokens / len(dataset)
        avg_output_tokens = total_output_tokens / len(dataset)
        
        # Print report
        print("\n=== Analysis Report ===")
        print(f"Total videos processed: {len(dataset)}")
        print(f"Total wall time: {timedelta(seconds=int(total_time))}")
        print(f"Total processing time: {timedelta(seconds=int(total_processing_time))}")
        print(f"Average time per video: {avg_time:.2f}s")
        print(f"\nToken Usage:")
        print(f"Total input tokens: {total_input_tokens}")
        print(f"Total output tokens: {total_output_tokens}")
        print(f"Average input tokens/video: {avg_input_tokens:.1f}")
        print(f"Average output tokens/video: {avg_output_tokens:.1f}")
        print(f"\nResults saved to: {output_json}")

def main():
    parser = argparse.ArgumentParser(description="GPT-4o Video Emotion Analysis")
    parser.add_argument("--response_json", type=str, default="",
                       help="Response JSON file path")
    parser.add_argument("--output_json", type=str, default="",
                       help="Output JSON file path")
    parser.add_argument("--audio_json", type=str, default="",
                       help="audio JSON file path")
    parser.add_argument("--video_dir", type=str, default="",
                       help="Base directory for video files")
    
    args = parser.parse_args()
    
    
    # Validate paths
    if not os.path.exists(args.video_dir):
        raise FileNotFoundError(f"Video directory not found: {args.video_dir}")
    
    # Run pipeline
    start_time = time.perf_counter()
    pipeline = EvaluationPipeline(args.video_dir)
    pipeline.process_dataset(args.audio_json, args.response_json, args.output_json)
    
    print(f"\nTotal execution time: {time.perf_counter()-start_time:.2f}s")

if __name__ == "__main__":
    main()


