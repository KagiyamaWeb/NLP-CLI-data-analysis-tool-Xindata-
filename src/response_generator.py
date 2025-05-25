from typing import Dict, Any


class ResponseGenerator:
    @staticmethod
    def generate(response_data: Dict[str, Any], original_query: str) -> str:
        numerical = response_data.get('numerical_result', 'No data')
        explanation = response_data.get('nlp_explanation', 'No explanation')
        
        return f"""Ответ на запрос "{original_query}":
            {'-'*40}    
            Данные:
            {numerical}
            
            Анализ:
            {explanation}
            {'-'*40}"""
