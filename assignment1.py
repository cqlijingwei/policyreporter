from typing import List, Dict
import unittest


def calculate_recall(tp: int, fn: int) -> float:
    """
    Calculate recall
    :param tp: True Positive
    :param fn: False Negative
    :return: Recall
    """
    if tp + fn == 0:
        raise ValueError("True positive and false negative cannot sum to zero!")
    return tp / (tp + fn)

def calculate_f1(tp: int, fn: int, fp: int) -> float:
    """
    Calculate F1 score
    :param tp: True Positive
    :param fn: False Negative
    :param fp: False Positive
    :return: F1 Score
    """
    if tp + fp == 0:
        raise ValueError("True positive and false positive cannot sum to zero!")
    precision = tp / (tp + fp)
    if tp + fn == 0:
        raise ValueError("True positive and false negative cannot sum to zero!")
    recall = tp / (tp + fn)
    if precision + recall == 0:
        raise ValueError("Precision and recall cannot sum to zero!")
    f1 = 2 * precision * recall / (precision + recall)
    return f1

def find_best_threshold(threshold_data: List[Dict[str, int]]) -> float:
    """
    find the best threshold which makes recall >= 0.9 
    :param threshold_data: contains different thresholds and corresponding results list
    :return: best threshold
    """
    best_threshold = None
    f1_score = 0.0
    for data in threshold_data:
        try:
            recall = calculate_recall(data['tp'], data['fn'])
            if recall >= 0.9:
                cur_f1 = calculate_f1(data['tp'], data['fn'], data['fp'])
                if best_threshold is None or cur_f1 > f1_score:
                    best_threshold = data['threshold']
        except ValueError as e:
            print(f"Error calculating recall for threshold {data['threshold']}: {e}")
    
    if best_threshold is None:
        raise ValueError("Threshold not found to make recall >= 0.9 ")
    
    return best_threshold

# sample data
threshold_data = [
    {'threshold': 0.1, 'tp': 80, 'tn': 20, 'fp': 10, 'fn': 5},
    {'threshold': 0.2, 'tp': 85, 'tn': 25, 'fp': 15, 'fn': 10},
    {'threshold': 0.3, 'tp': 90, 'tn': 30, 'fp': 20, 'fn': 15},
    # more data...
]

# call function
best_threshold = find_best_threshold(threshold_data)
print(f"best threshold: {best_threshold}")

class TestThresholdFinder(unittest.TestCase):
    def test_find_best_threshold(self):
        threshold_data = [
            {'threshold': 0.1, 'tp': 80, 'tn': 20, 'fp': 10, 'fn': 5},
            {'threshold': 0.2, 'tp': 85, 'tn': 25, 'fp': 15, 'fn': 10},
            {'threshold': 0.3, 'tp': 90, 'tn': 30, 'fp': 20, 'fn': 15},
        ]
        best_threshold = find_best_threshold(threshold_data)
        self.assertEqual(best_threshold, 0.1) # 0.1 is the only threshold with recall >= 0.9

    def test_no_valid_threshold(self):
        threshold_data = [
            {'threshold': 0.1, 'tp': 80, 'tn': 20, 'fp': 10, 'fn': 20},
            {'threshold': 0.2, 'tp': 85, 'tn': 25, 'fp': 15, 'fn': 25},
        ]
        with self.assertRaises(ValueError):
            find_best_threshold(threshold_data)

if __name__ == '__main__':
    unittest.main()