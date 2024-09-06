import pandas as pd
import logging
import os

def merge_data(df):
    """Merge all relevant data and logs into one consistent dataset."""
    male_students = df[df['gender'] == 'male']
    female_students = df[df['gender'] == 'female']

    # Save male and female students into separate files
    male_students.to_csv('output/male_students.csv', index=False)
    female_students.to_csv('output/female_students.csv', index=False)

    # Save the entire dataset as CSV and TSV
    df.to_csv('output/students.csv', index=False)
    df.to_csv('output/students.tsv', sep='\t', index=False)

    logging.info(f"Number of male students: {len(male_students)}")
    logging.info(f"Number of female students: {len(female_students)}")

def shuffle_and_save_outputs(df):
    """Shuffle the DataFrame and save outputs in JSON, JSONL, TSV, and CSV formats."""
    # Shuffle the DataFrame
    df_shuffled = df.sample(frac=1).reset_index(drop=True)

    # Save as JSON
    df_shuffled.to_json('output/shuffled.json', orient='records')

    # Save as JSONL
    with open('output/shuffled.jsonl', 'w') as f:
        for record in df_shuffled.to_dict(orient='records'):
            f.write(f"{record}\n")

    # Save as TSV
    df_shuffled.to_csv('output/shuffled.tsv', sep='\t', index=False)

    logging.info("Data shuffled and saved as JSON, JSONL, and TSV successfully.")
