import json
import asyncio
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

# --- CONFIGURATION ---
# PASTE YOUR NEW PIPEDREAM URL HERE
BACKEND_URL = "https://eozuh4g8hv307dt.m.pipedream.net" 

async def generate_recipe(*args):
    # 1. Get the vibe Mum selected
    vibe = document.getElementById("cuisine").value
    
    # 2. UI: Show loading, hide old result
    document.getElementById("loading").style.display = "block"
    document.getElementById("recipe-output").innerHTML = ""

    # 3. Prepare the simple package (Just the vibe!)
    # We moved the Diet Rules to the backend to keep them safe.
    payload = json.dumps({
        "vibe": vibe
    })

    try:
        # 4. Send the signal to Pipedream
        response = await pyfetch(
            url=BACKEND_URL, 
            method="POST", 
            headers={"Content-Type": "application/json"}, 
            body=payload
        )
        
        # 5. Get the text back
        if response.ok:
            recipe_text = await response.json() 
            # Note: If Pipedream returns raw text, use await response.string() instead
            
            # 6. Format and Display
            # Simple formatter to make it look nice in HTML
            formatted_html = recipe_text.replace("\n", "<br>")
            document.getElementById("recipe-output").innerHTML = formatted_html
        else:
            console.log(f"Server Error: {response.status}")
            document.getElementById("recipe-output").innerHTML = "Error connecting to the kitchen!"

    except Exception as e:
        document.getElementById("recipe-output").innerHTML = f"Something went wrong. Tell [Your Name] to fix the code!<br>Error: {e}"
        console.log(f"Python Error: {e}")

    finally:
        document.getElementById("loading").style.display = "none"
