def format_success_response(hsn_code, description, validation_details):
    """Format response for valid HSN code"""
    return {
        "status": "valid",
        "hsn_code": hsn_code,
        "description": description,
        "validation_details": validation_details
    }

def format_error_response(hsn_code, error_message, validation_stage):
    """Format response for invalid HSN code"""
    response = {
        "status": "invalid",
        "hsn_code": hsn_code,
        "error": {
            "message": error_message,
            "type": f"{validation_stage}_error"
        }
    }
    
    # Add suggestions for existence errors
    if validation_stage == "existence":
        response["error"]["suggestions"] = get_similar_codes(hsn_code)
    
    return response

def get_similar_codes(hsn_code):
    """Get similar HSN codes for suggestions"""
    # Implementation would use data_loader to find similar codes
    return []