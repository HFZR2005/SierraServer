import unittest
from tools.feedback import calculate_similarity, calculate_score, InvalidQAQError



class TestFeedback(unittest.TestCase):

    def test_calculate_similarity(self):
        QAQ = ["What is your name?", "My name is John.", "What is your age?"]
        score = calculate_similarity(QAQ)
        assert score >= 0.0
        assert score <= 1.0
   
    def test_calculate_score_on_single(self):
        QAQ = ["What is your name?", "My name is John.", "What is your age?"]
        score1 = calculate_score(QAQ)
        score2 = calculate_similarity(QAQ)

        assert score1 == score2

    def test_score(self):
        QResponseList = ["What is your name?", "My name is John.", "What is your age?", "What is your name?", "My name is John.", "What is your age?"]
        score = calculate_score(QResponseList)
        assert score >= 0.0
        assert score <= 1.0 

    def test_score_on_empty(self):
        with self.assertRaises(InvalidQAQError) as context:
            QResponseList = []
            score = calculate_score(QResponseList)

        self.assertTrue("QAQ list must be of length 3" in str(context.exception))
       
    def test_not_similar(self):
        QAQ = ["What is your name?", "The sky is Blue", "Toyota Corrolla?"]
        score = calculate_similarity(QAQ)
        print(score)
        assert score >= 0.0
        assert score <= 1.0
    
    def test_same_inputs(self):
        QAQ = ["What is your name?", "What is your name?", "What is your name?"]
        score = calculate_similarity(QAQ)
        print(score)

        assert score >= 0.0 
        assert score <= 1.0

if __name__ == "__main__":
    unittest.main()
