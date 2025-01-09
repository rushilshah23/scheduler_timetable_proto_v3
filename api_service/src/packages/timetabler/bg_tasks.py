from src.packages.timetabler.business.utils import save_output_file
from src.packages.timetabler.modules.ga_scale import generate_timetable
from src.packages.timetabler.business.business_utils import Utils
from .pdf_service.service_2 import create_class_timetable_pdfs
import os
import zipfile
from celery import shared_task
from celery.contrib.abortable import AbortableTask

@shared_task(bind=True, base=AbortableTask, ignore_result=False)
def generate_university_timetable_task(self,req_data):
    # Generate the timetable
    fittest_chromosome = generate_timetable(req_data)
    university_timetables = Utils.sort_slots(fittest_chromosome.genes)
    
    # Save the output as a JSON file
    save_output_file('output_utt_1.json', university_timetables)

    # Create PDF timetables
    pdfs_path, university_id = create_class_timetable_pdfs(university_timetables)

    # Zip the PDFs and the optional JSON
    zip_filename = f"{university_id}.zip"
    print(f"PDF PATH IS = {pdfs_path}")
    zip_file_path = zip_pdfs(pdfs_path=pdfs_path, zip_filename=zip_filename)

    return zip_file_path  # Return the path to the generated zip file


import os
import zipfile
from flask import send_file

def zip_pdfs(pdfs_path, zip_filename, json_file_path=None):
    """
    Zips the contents of a given folder (including subdirectories) and optionally includes a JSON file.
    :param pdfs_path: Path to the folder containing PDFs (can have subdirectories)
    :param zip_filename: The name of the resulting zip file
    :param json_file_path: Path to an optional JSON file to include in the zip
    :return: The path to the created zip file
    """
    # Extract the parent directory of pdfs_path and construct the zip file path
    parent_dir = os.path.dirname(pdfs_path)
    print("PARENT DIR - ",parent_dir)
    zip_file_path = os.path.join(parent_dir, zip_filename)
    print("ZIP PATH DIR - ",zip_file_path)

    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Optionally add the JSON file to the zip
        if json_file_path:
            zipf.write(json_file_path, os.path.basename(json_file_path))

        # Walk through the directory and add all PDFs and subdirectories
        for foldername, subfolders, filenames in os.walk(pdfs_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, pdfs_path)
                zipf.write(file_path, arcname)

    return zip_file_path