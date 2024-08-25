# recommendation.py

import google.generativeai as genai
from database import search_items

# Configure the Gemini API (make sure to set your API key in the environment variables)
genai.configure(api_key="AIzaSyD3kFTAAPuQvos29RBY5n_AtFcuHUpCvN8")

def get_outfit_recommendation(prompt):
    # Retrieve relevant items from the database
    relevant_items = search_items(prompt, n_results=5)
    
    # Prepare the context for Gemini
    context = "Wardrobe items:\n" + "\n".join([item['description'] for item in relevant_items])
    
    # Set up the model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Prepare the prompt
    full_prompt = f"""
    Given the following items in the user's wardrobe:
    {context}

    And the user's request:
    "{prompt}"

    Please suggest an outfit using the available items. If there are not enough suitable items, 
    suggest what additional items might complement the outfit. Provide a brief explanation for your choices.

    Format your response as follows:
    Suggested Outfit:
    - [Item 1]
    - [Item 2]
    ...

    Explanation:
    [Your explanation here]

    Additional Suggestions (if any):
    - [Suggestion 1]
    - [Suggestion 2]
    ...
    """
    
    # Generate recommendation
    response = model.generate_content(full_prompt)
    
    return response.text

# Example usage:
# recommendation = get_outfit_recommendation("I need an outfit for a casual summer day")
# print(recommendation)