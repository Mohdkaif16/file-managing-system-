import os
import shutil
import hashlib

# Function to calculate the hash of a file
def calculate_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

# Function to rename a file if there's a conflict
def handle_name_conflict(dest_folder, file):
    base_name, ext = os.path.splitext(file)
    counter = 1
    new_name = file
    while os.path.exists(os.path.join(dest_folder, new_name)):
        new_name = f"{base_name}_{counter}{ext}"
        counter += 1
    return new_name

# Function to organize files based on extensions
def organize_files(folder_path):
    extensions = {
        'Image': ['jpg', 'jpeg', 'png', 'gif'],
        'pdfs': ['pdf'],
        'docxs':['docx'],
        'txts': ['txt'],
        'xlsxs': ['xlsx'],
        'pptxs': ['pptx'],
        'JAVA files': ['java'],
        'class files': ['class'],
        'Video': ['mp4', 'avi', 'mkv'],
        'Other': []
    }

    seen_hashes = {}  # Dictionary to track file hashes
    duplicates_folder = os.path.join(folder_path, "Duplicates")
    os.makedirs(duplicates_folder, exist_ok=True)

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            # Calculate hash to check for duplicates
            file_hash = calculate_file_hash(file_path)
            if file_hash in seen_hashes:
                # If duplicate, move to Duplicates folder
                duplicate_path = os.path.join(duplicates_folder, file)
                try:
                    shutil.move(file_path, duplicate_path)
                    print(f"Duplicate found: {file} -> Moved to Duplicates folder.")
                except PermissionError:
                    print(f"Permission error while moving duplicate: {file}")
                except Exception as e:
                    print(f"Error moving file {file} to Duplicates folder: {e}")
                continue
            else:
                seen_hashes[file_hash] = file_path

            # Categorize the file
            ext = file.split('.')[-1].lower()
            category = 'Other'  # Default category
            for key, ext_list in extensions.items():
                if ext in ext_list:
                    category = key
                    break

            # Create folder named after the file type
            dest_folder = os.path.join(folder_path, category)
            os.makedirs(dest_folder, exist_ok=True)

            # Handle file name conflict
            new_file_name = handle_name_conflict(dest_folder, file)

            # Move the file and handle errors
            try:
                shutil.move(file_path, os.path.join(dest_folder, new_file_name))
                print(f"Moved: {file} -> {dest_folder}")
            except PermissionError:
                print(f"Permission error while moving file: {file}")
            except Exception as e:
                print(f"Error moving file {file} to {dest_folder}: {e}")

# Function to search for files by name or extension
def search_files(folder_path, query):
    results = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if query.lower() in file.lower():
                results.append(os.path.join(root, file))
    return results

# Main function
def main():
    print("Welcome to the File Management System")
    print("1. Organize Files (with duplicate handling)")
    print("2. Search Files")
    print("3. Exit")

    folder_path = input("Enter the folder path to manage: ").strip()

    if not os.path.exists(folder_path):
        print("Invalid folder path. Please try again.")
        return

    while True:
        choice = input("\nChoose an option (1/2/3): ").strip()
        if choice == '1':
            organize_files(folder_path)
            print("Files organized successfully. Duplicates handled.")
        elif choice == '2':
            query = input("Enter the file name or extension to search: ").strip()
            results = search_files(folder_path, query)
            if results:
                print("Search Results:")
                for result in results:
                    print(result)
            else:
                print("No files found matching your query.")
        elif choice == '3':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
