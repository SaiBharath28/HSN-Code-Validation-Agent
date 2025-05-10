import pandas as pd
from pathlib import Path

class HSNDataLoader:
    def __init__(self, data_path, verbose=False):
        self.data_path = Path(data_path)
        self.hsn_data = None
        self.trie = None
        self.verbose = verbose  # Control for debug prints

    def load_data(self):
        """Load and preprocess HSN data from Excel with robust error handling"""
        try:
            if not self.data_path.exists():
                raise FileNotFoundError(f"Excel file not found at: {self.data_path}")

            df = self._read_excel_with_fallback()

            df.columns = df.columns.str.strip().str.lower()
            required_columns = {'hsncode', 'description'}
            if not required_columns.issubset(df.columns):
                missing = required_columns - set(df.columns)
                raise ValueError(f"Missing required columns: {missing}")

            df['hsncode'] = df['hsncode'].astype(str).str.replace(' ', '').str.strip()
            df['description'] = df['description'].astype(str).str.strip()

            df = df.dropna(subset=['hsncode'])

            self.hsn_data = df.set_index('hsncode').to_dict()['description']
            self._build_trie()

            if self.verbose:
                print(f"Successfully loaded {len(self.hsn_data)} HSN codes")

            return True

        except Exception as e:
            print(f"Error loading data: {str(e)}")
            print(f"File path attempted: {self.data_path.absolute()}")
            if 'df' in locals():
                print(f"Columns found: {list(df.columns)}")
            return False

    def _read_excel_with_fallback(self):
        try:
            return pd.read_excel(
                self.data_path,
                dtype={'HSNCode': str, 'Description': str},
                engine='openpyxl'
            )
        except Exception as e:
            if self.verbose:
                print(f"Primary read failed ({e}), trying fallback methods...")
            try:
                return pd.read_excel(self.data_path, dtype={'HSNCode': str})
            except:
                xls = pd.ExcelFile(self.data_path)
                return pd.read_excel(xls, sheet_name=xls.sheet_names[0], dtype={'HSNCode': str})

    def _build_trie(self):
        if not self.hsn_data:
            raise ValueError("No HSN data available to build trie")

        self.trie = {}
        seen_codes = set()

        for code in self.hsn_data.keys():
            if not isinstance(code, str) or not code.isdigit():
                if self.verbose:
                    print(f"Warning: Invalid HSN code format - {code}")
                continue

            if code in seen_codes:
                if self.verbose:
                    print(f"Warning: Duplicate HSN code found - {code}")
                continue
            seen_codes.add(code)

            node = self.trie
            for digit in code:
                node = node.setdefault(digit, {})
            node['*'] = True

        if self.verbose:
            print(f"Built trie with {len(seen_codes)} unique codes")

    def get_description(self, hsn_code):
        if not self.hsn_data:
            raise ValueError("HSN data not loaded")

        hsn_code = str(hsn_code).replace(' ', '').strip()
        return self.hsn_data.get(hsn_code)

    def validate_hierarchy(self, hsn_code):
        if not self.trie:
            return False, []

        hsn_code = str(hsn_code).replace(' ', '').strip()
        node = self.trie
        hierarchy_valid = True
        parent_codes = []
        validation_path = []

        for i, digit in enumerate(hsn_code):
            if digit not in node:
                hierarchy_valid = False
                validation_path.append(f"Missing digit '{digit}' at position {i+1}")
                break

            node = node[digit]
            parent_code = hsn_code[:i+1]

            if parent_code in self.hsn_data:
                parent_codes.append({
                    'code': parent_code,
                    'description': self.hsn_data[parent_code]
                })
            else:
                validation_path.append(f"Parent code '{parent_code}' not in master data")

        return hierarchy_valid, parent_codes, validation_path

    def get_all_codes(self):
        return list(self.hsn_data.keys()) if self.hsn_data else []
