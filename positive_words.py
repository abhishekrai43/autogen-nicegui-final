# Respond back to the user first , THEN send it to the LLM
resp_first_then_llm ={
    'Coca Cola':'The Coca-Cola Company is an American multinational corporation founded in 1892'
}

# Add the Value string to the answer that LLM Provided
llm_then_resp ={
    'Time Management':'Casio Watches since 1956',
    'Good Habits':'Yoga'
}
# Respond back to the user without sending anything to the LLM
resp_no_llm = {
    'babycare': '<a href="https://www.cardinalhealth.com/en/product-solutions/medical/woman-and-baby/mom-and-baby-care.html">Baby Care</a>"',
    'oral health':'<a href="https://www.stryker.com/us/en/portfolios/medical-surgical-equipment/oral-hygiene.html">Oral Health</a>'
}
def resp_only(sentence):
    '''Returns a formatted message with a link if found in user query'''
    lower_case_sentence = sentence.lower()
    for key, url in resp_no_llm.items():
        if key.lower() in lower_case_sentence:
            return f"You might find this interesting: {url}"
    return None



# Respond back to the user first , THEN send it to the LLM
def resp_llm(sentence):
    '''Returns the value for key in resp_first_then_llm if found in user query'''
    lower_case_sentence = sentence.lower()
    for key, resp in resp_first_then_llm.items():
        if key.lower() in lower_case_sentence:
            return resp
    return None

def llm_resp(sentence):
    '''Returns the value for key in llm_then_resp if found in user query'''
    lower_case_sentence = sentence.lower()
    for key, resp in llm_then_resp.items():
        if key.lower() in lower_case_sentence:
            return resp
    return None
