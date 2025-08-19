import argparse
import json
import re
from collections import defaultdict

def parse_score(score_str):
    match = re.search(r'<score>(.*?)</score>', score_str)
    return [int(m.group(1)) for m in re.finditer(r': (\d)/1', match.group(1))] if match else None

def calculate_metrics(scores):

    if not scores:
        return 0.0, 0.0, 0.0
    return scores[-1], sum(scores[:-1])/len(scores[:-1]) if len(scores)>1 else 0.0, len(scores)

def process_data(input_file):

    with open(input_file, 'r') as f:
        data = json.load(f)
    
    stats = {
        'total': {'acc':0, 'reason':0, 'count':0, 'step':0},
        'categories': defaultdict(lambda: {'acc':0, 'reason':0, 'count':0, 'step':0})
    }

    for entry in data:
        #print(entry['video_id'], type(entry['score']))
        scores = parse_score(str(entry['score']))
        if not scores: continue
        
        acc, reasoning, step = calculate_metrics(scores)
        cat = entry['ground_truth']
        if cat == 'angry':
            cat = 'anger'
        if cat == 'disgusted':
            cat = 'disgust'
        if cat == 'happy':
            cat = 'happiness'
        if cat == 'sad':
            cat = 'sadness'
        if cat == 'surprised':
            cat = 'surprise'

        stats['total']['acc'] += acc
        stats['total']['reason'] += reasoning
        stats['total']['step'] += step
        stats['total']['count'] += 1
        
        stats['categories'][cat]['acc'] += acc
        stats['categories'][cat]['reason'] += reasoning
        stats['categories'][cat]['step'] += step
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
        f.write(f"Avg Step: {avg_step:.1f}\n\n")
        
        f.write("=== Category Metrics ===\n")
        for cat in sorted(stats['categories']):
            c = stats['categories'][cat]
            cat_acc = c['acc'] / c['count'] if c['count'] else 0
            cat_reason = c['reason'] / c['count'] if c['count'] else 0
            cat_step = c['step'] / c['count'] if c['count'] else 0
            cat_score = args.alpha * cat_acc + (1 - args.alpha) * cat_reason
            
            f.write(f"Category: {cat}\n")
            f.write(f"  Recognition Score: {100*cat_acc:.1f}\n")
            f.write(f"  Reasoning Score: {100*cat_reason:.1f}\n")
            f.write(f"  CoT Score: {100*cat_score:.1f}\n")
            f.write(f"  Avg Step: {cat_step:.1f}\n")
            f.write("-"*40 + "\n")

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