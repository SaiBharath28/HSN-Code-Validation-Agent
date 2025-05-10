import re

class HSNValidator:
    def __init__(self, data_loader):
        self.data_loader = data_loader
    
    def validate_format(self, hsn_code):
        """Validate HSN code format"""
        if not isinstance(hsn_code, str):
            return False, "HSN code must be a string"
        
        if not re.match(r'^\d{2,8}$', hsn_code):
            return False, "HSN code must be 2-8 digits"
        
        return True, "Format valid"
    
    def validate_existence(self, hsn_code):
        """Check if HSN code exists in master data"""
        description = self.data_loader.get_description(hsn_code)
        if description is None:
            return False, "HSN code not found in master data"
        return True, description
    
    def full_validation(self, hsn_code):
        """Perform complete validation"""
        # Format validation
        is_valid, message = self.validate_format(hsn_code)
        if not is_valid:
            return {
                'status': 'invalid',
                'error': message,
                'validation_stage': 'format'
            }
        
        # Existence validation
        is_valid, message = self.validate_existence(hsn_code)
        if not is_valid:
            return {
                'status': 'invalid',
                'error': message,
                'validation_stage': 'existence'
            }
        
        # Hierarchical validation (optional)
        hierarchy_valid, parent_codes = self.data_loader.validate_hierarchy(hsn_code)
        
        return {
            'status': 'valid',
            'description': message,
            'validation_details': {
                'format_valid': True,
                'exists_in_master': True,
                'hierarchy_valid': hierarchy_valid,
                'parent_codes': parent_codes
            }
        }
    
    def validate_multiple(self, hsn_codes):
        """Validate multiple HSN codes at once"""
        return [self.full_validation(code) for code in hsn_codes]