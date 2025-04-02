import os
import json
import glob
import shutil
import hashlib
from isatools import isatab
from isatools.model import Investigation


def calculate_sha256(filename):
    """Calculates the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filename, 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except FileNotFoundError:
        print(f"Error: File not found - {filename}")
        return None
    except Exception as e:
        print(f"Error calculating SHA256 for {filename}: {e}")
        return None


def isatab_to_isa_json(isa_tab_directory, output_directory):
    print(f"Starting conversion for: {isa_tab_directory}")

    try:
        investigation = isatab.load(isa_tab_directory)

        if investigation is None:
            print(f"Warning: No valid ISA-Tab data loaded from {isa_tab_directory}")
            return  # Stop execution if loading fails

        print("Successfully loaded ISA-Tab")

        os.makedirs(output_directory, exist_ok=True)

        isa_json_filename = os.path.join(output_directory, "isa.json")

       # Convert to JSON
        isa_json = investigation.to_dict()

        # Debugging: Print existing keys in the JSON
        print(f"Keys in ISA-JSON: {list(isa_json.keys())}")

        # Try to detect the actual investigation file
        investigation_files = [f for f in os.listdir(isa_tab_directory) if f.startswith("i_") and f.endswith(".txt")]
        investigation_file = investigation_files[0] if investigation_files else "i_*.txt"

        # Check for missing required fields
        required_fields = {
            "version": "1.0",
            "investigationFilePath": investigation_file,
            "samples": [],
            "assays": [],
            "parserMessages": [],
            "referencedAssignmentFiles": [],
            "referencedRawFiles": [],
            "referencedDerivedFiles": [],
            "foldersInHierarchy": []
        }

        missing_keys = set(required_fields.keys()) - set(isa_json.keys())

        if missing_keys:
            print(f"⚠️ Warning: The following required keys are missing and will be added: {missing_keys}")

            # Add missing fields
            for key in missing_keys:
                isa_json[key] = required_fields[key]

        # Print a short preview of the JSON structure (first 500 characters)
        print(f"ISA JSON preview:\n{json.dumps(isa_json, indent=4)[:500]}...")

        # Save JSON
        with open(isa_json_filename, "w") as output_file:
            json.dump(isa_json, output_file, indent=4)
      
    except Exception as e:
        print(f"❌ Error converting ISA-Tab in '{isa_tab_directory}': {type(e).__name__} - {e}")


def copy_directory_contents(source_dir, destination_dir):
    """
    Copies all files and directories from the source directory to the destination.

    Args:
        source_dir (str): Source directory path.
        destination_dir (str): Destination directory path.
    """
    os.makedirs(destination_dir, exist_ok=True)

    for item in os.listdir(source_dir):
        src_path = os.path.join(source_dir, item)
        dst_path = os.path.join(destination_dir, item)

        try:
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                print(f"📁 Copied directory: {src_path} -> {dst_path}")
            else:
                shutil.copy2(src_path, dst_path)
                print(f"📄 Copied file: {src_path} -> {dst_path}")
        except Exception as e:
            print(f"⚠️ Failed to copy {src_path} -> {dst_path}: {e}")


def process_isa_tab_studies(root_directory, output_root):
    """
    Processes all ISA-Tab studies within the root directory, converts them to ISA-JSON, 
    and saves the output in the corresponding output directory.

    Args:
        root_directory (str): Path to the root directory containing ISA-Tab studies.
        output_root (str): Path to the root output directory where ISA-JSON files will be saved.
    """
    print(f"\n🔍 Processing ISA-Tab studies in: {root_directory}")
    print(f"📁 Output root: {output_root}")

    for study_directory in glob.glob(os.path.join(root_directory, 'MTBLS*')):
        if os.path.isdir(study_directory):
            study_id = os.path.basename(study_directory)
            output_directory = os.path.join(output_root, study_id)

            print(f"\n🔍 Processing study: {study_id}")
            print(f"📂 Study directory: {study_directory}")
            print(f"📁 Expected output directory: {output_directory}")

            # Copy files (if necessary)
            copy_directory_contents(study_directory, output_directory)

            # Debug before calling conversion
            print(f"🚀 Calling isatab_to_isa_json() for {study_directory} -> {output_directory}")

            # Convert ISA-Tab to ISA-JSON
            isatab_to_isa_json(study_directory, output_directory)

            # Debug after function call
            print(f"✅ Completed conversion for {study_id}, checking output...")

            # Check if the JSON file was actually written
            json_path = os.path.join(output_directory, "isa.json")
            if os.path.exists(json_path):
                print(f"🎉 JSON successfully written: {json_path}")
            else:
                print(f"⚠️ JSON NOT FOUND at expected location: {json_path}")


# Example usage
if __name__ == "__main__":
    root_directory = "/home/karen/CFM_ISA/ISA-Tab-Templates/metadata/"  # Path to metadata folder
    output_root = "/home/karen/CFM_ISA/mtbls-validation/my_json_output"

    process_isa_tab_studies(root_directory, output_root)

