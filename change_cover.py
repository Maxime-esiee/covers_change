try:
    import mutagen
except ImportError:
    print("'mutagen' library is not installed. Please download it using 'pip install mutagen'.")
    sys.exit(1)  # Exit the program if mutagen is not installed
from mutagen.flac import FLAC, Picture
from mutagen.id3 import PictureType
import os
import sys
import io
import logging

# Configure logging
logging.basicConfig(filename='change_cover.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def change_cover_tag(flac_file_path, modified_count, modified_directories):
    """
    Change the picture tag type from 'other' to 'Cover' in a FLAC file.
    """
    try:
        # Ensure the path is properly encoded
        if not isinstance(flac_file_path, str):
            flac_file_path = flac_file_path.decode('utf-8')
            
        audio = FLAC(flac_file_path)
        
        # Get existing pictures
        pictures = audio.pictures
        
        if not pictures:
            #print(f"No pictures found in {flac_file_path!r}")
            logging.info(f"No pictures found in {flac_file_path!r}")  # Log the event
            return modified_count
        
        existing_cover = any(pic.type == 3 for pic in pictures)  # Check for existing cover
        if existing_cover:
            #print(f"Cover image already exists in {flac_file_path!r}, skipping modification.")
            logging.info(f"Cover image already exists in {flac_file_path!r}, skipping modification.")  # Log the event
            return modified_count
        
        # Find pictures with type 'other' (type 0) and change them to 'Cover' (type 3)
        modified = False
        for pic in pictures:
            if pic.type == 0:  # 'other' type
                pic.type = 3   # 'Cover (front)' type
                modified = True
        
        if modified:
            # Clear existing pictures and add modified ones
            audio.clear_pictures()
            for pic in pictures:
                audio.add_picture(pic)
            print(f"\nProcessing: {flac_file_path!r}")
            # Save the changes
            audio.save()
            print(f"Successfully updated cover tag in {flac_file_path!r}")
            logging.info(f"Updated cover tag in {flac_file_path!r}")  # Log the change
            modified_directories.add(os.path.dirname(flac_file_path))  # Add directory to the set
            return modified_count + 1
        else:
            #print(f"No 'other' type pictures found in {flac_file_path!r}")
            logging.info(f"No 'other' type pictures found in {flac_file_path!r}")  # Log the event
            
    except UnicodeEncodeError as ue:
        #print(f"Unicode encoding error with file: {flac_file_path!r}")
        #print(f"Error details: {str(ue)}")
        logging.error(f"Unicode encoding error with file: {flac_file_path!r} - {str(ue)}")  # Log the error
    except UnicodeDecodeError as ud:
        #print(f"Unicode decoding error with file: {flac_file_path!r}")
        #print(f"Error details: {str(ud)}")
        logging.error(f"Unicode decoding error with file: {flac_file_path!r} - {str(ud)}")  # Log the error
    except Exception as e:
        #print(f"Error processing {flac_file_path!r}: {str(e)}")
        logging.error(f"Error processing {flac_file_path!r}: {str(e)}")  # Log the error

def process_directory_recursive():
    """
    Process all FLAC files in the current directory and all its subdirectories.
    """
    try:
        modified_count = 0  # Initialize counter
        modified_directories = set()  # Track modified directories
        current_dir = os.getcwd()
        print(f"Processing FLAC files in: {current_dir!r} and all subdirectories")
        logging.info(f"Processing FLAC files in: {current_dir!r} and all subdirectories")  # Log the event
        
        flac_files = []
        # Walk through all subdirectories
        for root, _, files in os.walk(current_dir):
            for file in files:
                if file.lower().endswith('.flac'):
                    try:
                        flac_path = os.path.join(root, file)
                        flac_files.append(flac_path)
                    except UnicodeError as ue:
                        #print(f"Unicode error with file path: {file!r}")
                        #print(f"Error details: {str(ue)}")
                        logging.error(f"Unicode error with file path: {file!r} - {str(ue)}")  # Log the error
        
        if not flac_files:
            print("No FLAC files found")
            logging.info("No FLAC files found")  # Log the event
            return
        
        print(f"Found {len(flac_files)} FLAC files")
        logging.info(f"Found {len(flac_files)} FLAC files")  # Log the event
        
        # Process each FLAC file
        for flac_path in flac_files:
            try:
                # Get relative path for cleaner output
                rel_path = os.path.relpath(flac_path, current_dir)
                #print(f"\nProcessing: {rel_path!r}")
                logging.info(f"Processing: {rel_path!r}")  # Log the event
                modified_count = change_cover_tag(flac_path, modified_count, modified_directories)
            except UnicodeError as ue:
                #print(f"Unicode error with path: {flac_path!r}")
                #print(f"Error details: {str(ue)}")
                logging.error(f"Unicode error with path: {flac_path!r} - {str(ue)}")  # Log the error
                
        print(f"Total modified files: {modified_count}")
        
        if modified_count > 0:
            print("Directories with modified files:")
            for directory in modified_directories:
                print(directory)
        
    except Exception as e:
        print(f"Error during directory processing: {str(e)}")
        logging.error(f"Error during directory processing: {str(e)}")  # Log the error

if __name__ == "__main__":
    # Set UTF-8 as the default encoding for stdout
    if sys.stdout.encoding != 'utf-8':
        try:
            if isinstance(sys.stdout, io.TextIOWrapper):
                sys.stdout.reconfigure(encoding='utf-8')
            else:
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        except Exception as e:
            print(f"Error setting encoding: {str(e)}")
            logging.error(f"Error setting encoding: {str(e)}")  # Log the error

    process_directory_recursive()