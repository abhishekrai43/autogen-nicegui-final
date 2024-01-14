from pathlib import Path

swear_file_path = Path(__file__).parent / 'swear.txt'
swear_words_set = set()

def load_swear_words():
    global swear_words_set
    if swear_file_path.exists():
        with open(swear_file_path, 'r') as file:
            swear_words_set = {line.strip().lower() for line in file}

load_swear_words()
def check_swear_words(message):        
    words_in_message = set(word.lower() for word in message.split())
    found_swear_words = words_in_message.intersection(swear_words_set)
    if found_swear_words:
        warning_message = f"Please avoid using inappropriate language. Found: {', '.join(found_swear_words)}"
        return warning_message