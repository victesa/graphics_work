import pandas as pd
import logging
from functions import generate_email,find_names_with_special_characters

# Set up logging
logging.basicConfig(filename='logs/computations.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def main():
    try:
        # Read the Excel file
        df = pd.read_excel('data/students.xlsx')
        logging.info("Excel file loaded successfully.")

        # Standardize column names
        df.rename(columns={'Student Name': 'name', 'Gender': 'gender'}, inplace=True)

        # Generate emails
        df['email'] = df['name'].apply(generate_email)
        logging.info("Email addresses generated successfully.")

        # Clean and map gender data
        df['gender'] = df['gender'].str.strip().str.upper()  # Strip spaces and convert to uppercase for consistency
        df['gender'] = df['gender'].map({'M': 'male', 'F': 'female'})  # Map 'M' to 'male' and 'F' to 'female'

        # Generate emails based on the names
        df['email'] = df['name'].apply(generate_email)
        logging.info("Email addresses generated successfully.")

        # Log names with special characters
        special_names = find_names_with_special_characters(df['name'].tolist())
        logging.info(f"Students with special characters in their names: {special_names}")

        # Save the updated data to a new file
        df.to_csv('output/students_with_emails.csv', index=False)
        logging.info("Updated dataset saved successfully.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
