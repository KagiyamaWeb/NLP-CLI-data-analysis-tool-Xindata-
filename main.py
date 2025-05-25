import argparse

from src.data_processor import DataProcessor
from src.query_parser import QueryParser
from src.response_generator import ResponseGenerator
import pandas as pd


def main():
    processor = DataProcessor("data/freelancer_earnings_bd.csv")
    cleaned_data = processor.clean_data()
    
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="Natural language query about freelancer data")
    args = parser.parse_args()
    
    result = QueryParser(pd.DataFrame(cleaned_data)).parse_query(args.query)
    print(ResponseGenerator.generate(result, args.query))

if __name__ == "__main__":
    main()
