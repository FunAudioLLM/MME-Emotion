import argparse
import json
import time
import os
from openai import OpenAI
from tqdm import tqdm

def process_entry(model, client, entry):
    messages = [
        {
            "role": "system",
            "content": "You are an expert in affective computing and very good at handling tasks related to emotion recognition."
        },
        {
            "role": "user",
            "content": f"Given the following answer about the emotion conveyed in a video, "
                       f"please help me extract several key steps from the answer. Each step should be as concise as "
                       f"possible and prefixed with Step X. In the last step, showcase the predicted emotion. If there "
                       f"are no reasoning steps, please showcase the predicted emotion at Step 1. Enclose your result "
                       f"within <step></step> tags.\n"
                       f"answer: '{entry['model_response']}'\n"
                       f"Example 1:\n"
                       f"answer: In the video, an elderly man wearing a green shirt is in an outdoor nighttime setting. He appears focused and serious, with slightly "
                       f"furrowed brows and a serious expression. His eyes are scanning the other person, suggesting he wants to convey something important or ask about "
                       f"a certain thing. As time passes, his gaze shifts from scanning to direct engagement, eventually relaxing and showing a hint of happiness, "
                       f"indicating fluctuations in his emotions. Overall, the elderly man experiences a moderate intensity of neutral emotion, mixed with slight "
                       f"positive fluctuations.\n"
                       f"result: <step>Step 1: Observe the setting and characters in the video, noting any relevant details such as location and participants' appearance. "  
                       f"Step 2: Analyze the facial expressions and movements, such as furrowed brows and downturned eyes, looking for indicators of specific emotions. "  
                       f"Step 3: Consider verbal and non-verbal cues, including mouth movements and gaze direction, that signify communication and emotional responses. "
                       f"Step 4: Synthesize observations to understand the overall emotional state conveyed by the participant. "
                       f"Step 5: Based on the analysis, determine that the predicted emotion is neutral.</step>\n"
                       f"Example 2:\n"
                       f"answer: happy\n"
                       f"result: <step>Step 1: The predicted emotion is happy.</step>"
        }
    ]

    max_retries = 10
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.0
            )
            result = response.choices[0].message.content
            entry['step'] = result
            return True

        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                entry['step'] = f"Error: {str(e)}"
                return False
    return False

def process_json_file(input_file, output_file, model_name, api_key, base_url):
    
    with open(input_file, 'r') as f:
        data = json.load(f)

    #data = data[:10]

    client = OpenAI(api_key=api_key, base_url=base_url)

    success_count = 0
    for entry in tqdm(data, desc="Processing entries"):

        if 'label_set' in entry:
            del entry['label_set']
        if process_entry(model_name, client, entry):
            success_count += 1

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nProcessing completed. Success: {success_count}/{len(data)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process emotion recognition results with GPT-4")
    parser.add_argument("--input_json", type=str, default='', help="Input JSON file path")
    parser.add_argument("--output_json", type=str, default='', help="Input JSON file path")
    parser.add_argument("--model", type=str, default='gpt-4.1-2025-04-14', help="OpenAI model name")
    parser.add_argument("--api_key", type=str, default='', help="OpenAI API key")
    parser.add_argument("--base_url", type=str, default='', help="API base URL")
    
    args = parser.parse_args()

    process_json_file(
        input_file=args.input_json,
        output_file=args.output_json,
        model_name=args.model,
        api_key=args.api_key,
        base_url=args.base_url
    )