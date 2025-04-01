
import os
import PyPDF2
from fuzzywuzzy import fuzz
import spacy
import re
from docx import Document
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk



nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = ''
    for para in doc.paragraphs:
        text += para.text + '\n'
    return text


import pdfplumber

def extract_text_from_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
    return text.strip()



def preprocess_text(text):
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Tokenization
    tokens = word_tokenize(text)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    # Join tokens back into text
    preprocessed_text = ' '.join(lemmatized_tokens)
    return preprocessed_text


def extract_text_based_on_file(file_path):
    if file_path.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    elif file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    else:
        text = "Unsupported file format for file: {}".format(file_path)

    # Perform text preprocessing
    preprocessed_text = preprocess_text(text)
    return preprocessed_text


def extract_features_from_resumes(folder_path):
    extracted_texts = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            text = extract_text_based_on_file(file_path)
            extracted_texts.append(text)
    return extracted_texts


def extract_tfidf_features(texts):
    # Initialize the TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)  # Adjust max_features as needed

    # Fit and transform the text
    tfidf_features = tfidf_vectorizer.fit_transform(texts)
    return tfidf_features, tfidf_vectorizer




def extract_name(filename, row_number):
    # Extract name from the PDF filename
    name_pattern = r'(.+?)\.pdf'  # Pattern to match the name before '.pdf'

    # Search for the name pattern in the filename
    match = re.search(name_pattern, filename)

    if match:
        extracted_name = match.group(1)  # Extract the name without the '.pdf'
    else:
        extracted_name = f"resume_{row_number}"  # Return row_number if name not found

    print(extracted_name)
    return extracted_name






import re
#updated
def extract_contact_info(text):
    # Email extraction pattern (strict validation)
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

    # Phone number pattern (Supports international & Indian formats)
    phone_pattern = r'\b(?:\+?\d{1,3}[-.\s]?)?(?:\d{10}|\d{3}[-.\s]??\d{3}[-.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-.\s]??\d{4})\b'

    # Find unique email addresses
    emails = set(re.findall(email_pattern, text))

    # Find unique phone numbers
    phones = set(re.findall(phone_pattern, text))

    # Convert lists into formatted strings
    email_str = ", ".join(emails) if emails else "No emails found."
    phone_str = ", ".join(phones) if phones else "No phone numbers found."

    # Return the result as a formatted string
    return f"Emails: {email_str}\nPhone Numbers: {phone_str}"

#updated
def extract_education(text, education_file='education.txt'):
    # Read education keywords from a file
    with open(education_file, 'r', encoding='utf-8') as file:
        education_keywords = file.read().splitlines()
    
    # Convert text to lowercase for case-insensitive matching
    lowercase_text = text.lower()

    # Initialize a set to store unique education details
    education_details = set()

    # Regex pattern to match words with possible variations (e.g., B.Tech, BTech, Bachelor of Technology)
    pattern = r'\b(?:' + '|'.join(re.escape(keyword) for keyword in education_keywords) + r')\b'

    # Search for exact keyword matches using regex
    matches = re.findall(pattern, lowercase_text, re.IGNORECASE)
    education_details.update(matches)

    # Print the found education details
    print(education_details)

    return ', '.join(sorted(education_details))  # Return sorted, unique results
#updated
def extract_work_experience(text, work_exp_file='workExp.txt'):
    # Read work experience keywords (job titles) from the file
    with open(work_exp_file, 'r', encoding='utf-8') as file:
        experience_keywords = [line.strip().lower() for line in file.readlines()]

    # Convert text to lowercase for case-insensitive search
    lowercase_text = text.lower()

    # Extract job roles based on exact keyword match (to avoid partial matches)
    job_roles = []
    for keyword in experience_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', lowercase_text):  # Match exact word
            job_roles.append(keyword)

    # Return unique job roles (sorted)
    return ', '.join(sorted(set(job_roles)))  
# Return sorted, unique job rolespython 
def extract_job_roles(text, work_exp_file='workExp.txt'):
    # Read work experience keywords (job titles) from the file
    with open(work_exp_file, 'r', encoding='utf-8') as file:
        experience_keywords = [line.strip().lower() for line in file.readlines()]

    # Convert text to lowercase for case-insensitive search
    lowercase_text = text.lower()

    # Extract job roles based on exact keyword match (to avoid partial matches)
    job_roles = []
    for keyword in experience_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', lowercase_text):  # Match exact word
            job_roles.append(keyword)

    # Return unique job roles (sorted)
    return ', '.join(sorted(set(job_roles)))  # Return sorted, unique job roles

#updated
def extract_skills(text, skills_file='skills.txt'):
    # Read skills from the specified file using UTF-8 encoding
    with open(skills_file, 'r', encoding='utf-8') as file:
        skills_keywords = set(file.read().splitlines())  # Use a set for faster lookups

    # Convert text to lowercase for case-insensitive matching
    lowercase_text = text.lower()

    # Initialize an empty set to store extracted skills
    skills_list = set()

    # Search for exact skill matches using regex word boundaries
    for skill in skills_keywords:
        pattern = rf'\b{re.escape(skill.lower())}\b'  # Ensures exact word matching
        if re.search(pattern, lowercase_text):
            skills_list.add(skill)  # Add skill if found

    # Convert set to a sorted list and join into a string
    skills_info = ', '.join(sorted(skills_list))
    print(skills_info)
    return skills_info





    


   


    




    




def construct_dataset(folder_path):
    dataset = []
    row_number = 1  # Initialize row number
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            text = extract_text_based_on_file(file_path)
            name = extract_name(filename, row_number)

            # Extract relevant information from the text
            name = extract_name(filename, row_number)
            contact_info = extract_contact_info(text)
            education = extract_education(text)
            work_experience = extract_work_experience(text)
            skills = extract_skills(text)
            row_number += 1

            # Create a dictionary representing a row in the dataset
            resume_data = {
                'Filename': filename,
                'Name': name,
                'Contact Information': contact_info,
                'Education': education,
                'Work Experience': work_experience,
                'Skills': skills,
                # Add other fields accordingly
            }

            dataset.append(resume_data)
    print(dataset)
    return dataset


def save_dataset_to_csv(dataset, output_file):
    import csv

    # Define the field names (column headers) for the CSV file
    fieldnames = ['Filename', 'Name', 'Contact Information', 'Education', 'Work Experience', 'Skills']
    # Add other field names here if needed

    # Write the dataset to a CSV file
    with open(output_file, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dataset)



if __name__ == "__main__":
    folder_path = (r"C:\Developer\PycharmProjects\personality-Prediction-System-via-CV-Analysis\uploads")
    #folder_path = (r"C:\Developer\PycharmProjects\python-Test-Projects\data\ENGINEERING")


    if not os.path.exists(folder_path):
        print("Folder path doesn't exist.")
    else:
        # Extract preprocessed text from resumes
        extracted_texts = extract_features_from_resumes(folder_path)
        # Extract and structure data from resumes
        dataset = construct_dataset(folder_path)

        # Extract TF-IDF features
        tfidf_features, tfidf_vectorizer = extract_tfidf_features(extracted_texts)

        # Save the structured dataset to a CSV file
        output_file = 'resume_dataset.csv'
        save_dataset_to_csv(dataset, output_file)
        print(f"Dataset saved to {output_file}")

        # Display TF-IDF features
        feature_names = tfidf_vectorizer.get_feature_names_out()
        print("TF-IDF Features:")
        print(feature_names)
        print("\nTF-IDF Matrix:")
        print(tfidf_features.toarray())