"""
To use the Kaggle API, sign up for a Kaggle account at https://www.kaggle.com. 
Go to the 'Account' tab of user profile ( https://www.kaggle.com/<username>/account ) 
and select 'Create API Token'. 
This will trigger the download of kaggle. json, a file containing API credentials.

"""
import subprocess
import os
import json

# Function to decrypt data
def decrypt_data(encrypted_data, key, iterations):
    """
    Decrypts the given encrypted data using AES-256-CBC with the specified key and iterations.
    
    Args:
        encrypted_data (str): The encrypted data to be decrypted.
        key (str): The key used for decryption.
        iterations (int): The number of iterations for the key derivation function.

    Returns:
        str: The decrypted data.
    """
    command = f'echo "{encrypted_data}" | openssl enc -aes-256-cbc -pbkdf2 -iter {iterations} -d -a -k "{key}"'
    print(f"Decrypting data: {encrypted_data}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Decryption failed: {result.stderr}")
    decrypted_data = result.stdout.strip()
    print(f"Decrypted data: {decrypted_data}")
    return decrypted_data

# Function to encrypt data
def encrypt_data(data, key, iterations):
    """
    Encrypts the given data using AES-256-CBC with the specified key and iterations.
    
    Args:
        data (str): The data to be encrypted.
        key (str): The key used for encryption.
        iterations (int): The number of iterations for the key derivation function.

    Returns:
        str: The encrypted data.
    """
    command = f'echo "{data}" | openssl enc -aes-256-cbc -pbkdf2 -iter {iterations} -a -k "{key}" | tr -d "\n"'
    print(f"Encrypting data: {data}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Encryption failed: {result.stderr}")
    encrypted_data = result.stdout.strip()
    print(f"Encrypted data: {encrypted_data}")
    return encrypted_data

# Paths for the files
encrypted_file_path = "./sample_data/kaggle.json.enc"
decrypted_file_path = "./sample_data/kaggle.json"

# Example usage
if __name__ == "__main__":
    # Ensure the sample_data directory exists
    os.makedirs("./sample_data", exist_ok=True)

    # Sample data to encrypt and decrypt
    sample_data = '{"username":"*****","key":"*****"}'
    encryption_key = "*****"
    iterations = 100

    # Encrypt the sample data and write to a file
    encrypted = encrypt_data(sample_data, encryption_key, iterations)
    with open(encrypted_file_path, "w") as encrypted_file:
        encrypted_file.write(encrypted)
    print(f"Encrypted data written to: {encrypted_file_path}")

    # Read the encrypted data from the file and decrypt it
    with open(encrypted_file_path, "r") as encrypted_file:
        encrypted_data_from_file = encrypted_file.read()

    decrypted = decrypt_data(encrypted_data_from_file, encryption_key, iterations)
    with open(decrypted_file_path, "w") as decrypted_file:
        decrypted_file.write(decrypted)
    print(f"Decrypted data written to: {decrypted_file_path}")

"""
Encrypting data: {"username":"*****","key":"*****"}
Encrypted data: U2FsdGVkX19xADSwuQRnlh8FN7Hqt0vAlpFOD5/Pn3wx5S4endZ2lI03fdaZdLeG
Encrypted data written to: ./sample_data/kaggle.json.enc
Decrypting data: U2FsdGVkX19xADSwuQRnlh8FN7Hqt0vAlpFOD5/Pn3wx5S4endZ2lI03fdaZdLeG
Decrypted data: {username:*****,key:*****}
Decrypted data written to: ./sample_data/kaggle.json
"""

# Upload kaggle.json API token, and download / unzip California Housing csv

#!mkdir ./sample_data/.kaggle
!cp ./sample_data/kaggle.json ./sample_data/.kaggle/
!chmod 600 ./sample_data/.kaggle/kaggle.json
!kaggle datasets download -d camnugent/california-housing-prices
!unzip ./sample_data/california-housing-prices.zip
!curl -o ./sample_data/heart_statlog_cleveland_hungary_final.csv https://raw.githubusercontent.com/erdenahmet11/Heart-Disease-Prediction/main/heart_statlog_cleveland_hungary_final.csv

"""
Dataset URL: https://www.kaggle.com/datasets/camnugent/california-housing-prices
License(s): CC0-1.0
Downloading california-housing-prices.zip to /content
  0% 0.00/400k [00:00<?, ?B/s]
100% 400k/400k [00:00<00:00, 109MB/s]
unzip:  cannot find or open ./sample_data/california-housing-prices.zip, ./sample_data/california-housing-prices.zip.zip or ./sample_data/california-housing-prices.zip.ZIP.
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 39689  100 39689    0     0   308k      0 --:--:-- --:--:-- --:--:--  310k
"""

import json
import os

# Import the conversion function
def convert_json_format(input_str):
    """
    Convert between two JSON representation formats:
    1. '{username:*****,key:*****}'
    2. '{"username":"*****","key":"*****"}'

    Args:
        input_str (str): Input string in either format

    Returns:
        str: Converted JSON string
    """
    import re
    import json

    # Check if input is the non-standard format
    if re.match(r'^{[^"]+:[^"]+,[^"]+:[^"]+}$', input_str):
        # Convert from {username:value,key:value} to standard JSON
        # Remove { and }
        cleaned = input_str.strip('{}')
        # Split into key-value pairs
        pairs = cleaned.split(',')
        # Create a dictionary
        formatted_dict = {}
        for pair in pairs:
            key, value = pair.split(':')
            formatted_dict[key.strip()] = value.strip()
        
        # Convert to JSON string with quotes
        return json.dumps(formatted_dict)
    
    # If input is already standard JSON, return as-is
    try:
        json.loads(input_str)
        return input_str
    except json.JSONDecodeError:
        # If input is not valid JSON and not the non-standard format
        raise ValueError("Invalid input format")

# Define the file path
file_path = './sample_data/kaggle.json'

# Ensure the sample_data directory exists
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# Read the content of the file
with open(file_path, 'r') as file:
    content = file.read().strip()

# Convert the content to standard JSON format
try:
    # Use the conversion function to standardize the JSON
    json_content = convert_json_format(content)
    
    # Parse the content to ensure it's valid JSON
    content_dict = json.loads(json_content)
    
    # Write the updated content back to the file with pretty formatting
    with open(file_path, 'w') as file:
        file.write(json.dumps(content_dict, indent=4))

    print(f"Updated content written to {file_path}")
except (json.JSONDecodeError, ValueError) as e:
    print(f"Error processing JSON: {e}")

# Updated content written to ./sample_data/kaggle.json

import subprocess
import os
import shutil
import json

# Ensure the ~/.kaggle directory exists
os.makedirs(os.path.expanduser('~/.kaggle'), exist_ok=True)

# Path to the kaggle.json file in the current directory
source_file = './sample_data/kaggle.json'
destination_file = os.path.expanduser('~/.kaggle/kaggle.json')

# Check if kaggle.json exists in the source directory
if not os.path.exists(source_file):
    raise FileNotFoundError(f"The file {source_file} does not exist. Please make sure it is in the correct directory.")

# Load and validate kaggle.json content
with open(source_file, 'r') as f:
    kaggle_config = json.load(f)
    if 'username' not in kaggle_config or 'key' not in kaggle_config:
        raise ValueError("The kaggle.json file is missing 'username' or 'key'.")

# Copy the kaggle.json file to the ~/.kaggle directory
shutil.copy(source_file, destination_file)

# Set the permissions to read/write only for the user
os.chmod(destination_file, 0o600)

# Function to list available datasets
def list_datasets():
    command = "kaggle datasets list"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Failed to list datasets: {result.stderr}")
    print(result.stdout)

# Function to download a specific dataset
def download_dataset(dataset):
    command = f"kaggle datasets download -d {dataset}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Failed to download dataset {dataset}: {result.stderr}")
    print(f"Dataset {dataset} downloaded successfully.")

import subprocess
import random

def list_datasets_and_select_1_randomly():
    command = "kaggle datasets list"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Failed to list datasets: {result.stderr}")
    
    # Get dataset names from the command output
    datasets = []
    for line in result.stdout.splitlines():
        # Each line starts with the dataset name
        parts = line.split()
        if len(parts) > 0:
            datasets.append(parts[0])

    if not datasets:
        raise Exception("No datasets found.")
    
    # Select a random dataset
    dataset_name = random.choice(datasets)
    return dataset_name

# Example usage
if __name__ == "__main__":
    # List available datasets
    list_datasets()

    # Download a specific dataset
    dataset_name = "camnugent/california-housing-prices" # "rajugc/kaggle-dataset"
    download_dataset(dataset_name)

    dataset_name = list_datasets_and_select_1_randomly()
    print(f"Randomly selected dataset: {dataset_name}")
   

"""
ref                                                         title                                          size  lastUpdated          downloadCount  voteCount  usabilityRating  
----------------------------------------------------------  --------------------------------------------  -----  -------------------  -------------  ---------  ---------------  
bhadramohit/customer-shopping-latest-trends-dataset         Customer Shopping (Latest Trends) Dataset      76KB  2024-11-23 15:26:12           6192        116  1.0              
mujtabamatin/air-quality-and-pollution-assessment           Air Quality and Pollution Assessment           84KB  2024-12-04 15:29:51           1483         38  1.0              
anirudhchauhan/retail-store-inventory-forecasting-dataset   Retail Store Inventory Forecasting Dataset      2MB  2024-11-24 20:09:48           1262         23  1.0              
steve1215rogg/student-lifestyle-dataset                     student lifestyle dataset                      22KB  2024-11-11 19:11:28           8446        133  1.0              
ikynahidwin/depression-student-dataset                      Depression Student Dataset                      4KB  2024-11-20 06:42:01           4579         79  1.0              
hopesb/student-depression-dataset                           Student Depression Dataset.                   454KB  2024-11-22 17:56:03           3300         53  0.9411765        
junnn0126/university-students-mental-health                 University Students' Mental Health             11KB  2024-11-25 15:07:26           1333         24  0.8235294        
steve1215rogg/e-commerce-dataset                            E-Commerce Dataset                             90KB  2024-11-22 22:10:02           2177         39  1.0              
heidarmirhajisadati/regional-cost-of-living-analysis        Regional Cost of Living Analysis               13KB  2024-11-30 22:38:52            933         53  1.0              
bhadramohit/tata-ipl-auction-list2025-dataset               TATA IPL Auction List(2025) Dataset            16KB  2024-11-24 05:16:43            664         22  1.0              
mohitkumar282/used-car-dataset                              Used Car Dataset                              230KB  2024-11-24 09:14:58           2833         38  1.0              
zeeshier/student-admission-records                          Student Admission Records                       2KB  2024-11-08 17:26:54           2819         35  0.88235295       
datadrivenx/video-game-stocks-financial-market-data         Video Game Stocks: Financial Market Data       75KB  2024-11-14 18:51:38           1009         25  1.0              
taweilo/loan-approval-classification-data                   Loan Approval Classification Dataset          751KB  2024-10-29 04:07:34           8053         78  1.0              
valakhorasani/gym-members-exercise-dataset                  Gym Members Exercise Dataset                   22KB  2024-10-06 11:27:38          25516        354  1.0              
marmarplz/student-academic-grades-and-programs              Student Academic Marks and Programs             2MB  2024-11-18 18:31:40           1891         34  1.0              
fernandogarciah24/top-1000-imdb-dataset                     Top 1000 IMDB dataset                         236KB  2024-11-10 20:32:13            601         10  0.9411765        
ironwolf437/who-covid-19-cases-dataset                      WHO COVID-19 cases - dataset                  583KB  2024-11-19 20:22:38           1130         35  1.0              
computingvictor/transactions-fraud-datasets                 💳 Financial Transactions Dataset: Analytics   348MB  2024-10-31 21:29:56           6789         97  1.0              
valakhorasani/bank-transaction-dataset-for-fraud-detection  Bank Transaction Dataset for Fraud Detection  102KB  2024-11-04 09:23:49           4528         82  1.0              

Dataset camnugent/california-housing-prices downloaded successfully.
Randomly selected dataset: zeeshier/student-admission-records

"""
