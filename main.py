import json
from pyodide.http import pyfetch
from js import document, console

# 1. DEFINE THE STRICT DIET DATA (Your "Context")
# This ensures the AI never hallucinates butter or cream.
DIET_CONTEXT = """
You are a bodybuilding chef. Create a delicious recipe using ONLY these allowed ingredients.
Strictly adhere to the gram measurements.

PROTEIN (Choose ONE):
- 170g-200g Chicken Breast (Raw)
- 170g-200g Turkey Breast
- 200g White Fish
- 170g Flank Steak
- 250g Egg Whites + 2 Whole Eggs

CARBS (Choose ONE):
- 150g Jasmine Rice (Cooked Weight)
- 225g Potato/Sweet Potato (Raw Weight)
- 2 Slices Ezekiel Bread

FATS (Choose ONE - Only if Protein is NOT Steak/Eggs):
- 15ml Olive/Macadamia Oil
- 80g Avocado
- 16g Peanut Butter

VEGGIES (Unlimited):
- Spinach, Broccoli, Asparagus, Zucchini, Cucumber.

SEASONINGS (Unlimited):
- Salt, Pepper, Garlic/Onion Powder, Paprika, Hot Sauce, Soy Sauce (Low sodium), Lemon juice.
NO SUGAR, NO BUTTER, NO CREAM.
"""

async def generate_recipe(*args):
    # Get the vibe Mum selected
    vibe = document.getElementById("cuisine").value
    
    # Show loading state
    document.getElementById("loading").style.display = "block"
    document.getElementById("recipe-output").innerHTML = ""

    # Construct the user prompt
    prompt = f"Create a {vibe} meal. Output format: Title, Ingredients (with EXACT grams), and Instructions."

    # Prepare the payload for your API (OpenAI or your Proxy)
    # Note: Replace 'YOUR_BACKEND_URL' with the secure endpoint you create
    body = json.dumps({
        "messages": [
            {"role": "system", "content": DIET_CONTEXT},
            {"role": "user", "content": prompt}
        ]
    })

    try:
        # This uses PyScript's fetch to hit your endpoint
        response = await pyfetch(
            url="YOUR_BACKEND_URL", 
            method="POST", 
            headers={"Content-Type": "application/json"}, 
            body=body
        )
        
        data = await response.json()
        recipe_text = data['choices'][0]['message']['content']
        
        # Format the output for HTML (replace newlines with breaks)
        formatted_html = recipe_text.replace("\n", "<br>")
        
        # Display to Mum
        document.getElementById("recipe-output").innerHTML = formatted_html

    except Exception as e:
        document.getElementById("recipe-output").innerHTML = "Oops! Something went wrong. Try again."
        console.log(f"Error: {e}")

    finally:
        document.getElementById("loading").style.display = "none"
