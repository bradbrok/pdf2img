# PDF and Text to Image Converter

A Flask web application that converts PDF files and text files to images. PDFs are converted page by page, and text files are rendered as images.

## Prerequisites

Before running this application, you need to install:

1. Python 3.7 or higher
2. Poppler (required for PDF conversion)

### Installing Poppler

- **macOS**:
  ```bash
  brew install poppler
  ```

- **Windows**:
  1. Download Poppler from: http://blog.alivate.com.au/poppler-windows/
  2. Extract the downloaded file
  3. Add the `bin` folder to your system PATH

- **Linux**:
  ```bash
  sudo apt-get install poppler-utils
  ```

## Setup Instructions

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Project Structure

```
.
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── static/            # Static files (CSS, JS, etc.)
│   └── css/
│       └── style.css
├── templates/         # HTML templates
│   └── index.html
└── uploads/          # Temporary folder for file uploads
```

## Usage

1. Select one or multiple PDF or text files using the file upload form
2. Adjust DPI settings if needed (for PDF conversion)
3. Click "Convert" to process the files
4. A zip file containing the converted images will be downloaded automatically

## Notes

- The application has a file size limit of 100MB
- Uploaded files are temporarily stored and automatically deleted after processing
- PDF files are converted to JPG images, one image per page
- Text files are rendered as images with configurable font size
