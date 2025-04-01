
import os
import pandas as pd
from pandas.core.interchange import column

# Load the extracted details from the CSV file
file_path = 'extracted_details.csv'

# Check if the file exists
if not os.path.isfile(file_path):
    # If the file does not exist, create it with the appropriate headers
    pd.DataFrame(columns=['Filename', 'Name', 'Contact Information', 'Education', 'Work Experience', 'Skills']).to_csv(file_path, index=False)
data = pd.read_csv(file_path)

# Define personality traits associations with skills
def read_traits_from_file(traits_file):
    traits_mapping = {}

    with open(traits_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            # Skip empty lines or lines without a ':'
            if not line or ':' not in line:
                print(f"Skipping malformed line: {repr(line)}")  # Debugging
                continue

            try:
                trait, skills = line.split(':', 1)  # Ensures only first ':' is used for splitting
                traits_mapping[trait.strip()] = skills.strip()
            except ValueError:
                print(f"Error processing line: {repr(line)}")  # Debugging
                continue  # Skip malformed lines

    return traits_mapping


# Usage:
traits_file = 'traits.txt'  # Path to your traits file
traits_mapping = read_traits_from_file(traits_file)
#print(traits_mapping)  # This will display the traits mapping dictionary


def assign_personality_traits(row):
    traits_scores = {trait: 0 for trait in traits_mapping}

    if not pd.isna(row['Skills']): 
        user_skills = set(row['Skills'].split(', ')) 

        for trait, skills in traits_mapping.items():
            trait_skills = set(skills.split(', '))  
            traits_scores[trait] = len(user_skills.intersection(trait_skills))

    return pd.Series(traits_scores)

# Apply the function to the dataframe to assign personality traits
personality_traits = data.apply(assign_personality_traits, axis=1)

# Concatenate the original data with the assigned personality traits
data_with_traits = pd.concat([data, personality_traits], axis=1)

# Save the updated data to a new CSV file
output_file_path = 'extracted_detailsWith_traits.csv'
data_with_traits.to_csv(output_file_path, index=False)

