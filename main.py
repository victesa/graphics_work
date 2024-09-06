import pandas as pd
import logging
from functions import generate_email

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

        # Save the updated data to a new file
        df.to_csv('output/students_with_emails.csv', index=False)
        logging.info("Updated dataset saved successfully.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
