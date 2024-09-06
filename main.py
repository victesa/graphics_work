import pandas as pd
import logging
import os
from functions import generate_email, find_names_with_special_characters
from similarity import compute_similarity_matrix, find_similar_names, save_results_to_json
from output_handler import merge_data, shuffle_and_save_outputs

# Set up logging
logging.basicConfig(filename='logs/computations.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def main():
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists('output'):
            os.makedirs('output')

        # Read the Excel file
        df = pd.read_excel('data/students.xlsx')
        logging.info("Excel file loaded successfully.")

        # Standardize column names
        df.rename(columns={'Student Name': 'name', 'Gender': 'gender'}, inplace=True)

        # Generate emails
        df['email'] = df['name'].apply(generate_email)
        logging.info("Email addresses generated successfully.")

        # Clean and map gender data
        df['gender'] = df['gender'].str.strip().str.upper()
        df['gender'] = df['gender'].map({'M': 'male', 'F': 'female'})

        # Log gender counts
        males = df[df['gender'] == 'male']
        females = df[df['gender'] == 'female']
        logging.info(f"Number of male students: {len(males)}")
        logging.info(f"Number of female students: {len(females)}")

        # Log names with special characters
        special_names = find_names_with_special_characters(df['name'].tolist())
        logging.info(f"Students with special characters in their names: {special_names}")

        # Compute similarity matrix and find similar names
        male_names = males['name'].tolist()
        female_names = females['name'].tolist()

        male_similarity_matrix = compute_similarity_matrix(male_names)
        female_similarity_matrix = compute_similarity_matrix(female_names)

        male_similarities = find_similar_names(male_similarity_matrix, male_names)
        female_similarities = find_similar_names(female_similarity_matrix, female_names)

        # Save results to JSON
        save_results_to_json({
            'male_similarities': male_similarities,
            'female_similarities': female_similarities
        }, 'output/similarity_results.json')

        # Merge, shuffle, and save data in various formats
        merge_data(df)
        shuffle_and_save_outputs(df)

        logging.info("All operations completed successfully.")



    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
