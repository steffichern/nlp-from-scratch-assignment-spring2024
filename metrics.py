import string
import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = file.read().splitlines()
    return data


# Identical, word for word
def exact_math(generated_outputs, ground_truths):
    exact_match = 0
    for i in range(len(generated_outputs)):
        if ground_truths[i] == generated_outputs[i]:
            exact_match += 1
    return exact_match / len(generated_outputs)


# tokenize text
def tokenize(text):
    translator = str.maketrans('', '', string.punctuation)   
    # Remove punctuation
    no_punctuation = text.translate(translator).lower()
    return no_punctuation.split()

# precision, recall, and F1
# Check if each token in the ground truth exists anywhere in the generated output

'''
True Positives (TP): Tokens that are present in both the prediction and the ground truth.
False Positives (FP): Tokens that are present in the prediction but not in the ground truth.
False Negatives (FN): Tokens that are not present in the prediction but are in the ground truth.
'''

def calculate_metrics(pred_tokens, truth_tokens):
    TP = sum(1 for token in pred_tokens if token in truth_tokens)
    FP = sum(1 for token in pred_tokens if token not in truth_tokens)
    FN = sum(1 for token in truth_tokens if token not in pred_tokens)

    if TP == 0:  # If there's no TP, precision and recall are both 0
        precision = recall = f1 = 0
    else:
        precision = TP / (TP + FP)
        recall = TP / (TP + FN)
        f1 = 2 * (precision * recall) / (precision + recall)

    return precision, recall, f1, TP, FP, FN

def calculate_macro_averaged_metrics(generated_outputs, ground_truths):
    total_recall = 0
    total_f1 = 0
    for gen_output, ground_truth in zip(generated_outputs, ground_truths):
        pred_tokens = tokenize(gen_output)
        truth_tokens = tokenize(ground_truth)
        
        precision, recall, f1, TP, FP, FN = calculate_metrics(pred_tokens, truth_tokens)
        total_recall += recall
        total_f1 += f1
    
    num_instances = len(generated_outputs)
    macro_averaged_recall = total_recall / num_instances
    macro_averaged_f1 = total_f1 / num_instances
    return macro_averaged_recall, macro_averaged_f1


# bootrap resampling
def bootstrap_resampling(generated_outputs, ground_truths, num_samples=1):
    num_instances = len(generated_outputs)
    f1_scores = []
    for _ in range(num_samples):
        sample_indices = np.random.choice(num_instances, num_instances, replace=True)
        sample_gen_outputs = [generated_outputs[i] for i in sample_indices]
        sample_ground_truths = [ground_truths[i] for i in sample_indices]
        macro_averaged_metrics = calculate_macro_averaged_metrics(sample_gen_outputs, sample_ground_truths)
        f1_scores.append(macro_averaged_metrics[1])
    return f1_scores

def bootstrap_resampling_all_models(model_outputs, ground_truths, num_samples=100):
    bootstrap_results = {
        'Llama': [],
        'Mistral': [],
        'Gemma': []
    }
    
    for _ in range(num_samples):
        # Bootstrap for each model
        for model_key, generated_outputs in model_outputs.items():
            sampled_f1_scores = bootstrap_resampling(generated_outputs, ground_truths, 1)  # 1 sample per bootstrap iteration
            bootstrap_results[model_key].extend(sampled_f1_scores)  # bootstrap_resampling returns a list
    
    return bootstrap_results


# ANOVA for significant testing
def anova(f1_llama, f1_mistral, f1_gemma):
    f1_llama = np.array(f1_llama)
    f1_mistral = np.array(f1_mistral)
    f1_gemma = np.array(f1_gemma)
    f, p = stats.f_oneway(f1_llama, f1_mistral, f1_gemma)
    return f, p

# Tukey's HSD for pairwise comparison
def tukey_hsd(f1_llama, f1_mistral, f1_gemma):
    f1_llama = np.array(f1_llama)
    f1_mistral = np.array(f1_mistral)
    f1_gemma = np.array(f1_gemma)
    f1_scores = np.concatenate([f1_llama, f1_mistral, f1_gemma])
    labels = ['llama'] * len(f1_llama) + ['mistral'] * len(f1_mistral) + ['gemma'] * len(f1_gemma)
    tukey_results = pairwise_tukeyhsd(f1_scores, labels, 0.05)
    return tukey_results


# Run!
generated_outputs_llama = load_data('./data/test/answers_our_llama.txt')
ground_truths_llama = load_data('./data/test/reference_answers.txt')

print("Exact Match (Llama):", exact_math(generated_outputs_llama, ground_truths_llama))
macro_averaged_llama = calculate_macro_averaged_metrics(generated_outputs_llama, ground_truths_llama)
print("Recall (Llama): ", macro_averaged_llama[0], "\nMacro-averaged F1 (Llama): ", macro_averaged_llama[1])

generated_outputs_mistral = load_data('./data/test/answers_our_mistral.txt')
ground_truths_mistral = load_data('./data/test/reference_answers.txt')

print("Exact Match (Mistral):", exact_math(generated_outputs_mistral, ground_truths_mistral))
macro_averaged_mistral = calculate_macro_averaged_metrics(generated_outputs_mistral, ground_truths_mistral)
print("Recall (Mistral): ", macro_averaged_mistral[0], "\nMacro-averaged F1 (Mistral): ", macro_averaged_mistral[1])

generated_outputs_gemma = load_data('./data/test/answers_our_gemma.txt')
ground_truths_gemma = load_data('./data/test/reference_answers.txt')

print("Exact Match (Gemma):", exact_math(generated_outputs_gemma, ground_truths_gemma))
macro_averaged_gemma = calculate_macro_averaged_metrics(generated_outputs_gemma, ground_truths_gemma)
print("Recall (Gemma): ", macro_averaged_gemma[0], "\nMacro-averaged F1 (Gemma): ", macro_averaged_gemma[1])

# Bootstrap resampling
model_outputs = {
    'Llama': generated_outputs_llama,
    'Mistral': generated_outputs_mistral,
    'Gemma': generated_outputs_gemma
}
bootstrap_results = bootstrap_resampling_all_models(model_outputs, ground_truths_llama, num_samples=100)
#print("Bootstrap Results:", bootstrap_results)

# ANOVA
f_stat, p_val = anova(bootstrap_results['Llama'], bootstrap_results['Mistral'], bootstrap_results['Gemma'])
print("F-statistic:", f_stat, "\nP-value:", p_val, "\nReject Null Hypothesis:", p_val < 0.05)

# get f1 scores mean
print("F1 scores mean (Llama):", np.mean(bootstrap_results['Llama']), "\nF1 scores mean (Mistral):", np.mean(bootstrap_results['Mistral']), "\nF1 scores mean (Gemma):", np.mean(bootstrap_results['Gemma']))

# Tukey's HSD
tukey_results = tukey_hsd(bootstrap_results['Llama'], bootstrap_results['Mistral'], bootstrap_results['Gemma'])
print(tukey_results)



