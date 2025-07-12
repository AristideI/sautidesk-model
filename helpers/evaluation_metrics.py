import numpy as np
from datasets import evaluate
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments
import evaluate


rouge = evaluate.load("rouge")


def compute_metrics(eval_preds):
    preds, labels = eval_preds
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    # Strip whitespace
    decoded_preds = [pred.strip() for pred in decoded_preds]
    decoded_labels = [label.strip() for label in decoded_labels]

    # Compute ROUGE
    rouge_result = rouge.compute(
        predictions=decoded_preds, references=decoded_labels, use_stemmer=True
    )

    # Exact match
    exact_matches = [int(p == l) for p, l in zip(decoded_preds, decoded_labels)]
    exact_match_score = np.mean(exact_matches)

    return {
        "rouge1": rouge_result["rouge1"],
        "rouge2": rouge_result["rouge2"],
        "rougeL": rouge_result["rougeL"],
        "exact_match": exact_match_score,
    }
