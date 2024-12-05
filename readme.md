# Credentials Encryption and Kaggle Dataset Integration

Provides an example of how to securely encrypt and decrypt data using AES-256-CBC encryption, and how to work with Kaggle datasets using API keys.

## Features

- **AES-256-CBC Encryption/Decryption**: Encrypt and decrypt JSON data securely.
   - The encrypted data is saved to ./sample_data/kaggle.json.enc, and the decrypted data is saved to ./sample_data/kaggle.json.

- **Kaggle Dataset Handling**: Upload API keys, list available datasets, and download selected datasets.
   - The script sets up the Kaggle API key for use.
   - Lists available datasets on Kaggle.
   - Downloads the dataset or selects a random dataset.

## Requirements

- Python 3.x
- `openssl` command-line tool
- Kaggle account with API key

## Setup

1. **Kaggle API Key**: 
   - Place your `kaggle.json` API key in the `./sample_data/` directory.

2. **Encryption Setup**:
   - Modify the `encryption_key` and `iterations` parameters as needed.


