def parser(response):
    # Initialize with default values
    parsed_data = {
        "Category": response.get("Category", "NA"),
        "Individual_category": response.get("Individual_category", "NA"),
        "category_by_Gender": response.get("category_by_Gender", "NA"),
        "colour": response.get("colour", "NA"),
        "MOVE_ON": False,
        "FOLLOW_UP_MESSAGE": "NA"
    }

    # Check if all required fields are present and not empty
    required_fields = ["Category", "Individual_category", "category_by_Gender", "colour"]
    all_fields_present = all(response.get(field) for field in required_fields)

    if all_fields_present:
        parsed_data["MOVE_ON"] = True
        parsed_data["FOLLOW_UP_MESSAGE"] = ""
    else:
        parsed_data["MOVE_ON"] = False
        parsed_data["FOLLOW_UP_MESSAGE"] = (
            "Please provide more details like color, category (Indian/Western), product type (kurti, jeans, etc.), and gender."
        )

    return parsed_data