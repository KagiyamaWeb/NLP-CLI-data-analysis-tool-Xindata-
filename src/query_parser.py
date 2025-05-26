import google.generativeai as genai
import os
import pandas as pd


class QueryParser:
    def __init__(self, processed_data):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.df = processed_data
        
    def parse_query(self, question: str) -> str:
        prompt = f"""Given this pandas DataFrame schema:
            {self.df.dtypes.to_string()}
        Generate TWO code blocks to answer: {question}

        Requirements:
        1. Use EXISTING DataFrame 'df' (DO NOT CREATE NEW DATA EXCEPT FOR 'numerical_result' AND 'nlp_explanation')
        2. First code block (data):
           - Use pandas to calculate numerical results
           - Store in 'numerical_result' as DataFrame/Series
           - Generate natural language explanation in Russian
           - Store in 'nlp_explanation' as string
           - NO FUNCTION DEFINITIONS
        """
        
        response = self.model.generate_content(prompt)
        code = self._extract_code(response.text)

        return self._execute_safe(code)
    
    def _extract_code(self, text: str) -> str:
        raw_code = text.split('```python')[1].split('```')[0].strip()
        # Remove leading whitespace from each line
        return '\n'.join([line.lstrip() for line in raw_code.split('\n')])
    
    def _execute_safe(self, code: str):
        # Forbidden patterns that break execution
        forbidden_patterns = ['def ', 'class ', 'lambda ', 'import os', 'import sys', 'from ']
        
        # Check for forbidden imports
        for pattern in forbidden_patterns:
            if pattern in code:
                return {
                    'numerical_result': 'Invalid code',
                    'nlp_explanation': f'Forbidden pattern detected: {pattern}'
                }
        
        # Validate allowed imports
        if 'import pandas' not in code:
            code = 'import pandas as pd\n' + code
        
        allowed_globals = {
            'pd': pd,
            'df': self.df,
        }
        
        try:
            # Execute in restricted environment
            exec(code, allowed_globals)
            return {
                'numerical_result': allowed_globals.get('numerical_result', 'No data'),
                'nlp_explanation': allowed_globals.get('nlp_explanation', 'No explanation')
            }
        except Exception as e:
            print(f'\n=== Execution Error ===\n{e}')
            return {
                'numerical_result': 'Error',
                'nlp_explanation': f'Execution error: {str(e)}'
            }
