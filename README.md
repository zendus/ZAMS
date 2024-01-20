# Face Recognition Attendance Management System

## Overview

Welcome to the Face Recognition Attendance Management System! This web-based application utilizes OpenCV for face detection, scikit-learn's Support Vector Machine (SVM) model for face embeddings training, and SQL for storing captured student face details. The system can efficiently detect and label faces from both images and video streams, making it a powerful tool for managing attendance in various settings.

## Features

- **Face Detection:** The system employs OpenCV to detect faces in images and video streams. This ensures accurate identification and labeling of individuals.

- **Embedding with SVM Model:** Face embeddings are generated using scikit-learn's SVM model. This allows for efficient representation of facial features, enabling accurate recognition and matching.

- **SQL Database Integration:** Student face details are stored in an SQL database, providing a secure and organized way to manage attendance records.

- **Web-Based Application:** The system is accessible through a user-friendly web interface, making it easy for administrators and users to interact with the attendance management features.

## Requirements

- Python 3.x
- OpenCV
- scikit-learn
- Flask
- SQL Database (e.g., MySQL, SQLite)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/zendus/ZAMS.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up the SQL database:

    - Create a new database and configure the connection details in `config.py`

4. Run the application:

    ```bash
    python webstreaming.py
    ```

## Usage

1. Open the web application in your browser.

2. Register or login by filling the form provided

3. Use the system to capture attendance from images or live video streams.

4. View and export attendance records as a spreadsheet through the web interface.

## Configuration

- Update the `config.py` file with your database connection details, SVM model parameters, and other configuration settings.

## Contributions

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- PyImageSearch

- OpenCV 


Thank you for using the Face Recognition Attendance Management System! If you encounter any issues or have questions, please reach out to us. Happy attendance tracking!