import argparse
import json
import re
from collections import defaultdict

def parse_score(score_str):
    match = re.search(r'<score>(.*?)</score>', score_str)
    if not match:
        return None
    
    scores = []
  
    for m in re.finditer(r':\s*(\d+)/(\d+)', match.group(1)):
        numerator = int(m.group(1))
        denominator = int(m.group(2))
   
        if denominator == 0:
            scores.append(0.0)
        else:
            scores.append(numerator / denominator)
    return scores

def calculate_metrics(scores):
    if not scores:
        return 0.0, 0.0, 0
 
    acc_score = scores[-1]
    reasoning_scores = scores[:-1] if len(scores) > 1 else []
    reasoning_avg = sum(reasoning_scores)/len(reasoning_scores) if reasoning_scores else 0.0
    return acc_score, reasoning_avg, len(scores)

def process_data(data):

    
    stats = {
        'total': {'acc':0.0, 'reason':0.0, 'count':0, 'step':0}
    }

    for entry in data:
        scores = parse_score(str(entry['score']))
        if not scores: 
            continue
        
        acc, reasoning, step_count = calculate_metrics(scores)
        cat = entry['ground_truth']

 
        stats['total']['acc'] += acc
        stats['total']['reason'] += reasoning
        stats['total']['step'] += step_count
        stats['total']['count'] += 1
        
    return stats

def save_results(args, stats):
    total = stats['total']
    avg_acc = total['acc'] / total['count'] if total['count'] else 0
    avg_reason = total['reason'] / total['count'] if total['count'] else 0
    avg_step = total['step'] / total['count'] if total['count'] else 0
    combined_score = args.alpha * avg_acc + (1 - args.alpha) * avg_reason

    with open(args.output_txt, 'w') as f:
        f.write(f"Model: {args.model_name}\n")
        f.write(f"Alpha: {args.alpha:.1f}\n\n")
        
        f.write("=== Overall Metrics ===\n")
        f.write(f"Total Count: {total['count']}\n")
        f.write(f"Recognition Score: {100*avg_acc:.1f}\n")
        f.write(f"Reasoning Score: {100*avg_reason:.1f}\n")
        f.write(f"CoT Score: {100*combined_score:.1f}\n")
        f.write(f"Avg Steps: {avg_step:.1f}\n\n")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Emotion Analysis Metrics Calculator")
    parser.add_argument("--output_txt", type=str, default='', help="Output text file path")
    parser.add_argument("--model_name", type=str, default='', help="Name of the evaluated model")
    parser.add_argument("--alpha", type=float, default=0.5, help="Weighting factor", metavar="[0.0-1.0]")
    
    args = parser.parse_args()
    
  
    if not 0 <= args.alpha <= 1:
        raise ValueError("Lambda must be between 0 and 1")
    
    if args.model_name == 'AffectGPT':
        args.output_txt = '/metrics/results/Overall_affectgpt_metrics.txt'
        file_paths = [
            '/eval_cot/ER-Lab/results/ER_Lab_affectgpt_eval.json',
            '/eval_cot/ER-Wild/results/ER_SL_Wild_affectgpt_eval.json',
            '/eval_cot/ML-ER/results/ML_ER_affectgpt_eval.json',
            '/eval_cot/FG-ER/results/FG_ER_affectgpt_eval.json',
            '/eval_cot/Noise-ER/results/Noise_ER_affectgpt_eval.json',
            '/eval_cot/IR/results/IR_affectgpt_eval.json',
            '/eval_cot/SA/results/SA_affectgpt_eval.json',
            '/eval_cot/FG-SA/results/FG_SA_affectgpt_eval.json'
        ]
    
    if args.model_name == 'Audio_Reasoner':
        args.output_txt = '/metrics/results/Overall_audio_reasoner_metrics.txt'
        file_paths = [
            '/eval_cot/ER-Lab/results/ER_Lab_audio_reasoner_eval.json',
            '/eval_cot/ER-Wild/results/ER_SL_Wild_audio_reasoner_eval.json',
            '/eval_cot/ML-ER/results/ML_ER_audio_reasoner_eval.json',
            '/eval_cot/FG-ER/results/FG_ER_audio_reasoner_eval.json',
            '/eval_cot/Noise-ER/results/Noise_ER_audio_reasoner_eval.json',
            '/eval_cot/IR/results/IR_audio_reasoner_eval.json',
            '/eval_cot/SA/results/SA_audio_reasoner_eval.json',
            '/eval_cot/FG-SA/results/FG_SA_audio_reasoner_eval.json'
        ]

    if args.model_name == 'Emotion-LLaMA':
        args.output_txt = '/metrics/results/Overall_Emotion-LLaMA_metrics.txt'
        file_paths = [
            '/eval_cot/ER-Lab/results/ER_Lab_Emotion-LLaMA_eval.json',
            '/eval_cot/ER-Wild/results/ER_SL_Wild_Emotion-LLaMA_eval.json',
            '/eval_cot/ML-ER/results/ML_ER_Emotion-LLaMA_eval.json',
            '/eval_cot/FG-ER/results/FG_ER_Emotion-LLaMA_eval.json',
            '/eval_cot/Noise-ER/results/Noise_ER_Emotion-LLaMA_eval.json',
            '/eval_cot/IR/results/IR_Emotion-LLaMA_eval.json',
            '/eval_cot/SA/results/SA_Emotion-LLaMA_eval.json',
            '/eval_cot/FG-SA/results/FG_SA_Emotion-LLaMA_eval.json'
        ]

    if args.model_name == 'Gemini_2.0_Flash':
        args.output_txt = '/metrics/results/Overall_gemini_2.0_flash_metrics.txt'
        file_paths = [
            '/eval_cot/ER-Lab/results/ER_Lab_gemini_2.0_flash_eval.json',
            '/eval_cot/ER-Wild/results/ER_SL_Wild_gemini_2.0_flash_eval.json',
            '/eval_cot/ML-ER/results/ML_ER_gemini_2.0_flash_eval.json',
            '/eval_cot/FG-ER/results/FG_ER_gemini_2.0_flash_eval.json',
            '/eval_cot/Noise-ER/results/Noise_ER_gemini_2.0_flash_eval.json',
            '/eval_cot/IR/results/IR_gemini_2.0_flash_eval.json',
            '/eval_cot/SA/results/SA_gemini_2.0_flash_eval.json',
            '/eval_cot/FG-SA/results/FG_SA_gemini_2.0_flash_eval.json'
        ]

    if args.model_name == 'Gemini_2.5_Flash':
        args.output_txt = '/metrics/results/Overall_gemini_2.5_flash_metrics.txt'
        file_paths = [
            '/eval_cot/ER-Lab/results/ER_Lab_gemini_2.5_flash_eval.json',
            '/eval_cot/ER-Wild/results/ER_SL_Wild_gemini_2.5_flash_eval.json',
            '/eval_cot/ML-ER/results/ML_ER_gemini_2.5_flash_eval.json',
            '/eval_cot/FG-ER/results/FG_ER_gemini_2.5_flash_eval.json',
            '/eval_cot/Noise-ER/results/Noise_ER_gemini_2.5_flash_eval.json',
            '/eval_cot/IR/results/IR_gemini_2.5_flash_eval.json',
            '/eval_cot/SA/results/SA_gemini_2.5_flash_eval.json',
            '/eval_cot/FG-SA/results/FG_SA_gemini_2.5_flash_eval.json'
        ]

    if args.model_name == 'Gemini_2.5_Pro':
        args.output_txt = '/metrics/results/Overall_gemini_2.5_pro_metrics.txt'
        file_paths = [
            '/eval_cot/ER-Lab/results/ER_Lab_gemini_2.5_pro_eval.json',
            '/eval_cot/ER-Wild/results/ER_SL_Wild_gemini_2.5_pro_eval.json',
            '/eval_cot/ML-ER/results/ML_ER_gemini_2.5_pro_eval.json',
            '/eval_cot/FG-ER/results/FG_ER_gemini_2.5_pro_eval.json',
            '/eval_cot/Noise-ER/results/Noise_ER_gemini_2.5_pro_eval.json',
            '/eval_cot/IR/results/IR_gemini_2.5_pro_eval.json',
            '/eval_cot/SA/results/SA_gemini_2.5_pro_eval.json',
            '/eval_cot/FG-SA/results/FG_SA_gemini_2.5_pro_eval.json'
        ]

    if args.model_name == 'GPT-4.1':
        args.output_txt = '/metrics/results/Overall_gpt4.1_metrics.txt'
        file_paths = [
            '/eval_cot/ER-Lab/results/ER_Lab_gpt4.1_eval.json',
            '/eval_cot/ER-Wild/results/ER_SL_Wild_gpt4.1_eval.json',
            '/eval_cot/ML-ER/results/ML_ER_gpt4.1_eval.json',
            '/eval_cot/FG-ER/results/FG_ER_gpt4.1_eval.json',
            '/eval_cot/Noise-ER/results/Noise_ER_gpt4.1_eval.json',
            '/eval_cot/IR/results/IR_gpt4.1_eval.json',
            '/eval_cot/SA/results/SA_gpt4.1_eval.json',
            '/eval_cot/FG-SA/results/FG_SA_gpt4.1_eval.json'
        ]

    if args.model_name == 'GPT-4o':
        args.output_txt = '/metrics/results/Overall_gpt4o_metrics.txt'
        file_paths = [
            '/eval_cot/ER-Lab/results/ER_Lab_gpt4o_eval.json',
            '/eval_cot/ER-Wild/results/ER_SL_Wild_gpt4o_eval.json',
            '/eval_cot/ML-ER/results/ML_ER_gpt4o_eval.json',
            '/eval_cot/FG-ER/results/FG_ER_gpt4o_eval.json',
            '/eval_cot/Noise-ER/results/Noise_ER_gpt4o_eval.json',
            '/eval_cot/IR/results/IR_gpt4o_eval.json',
            '/eval_cot/SA/results/SA_gpt4o_eval.json',
            '/eval_cot/FG-SA/results/FG_SA_gpt4o_eval.json'
        ]

    if args.model_name == 'HumanOmni-7B':
        args.output_txt = '/metrics/results/Overall_humanomni_7b_metrics.txt'
        file_paths = [
            '/eval_cot/ER-Lab/results/ER_Lab_humanomni_7b_eval.json',
            '/eval_cot/ER-Wild/results/ER_SL_Wild_humanomni_7b_eval.json',
            '/eval_cot/ML-ER/results/ML_ER_humanomni_7b_eval.json',
            '/eval_cot/FG-ER/results/FG_ER_humanomni_7b_eval.json',
            '/eval_cot/Noise-ER/results/Noise_ER_humanomni_7b_eval.json',
            '/eval_cot/IR/results/IR_humanomni_7b_eval.json',
            '/eval_cot/SA/results/SA_humanomni_7b_eval.json',
            '/eval_cot/FG-SA/results/FG_SA_humanomni_7b_eval.json'
        ]

    if args.model_name == 'QVQ-72B':
        args.output_txt = '/metrics/results/Overall_qvq_72b_metrics.txt'
        file_paths = [
            '/eval_cot/ER-Lab/results/ER_Lab_qvq_72b_eval.json',
            '/eval_cot/ER-Wild/results/ER_SL_Wild_qvq_72b_eval.json',
            '/eval_cot/ML-ER/results/ML_ER_qvq_72b_eval.json',
            '/eval_cot/FG-ER/results/FG_ER_qvq_72b_eval.json',
            '/eval_cot/Noise-ER/results/Noise_ER_qvq_72b_eval.json',
            '/eval_cot/IR/results/IR_qvq_72b_eval.json',
            '/eval_cot/SA/results/SA_qvq_72b_eval.json',
            '/eval_cot/FG-SA/results/FG_SA_qvq_72b_eval.json'
        ]

    if args.model_name == 'Qwen2-Audio':
        args.output_txt = '/metrics/results/Overall_qwen2_audio_metrics.txt'
        file_paths = [
            '/eval_cot/ER-Lab/results/ER_Lab_qwen2_audio_eval.json',
            '/eval_cot/ER-Wild/results/ER_SL_Wild_qwen2_audio_eval.json',
            '/eval_cot/ML-ER/results/ML_ER_qwen2_audio_eval.json',
            '/eval_cot/FG-ER/results/FG_ER_qwen2_audio_eval.json',
            '/eval_cot/Noise-ER/results/Noise_ER_qwen2_audio_eval.json',
            '/eval_cot/IR/results/IR_qwen2_audio_eval.json',
            '/eval_cot/SA/results/SA_qwen2_audio_eval.json',
            '/eval_cot/FG-SA/results/FG_SA_qwen2_audio_eval.json'
        ]

    if args.model_name == 'Qwen2.5-Omni-7B':
        args.output_txt = '/metrics/results/Overall_qwen2.5_omni_7b_metrics.txt'
        file_paths = [
            '/eval_cot/ER-Lab/results/ER_Lab_qwen2.5_omni_7b_eval.json',
            '/eval_cot/ER-Wild/results/ER_SL_Wild_qwen2.5_omni_7b_eval.json',
            '/eval_cot/ML-ER/results/ML_ER_qwen2.5_omni_7b_eval.json',
            '/eval_cot/FG-ER/results/FG_ER_qwen2.5_omni_7b_eval.json',
            '/eval_cot/Noise-ER/results/Noise_ER_qwen2.5_omni_7b_eval.json',
            '/eval_cot/IR/results/IR_qwen2.5_omni_7b_eval.json',
            '/eval_cot/SA/results/SA_qwen2.5_omni_7b_eval.json',
            '/eval_cot/FG-SA/results/FG_SA_qwen2.5_omni_7b_eval.json'
        ]

    if args.model_name == 'Qwen2.5-VL-72B':
        args.output_txt = '/metrics/results/Overall_qwen2.5vl_72b_metrics.txt'
        file_paths = [
            '/eval_cot/ER-Lab/results/ER_Lab_qwen2.5vl_72b_eval.json',
            '/eval_cot/ER-Wild/results/ER_SL_Wild_qwen2.5vl_72b_eval.json',
            '/eval_cot/ML-ER/results/ML_ER_qwen2.5vl_72b_eval.json',
            '/eval_cot/FG-ER/results/FG_ER_qwen2.5vl_72b_eval.json',
            '/eval_cot/Noise-ER/results/Noise_ER_qwen2.5vl_72b_eval.json',
            '/eval_cot/IR/results/IR_qwen2.5vl_72b_eval.json',
            '/eval_cot/SA/results/SA_qwen2.5vl_72b_eval.json',
            '/eval_cot/FG-SA/results/FG_SA_qwen2.5vl_72b_eval.json'
        ]

    if args.model_name == 'Qwen2.5-VL-7B':
        args.output_txt = '/metrics/results/Overall_qwen2.5vl_7b_metrics.txt'
        file_paths = [
            '/eval_cot/ER-Lab/results/ER_Lab_qwen2.5vl_7b_eval.json',
            '/eval_cot/ER-Wild/results/ER_SL_Wild_qwen2.5vl_7b_eval.json',
            '/eval_cot/ML-ER/results/ML_ER_qwen2.5vl_7b_eval.json',
            '/eval_cot/FG-ER/results/FG_ER_qwen2.5vl_7b_eval.json',
            '/eval_cot/Noise-ER/results/Noise_ER_qwen2.5vl_7b_eval.json',
            '/eval_cot/IR/results/IR_qwen2.5vl_7b_eval.json',
            '/eval_cot/SA/results/SA_qwen2.5vl_7b_eval.json',
            '/eval_cot/FG-SA/results/FG_SA_qwen2.5vl_7b_eval.json'
        ]

    if args.model_name == 'Qwen2-VL-72B':
        args.output_txt = '/metrics/results/Overall_qwen2vl_72b_metrics.txt'
        file_paths = [
            '/eval_cot/ER-Lab/results/ER_Lab_qwen2vl_72b_eval.json',
            '/eval_cot/ER-Wild/results/ER_SL_Wild_qwen2vl_72b_eval.json',
            '/eval_cot/ML-ER/results/ML_ER_qwen2vl_72b_eval.json',
            '/eval_cot/FG-ER/results/FG_ER_qwen2vl_72b_eval.json',
            '/eval_cot/Noise-ER/results/Noise_ER_qwen2vl_72b_eval.json',
            '/eval_cot/IR/results/IR_qwen2vl_72b_eval.json',
            '/eval_cot/SA/results/SA_qwen2vl_72b_eval.json',
            '/eval_cot/FG-SA/results/FG_SA_qwen2vl_72b_eval.json'
        ]

    if args.model_name == 'Qwen2-VL-7B':
        args.output_txt = '/metrics/results/Overall_qwen2vl_7b_metrics.txt'
        file_paths = [
            '/eval_cot/ER-Lab/results/ER_Lab_qwen2vl_7b_eval.json',
            '/eval_cot/ER-Wild/results/ER_SL_Wild_qwen2vl_7b_eval.json',
            '/eval_cot/ML-ER/results/ML_ER_qwen2vl_7b_eval.json',
            '/eval_cot/FG-ER/results/FG_ER_qwen2vl_7b_eval.json',
            '/eval_cot/Noise-ER/results/Noise_ER_qwen2vl_7b_eval.json',
            '/eval_cot/IR/results/IR_qwen2vl_7b_eval.json',
            '/eval_cot/SA/results/SA_qwen2vl_7b_eval.json',
            '/eval_cot/FG-SA/results/FG_SA_qwen2vl_7b_eval.json'
        ]

    if args.model_name == 'R1-Omni-0.5B':
        args.output_txt = '/metrics/results/Overall_r1_omni_0.5b_metrics.txt'
        file_paths = [
            '/eval_cot/ER-Lab/results/ER_Lab_r1_omni_0.5b_eval.json',
            '/eval_cot/ER-Wild/results/ER_SL_Wild_r1_omni_0.5b_eval.json',
            '/eval_cot/ML-ER/results/ML_ER_r1_omni_0.5b_eval.json',
            '/eval_cot/FG-ER/results/FG_ER_r1_omni_0.5b_eval.json',
            '/eval_cot/Noise-ER/results/Noise_ER_r1_omni_0.5b_eval.json',
            '/eval_cot/IR/results/IR_r1_omni_0.5b_eval.json',
            '/eval_cot/SA/results/SA_r1_omni_0.5b_eval.json',
            '/eval_cot/FG-SA/results/FG_SA_r1_omni_0.5b_eval.json'
        ]

    if args.model_name == 'VideoLLaMA':
        args.output_txt = '/metrics/results/Overall_VideoLLaMA_metrics.txt'
        file_paths = [
            '/eval_cot/ER-Lab/results/ER_Lab_VideoLLaMA_eval.json',
            '/eval_cot/ER-Wild/results/ER_SL_Wild_VideoLLaMA_eval.json',
            '/eval_cot/ML-ER/results/ML_ER_VideoLLaMA_eval.json',
            '/eval_cot/FG-ER/results/FG_ER_VideoLLaMA_eval.json',
            '/eval_cot/Noise-ER/results/Noise_ER_VideoLLaMA_eval.json',
            '/eval_cot/IR/results/IR_VideoLLaMA_eval.json',
            '/eval_cot/SA/results/SA_VideoLLaMA_eval.json',
            '/eval_cot/FG-SA/results/FG_SA_VideoLLaMA_eval.json'
        ]

    if args.model_name == 'VideoLLaMA2':
        args.output_txt = '/metrics/results/Overall_VideoLLaMA2_metrics.txt'
        file_paths = [
            '/eval_cot/ER-Lab/results/ER_Lab_VideoLLaMA2_eval.json',
            '/eval_cot/ER-Wild/results/ER_SL_Wild_VideoLLaMA2_eval.json',
            '/eval_cot/ML-ER/results/ML_ER_VideoLLaMA2_eval.json',
            '/eval_cot/FG-ER/results/FG_ER_VideoLLaMA2_eval.json',
            '/eval_cot/Noise-ER/results/Noise_ER_VideoLLaMA2_eval.json',
            '/eval_cot/IR/results/IR_VideoLLaMA2_eval.json',
            '/eval_cot/SA/results/SA_VideoLLaMA2_eval.json',
            '/eval_cot/FG-SA/results/FG_SA_VideoLLaMA2_eval.json'
        ]

    if args.model_name == 'VideoLLaVA':
        args.output_txt = '/metrics/results/Overall_VideoLLaVA_metrics.txt'
        file_paths = [
            '/eval_cot/ER-Lab/results/ER_Lab_VideoLLaVA_eval.json',
            '/eval_cot/ER-Wild/results/ER_SL_Wild_VideoLLaVA_eval.json',
            '/eval_cot/ML-ER/results/ML_ER_VideoLLaVA_eval.json',
            '/eval_cot/FG-ER/results/FG_ER_VideoLLaVA_eval.json',
            '/eval_cot/Noise-ER/results/Noise_ER_VideoLLaVA_eval.json',
            '/eval_cot/IR/results/IR_VideoLLaVA_eval.json',
            '/eval_cot/SA/results/SA_VideoLLaVA_eval.json',
            '/eval_cot/FG-SA/results/FG_SA_VideoLLaVA_eval.json'
        ]       

   
    data = []
    for path in file_paths:
        with open(path, 'r') as f:
            data.extend(json.load(f))
    stats = process_data(data)
    save_results(args, stats)
    print(f"Metrics saved to {args.output_txt}")
