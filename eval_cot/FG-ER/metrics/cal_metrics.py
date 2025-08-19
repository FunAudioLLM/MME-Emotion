import argparse
import json
import re
from collections import defaultdict

def parse_score(score_str):
    match = re.search(r'<score>(.*?)</score>', score_str)
    if not match:
        return None
    
    scores = []
    # 匹配分数模式（支持任意分母）
    for m in re.finditer(r':\s*(\d+)/(\d+)', match.group(1)):
        numerator = int(m.group(1))
        denominator = int(m.group(2))
        # 处理分母为0的异常情况
        if denominator == 0:
            scores.append(0.0)
        else:
            scores.append(numerator / denominator)
    return scores

def calculate_metrics(scores):
    if not scores:
        return 0.0, 0.0, 0
    # 最后一步为识别分数，前几步平均为推理分数
    acc_score = scores[-1]
    reasoning_scores = scores[:-1] if len(scores) > 1 else []
    reasoning_avg = sum(reasoning_scores)/len(reasoning_scores) if reasoning_scores else 0.0
    return acc_score, reasoning_avg, len(scores)

def process_data(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    stats = {
        'total': {'acc':0.0, 'reason':0.0, 'count':0, 'step':0},
        'categories': defaultdict(lambda: {'acc':0.0, 'reason':0.0, 'count':0, 'step':0})
    }

    for entry in data:
        scores = parse_score(str(entry['score']))
        if not scores: 
            continue
        
        acc, reasoning, step_count = calculate_metrics(scores)
        cat = entry['ground_truth']

        # 更新统计信息（使用浮点累加）
        stats['total']['acc'] += acc
        stats['total']['reason'] += reasoning
        stats['total']['step'] += step_count
        stats['total']['count'] += 1
        
        stats['categories'][cat]['acc'] += acc
        stats['categories'][cat]['reason'] += reasoning
        stats['categories'][cat]['step'] += step_count
        stats['categories'][cat]['count'] += 1

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
    parser.add_argument("--input_json", type=str, default='', help="Input JSON file path")
    parser.add_argument("--output_txt", type=str, default='', help="Output text file path")
    parser.add_argument("--model_name", type=str, default='', help="Name of the evaluated model")
    parser.add_argument("--alpha", type=float, default=0.5, help="Weighting factor", metavar="[0.0-1.0]")
    
    args = parser.parse_args()
    
  
    if not 0 <= args.alpha <= 1:
        raise ValueError("Lambda must be between 0 and 1")
    
 
    stats = process_data(args.input_json)
    save_results(args, stats)
    print(f"Metrics saved to {args.output_txt}")