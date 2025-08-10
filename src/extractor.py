import json

def extractor(llm, conversation_history):
    prompt = f'''
## CONTEXT ##
Analyze the following Fashion e-commerce conversation history:
{conversation_history}

## TASK ##
Extract and infer relevant information about the customer's primary product request, focusing only on the parameters specified below. If multiple products are mentioned, focus on the first or main product. Make reasonable assumptions based on context, but do not introduce information outside the given categories.

## GUIDELINES ##
1. Category: Choose ONE from Indian Wear, Plus Size, Western, Sports Wear, Inner Wear & Sleep Wear, Lingerie & Sleep Wear. If none fit, use "Other". If multiple categories apply, choose the most relevant for the main product.
2. Individual Category: Choose ONE from kurta-sets, kurtas, tops, thermal-tops, jeans, skirts, shorts, trousers, palazzos, jumpsuit, co-ords, clothing-set, kurtis, tunics, saree, lehengas, anarkalis, salwar-kameez, dupattas, blouses, ethnic-dresses, traditional-wear. If none fit, use "Other".
3. Category by Gender: Choose Women or Men. If unclear, use your best judgment.
4. Colour: Choose from Black, Orange, Navy Blue, Red, Beige, Yellow, Green, Mustard, Teal, Peach, Blue, Sea Green, Pink, Burgundy, Maroon, Lavender, Purple, White, Grey, Lime Green, Brown, Cream, Rust, Off White, Turquoise Blue, Multi, Mauve, Assorted, Magenta, Fuchsia, Coral, Olive, Rose, Gold, Fluorescent Green, Silver, Nude, Violet, Charcoal, Grey Melange, Khaki, Coffee Brown, Taupe, Copper. If unclear or not listed, use "Other".

5. Move On:
   - Use "true" if Category, Individual Category, and at least one of Colour or Category by Gender are available.
   - Otherwise use "false".

6. Follow-up Message:
   - If Move On is true, confirm intent to search.
   - If false, ask for missing required fields or clarify.
   - If non-fashion product is detected, reply with an appropriate error message.

## IMPORTANT NOTES ##
- Respond ONLY for fashion-related products.
- Do not invent fields or make assumptions outside the provided options.
- Use "NA" if something cannot be inferred or is missing.
- Map similar terms: "saree" = "saree", "kurta" = "kurtas", "kurti" = "kurtis", "dress" = "ethnic-dresses"

## OUTPUT FORMAT ##
Respond in this exact format:

Category: "..."
Individual_category: "..."
category_by_Gender: "..."
colour: "..."
MOVE_ON: "true" or "false"
FOLLOW_UP_MESSAGE: "..."

Input: {conversation_history}

Your output:
'''

    response = llm.invoke(prompt)

    # ------------------- Parse ------------------------
    parsed_data = {
        "Category": "NA",
        "Individual_category": "NA",
        "category_by_Gender": "NA",
        "colour": "NA",
        "MOVE_ON": False,
        "FOLLOW_UP_MESSAGE": "Please provide more details like color, category (Indian/Western), product type (kurti, jeans, etc.), and gender."
    }

    try:
        lines = response.content.strip().split("\n")
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().strip('"')

                if key in parsed_data:
                    if key == "MOVE_ON":
                        parsed_data[key] = value.lower() == "true"
                    else:
                        parsed_data[key] = value

        # Fill follow-up message if present
        if "FOLLOW_UP_MESSAGE" in response.content:
            follow_up = [l for l in lines if "FOLLOW_UP_MESSAGE" in l]
            if follow_up:
                parsed_data["FOLLOW_UP_MESSAGE"] = follow_up[0].split(":", 1)[1].strip().strip('"')

    except Exception as e:
        print("❌ Extractor Parsing Error:", e)

    return parsed_data




# import json
# import re

# def extractor(llm, query):
#     try:
#         response = llm.invoke(query)

#         # If response is a Langchain Message object, extract content
#         if hasattr(response, 'content'):
#             response_text = response.content
#         else:
#             response_text = str(response)

#         print("Raw LLM Response:\n", response_text)

#         # Extract JSON block from text using regex
#         json_match = re.search(r"\{.*?\}", response_text, re.DOTALL)
#         if json_match:
#             json_text = json_match.group()
#             parsed_json = json.loads(json_text)
#             print("✅ Extracted JSON:", parsed_json)
#             return parsed_json
#         else:
#             raise ValueError("LLM output did not contain valid JSON.")

#     except Exception as e:
#         print("❌ Error in extractor:", str(e))
#         return {}







# BELOW THIS IS THE ORIGINAL VERSION

# def extractor(llm, conversation_history):
#     prompt = f'''
#     ## CONTEXT ##
#     Analyze the following Fashion e-commerce conversation history:
#     {conversation_history}

#     ## TASK ##
#     Extract and infer relevant information about the customer's primary product request, focusing only on the parameters specified below. If multiple products are mentioned, focus on the first or main product. Make reasonable assumptions based on context, but do not introduce information outside the given categories.

#     ## GUIDELINES ##
#     1. Category: Choose ONE from Indian Wear, Plus Size, Western, Sports Wear, Inner Wear & Sleep Wear, Lingerie & Sleep Wear. If none fit, use "Other". If multiple categories apply, choose the most relevant for the main product.
#     2. Individual Category: Choose ONE from kurta-sets, kurtas, tops, thermal-tops, jeans, skirts, shorts, trousers, palazzos, jumpsuit, co-ords, clothing-set, kurtis, tunics. If none fit, use "Other". This should correspond to the main product if multiple are mentioned.
#     3. Category by Gender: Choose Women or Men. If unclear, use your best judgment based on the conversation.
#     4. Colour: Choose from Black, Orange, Navy Blue, Red, Beige, Yellow, Green, Mustard, Teal, Peach, Blue, Sea Green, Pink, Burgundy, Maroon, Lavender, Purple, White, Grey, Lime Green, Brown, Cream, Rust, Off White, Turquoise Blue, Multi, Mauve, Assorted, Magenta, Fuchsia, Coral, Olive, Rose, Gold, Fluorescent Green, Silver, Nude, Violet, Charcoal, Grey Melange, Khaki, Coffee Brown, Taupe, Copper. If the color isn't listed or multiple colors are mentioned, use "Other" or the color of the main product.
#     5. Move On: Determine if enough key information (at least Category, Individual Category, and one of either Colour or Category by Gender) has been gathered for the main product to proceed to product searching. Use "true" only if these are available, otherwise "false".
#     6. Follow-up Message:
#        - If Move On is "true", provide a confirmation message to proceed with searching for the main product.
#        - If Move On is "false", ask a question to gather missing key information (Category, Individual Category, Colour, or Category by Gender) for the main product.
#        - If multiple products were mentioned, acknowledge this in your follow-up message and confirm focus on the main product.
#        - Phrase questions to elicit specific, relevant information.
#        - If any other product other than fashion is mentioned then give an appropriate error message. As we can only show fashion products.

#     ## IMPORTANT NOTES ##
#     - If any other product other than fashion is mentioned then give an appropriate error message. As we can only show fashion products.
#     - If multiple products are mentioned, focus on extracting information for the first or main product mentioned.
#     - Stick strictly to the categories provided. Do not invent or introduce new parameters.
#     - If information for a category is not available and can't be reasonably inferred, use "NA".

#     ## OUTPUT FORMAT ##
#     Respond with the information in the following format:

#     Category: "Extracted or inferred category for main product"
#     Individual_category: "Extracted or inferred individual category for main product"
#     category_by_Gender: "Extracted or inferred gender category"
#     colour: "Extracted or inferred colour for main product"
#     MOVE_ON: "true" or "false"
#     FOLLOW_UP_MESSAGE: "Your context-aware follow-up message"

#     Your Input: {conversation_history}
#     Your output:
#     '''

#     response = llm.invoke(prompt)
    
#     return response.content
