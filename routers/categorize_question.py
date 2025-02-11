import random 

# to implement properly using classifier

def get_category(question: str):
    categories = list(range(1, 6))
    return random.choice(categories)
