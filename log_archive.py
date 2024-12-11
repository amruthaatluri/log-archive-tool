import argparse
import os
import tarfile
from datetime import datetime
import logging

# Argument parser setup
def parse_arguments():
    parser = argparse.ArgumentParser(description="Archive logs from a specified directory.")
    parser.add_argument('log_directory', type=str, help="Directory containing the logs to archive")
    parser.add_argument('archive_directory', type=str, help="Directory to store the archived logs")
    return parser.parse_args()

# Check if directories exist and create archive directory if it doesn't exist
def check_directories(log_directory, archive_directory):
    if not os.path.isdir(log_directory):
        print(f"Error: The directory '{log_directory}' does not exist.")
        return False
    
    if not os.path.exists(archive_directory):
        os.makedirs(archive_directory)  # Create the archive directory if it doesn't exist

    return True

# Generate a timestamp for the archive filename
def generate_timestamp():
    return datetime.now().strftime('%Y%m%d_%H%M%S')  # Format: 20240816_100648

# Create a .tar.gz archive of the logs
def create_archive(log_directory, archive_directory, timestamp):
    archive_name = f"logs_archive_{timestamp}.tar.gz"
    archive_path = os.path.join(archive_directory, archive_name)

    # Create a tar.gz file and add all files from the log directory
    with tarfile.open(archive_path, "w:gz") as tar:
        for root, dirs, files in os.walk(log_directory):
            for file in files:
                file_path = os.path.join(root, file)
                tar.add(file_path, arcname=os.path.relpath(file_path, log_directory))

    return archive_path

# Log the date and time of the archive creation
def log_archive_creation(archive_path):
    logging.info(f"Archived logs to {archive_path}")

# Configure logging
logging.basicConfig(filename='log_archive.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

def main():
    try:
        # Get arguments from the command line
        args = parse_arguments()

        # Check if directories exist
        if not check_directories(args.log_directory, args.archive_directory):
            return
        
        # Generate timestamp for the archive filename
        timestamp = generate_timestamp()

        # Create the archive
        archive_path = create_archive(args.log_directory, args.archive_directory, timestamp)

        # Log the success of the operation
        log_archive_creation(archive_path)

        print(f"Log archive created at: {archive_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"Error during archiving: {e}")

if __name__ == "__main__":
    main()


