# Reads the CSV file for stapleton , then loops through each row of the csv file, the following would be done to each of the rows.
# Note , connect to the database before running the loop. and disconnect after.

# The reson cursor and con arent defined is because they would need to defined before the functions are called, so before the loop would start.

import csv
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import argparse
import re

import logging

# Configure logging
logging.basicConfig(
    filename="Import_logging_output.log",  # Log file name
    filemode="w",           # Use "w" to overwrite or "a" to append
    format="%(asctime)s - %(message)s",  # Log message format
    level=logging.INFO      # Log level (INFO, DEBUG, etc.)
)

#Create_patient()# save id
#Create_vist()# None.
#Create_admissionn_note()# save id


# Set up the argument parser
import argparse

# Create the argument parser
parser = argparse.ArgumentParser(description="Process user ID and a file from the command line.")
parser.add_argument('user_id', type=str, help="The User ID to be processed")
parser.add_argument('file', type=str, help="The file to be processed (e.g., file.csv)")

# Parse the command-line arguments
args = parser.parse_args()

# Assign the user_id and file from the command-line arguments
user_id = args.user_id
file_path = args.file

# Print the parsed arguments (for demonstration purposes)
print(f"User ID: {user_id}")
print(f"File Path: {file_path}")


import logging
from datetime import datetime
from mysql.connector import Error

def create_patient(folder_number, id_number, first_name, last_name, title, dob, gender, created_at, updated_at, merged, organisation_id, canonical, conn, cursor):
    """
    Creates a patient record in the database if it does not already exist.

    Args:
        folder_number (str): Patient's folder number.
        id_number (str): Patient's ID number.
        first_name (str): First name of the patient.
        last_name (str): Last name of the patient.
        title (str): Title of the patient (e.g., Mr., Mrs.).
        dob (str): Date of birth in DD/MM/YYYY format.
        gender (str): Gender (M/F/Other).
        created_at (str): Timestamp for record creation.
        updated_at (str): Timestamp for record update.
        merged (bool): Merged flag.
        organisation_id (str): Organisation ID.
        canonical (str): Canonical ID.
        conn: Database connection.
        cursor: Database cursor.

    Returns:
        int: ID of the existing or newly created patient.
    """
    try:
        # Check if the patient exists
        patient_query = """
        SELECT id 
        FROM patients 
        WHERE folder = %s AND organisation_id = %s AND canonical = %s
        """
        cursor.execute(patient_query, (folder_number, organisation_id , canonical))
        results = cursor.fetchall()

        if results:
            result = results[-1]
            patient_id = result[0]
            print(f"Patient exists with ID: {patient_id}")
            logging.info(f"Patient exists with ID: {patient_id}")
            return patient_id

        # Parse and validate date of birth
        if dob:
            try:
                dob = dob.replace(".", "/").replace("-", "/")
                parsed_date = datetime.strptime(dob.strip(), "%d/%m/%Y")
                pdob = parsed_date.strftime("%Y/%m/%d")
            except ValueError:
                logging.error(f"Invalid DOB format: {dob}. Using default '0000/00/00'.")
                pdob = "0000/00/00"
        else:
            pdob = "0000/00/00"

        # Determine gender
        gender_map = {"m": "0", "f": "1"}
        p_gender = gender_map.get(gender.lower(), "2") if gender else "2"

        # Insert new patient record
        query = """
        INSERT INTO patients (folder, id_number, first_name, last_name, title, date_of_birth, gender, created_at, updated_at, merged, organisation_id, canonical)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (folder_number, id_number, first_name, last_name, title, pdob, p_gender, created_at, updated_at, merged, organisation_id, canonical))
        conn.commit()

        # Retrieve the ID of the newly created patient
        patient_id = cursor.lastrowid
        print(f"Patient created successfully with ID: {patient_id}")
        logging.info(f"Patient created successfully with ID: {patient_id}")
        return patient_id

    except Error as e:
        logging.error(f"Error creating patient: {e}")
        conn.rollback()
        raise

def create_admission_forms(patient_id,created_at,updated_at, conn, cursor):

    query = """
    INSERT INTO admission_forms (patient_id, created_at, updated_at)
    VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(query, (patient_id, created_at, updated_at))
    
    # Commit the transaction
        conn.commit()

    # Get the ID of the newly inserted patient
        admission_form_id = cursor.lastrowid
        print(f"Admission_form created successfully with ID: {admission_form_id}")
        logging.info(f"Admission_form created successfully with ID: {admission_form_id}")
        
        return admission_form_id # returns the id for use in the next functions.

    except Error as e:
        print(f"Error Admission form not created: {e}")
        logging.info(f"Error Admission form not created: {e}")
        conn.rollback() 

def create_clinical_history_and_physical(user_id, patient_id,admission_form_id, conn, cursor, created_at,updated_at):

    signed_off = 0
    time_for_import = created_at # created_at , returns a formatted time, which can be used for the other values
    recorded_at = time_for_import
    created_at = time_for_import
    updated_at = time_for_import
    note_catagory_id = 6

    query = """
    INSERT INTO clinical_history_and_physicals (user_id, patient_id, recorded_at, signed_off, created_at, updated_at, note_category_id, admission_form_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (user_id, patient_id, recorded_at, signed_off, created_at, updated_at, note_catagory_id, admission_form_id))
    
    # Commit the transaction
        conn.commit()

    # Get the ID of the newly inserted patient
        clinical_history_and_physical_id = cursor.lastrowid
        print(f"create_clinical_history_and_physical created successfully with ID: {clinical_history_and_physical_id}")
        logging.info(f"create_clinical_history_and_physical created successfully with ID: {clinical_history_and_physical_id}")
        return clinical_history_and_physical_id # returns the id for use in the next functions.

    except Error as e:
        print(f"Error create_clinical_history_and_physical not created: {e}")
        logging.info(f"Error create_clinical_history_and_physical not created: {e}")
        conn.rollback()


def create_ongoing_problems(clinical_history_and_physical_id, Problem_list, conn, cursor):

    query = """
    INSERT INTO clinical_history_and_physical_patient_ongoing_problems (clinical_history_and_physical_id, name)
    VALUES (%s, %s)
    """
    try:
        sections = Problem_list.split('\v')  # Split the Problem_list by vertical tab
        for i, section in enumerate(sections, start=1):
            # Skip empty sections
            if not section.strip():  # strip removes leading/trailing whitespaces
                print(f"Skipping empty section in problem list {i}")
                continue

            cursor.execute(query, (clinical_history_and_physical_id, section))  # Use section instead of Problem_list
            # Get the ID of the newly inserted record
            ongoing_problems_id = cursor.lastrowid
            print(f"create_ongoing_problems created successfully with ID: {ongoing_problems_id}")
            logging.info(f"create_ongoing_problems created successfully with ID: {ongoing_problems_id}")

        # Commit the transaction once after the loop
        conn.commit()

    except Exception as e:
        print(f"Error ongoing problems: {e}")
        logging.error(f"Error ongoing problems: {e}")
        conn.rollback()  # Rollback in case of error to avoid partial data insert

def create_allergies(patient_id, allergies, conn, cursor, created_at):
    """
    Function to create an allergy record for a patient.
    Args:
        patient_id: ID of the patient.
        allergies: Name of the allergy (string).
        conn: Database connection object.
        cursor: Database cursor object.
        created_at: Timestamp of record creation.
    """
    if allergies is None:
        return  # Skip if allergies is None

    recorded_at = created_at  # Use the passed timestamp as the recorded_at value
    allergy = allergies.strip().lower()  # Normalize allergy name

    try:
        # Query to check if the allergy exists in the allergens database
        query_allergen_id = "SELECT id FROM allergens WHERE name = %s"
        cursor.execute(query_allergen_id, (allergy,))
        result = cursor.fetchone()

        if result:
            # If the allergen exists, insert into the allergies table
            allergen_id = result[0]
            query = """
                INSERT INTO allergies (patient_id, allergen_id, recorded_at, start_date)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (patient_id, allergen_id, recorded_at, recorded_at))  # Assuming start_date = recorded_at
            conn.commit()

            allergies_id = cursor.lastrowid
            print(f"Allergy record created successfully with ID: {allergies_id}")
            logging.info(f"Allergy record created successfully with ID: {allergies_id}")
        else:
            # If the allergen does not exist, insert it as a failed allergen
            failed_allergen_id = 9  # ID for unknown allergens
            query = """
                INSERT INTO allergies (patient_id, allergen_id, other, recorded_at, start_date)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (patient_id, failed_allergen_id, allergy, recorded_at, recorded_at))  # Assuming start_date = recorded_at
            conn.commit()

            allergies_id = cursor.lastrowid
            print(f"Unknown allergen record created successfully with ID: {allergies_id}")
            logging.info(f"Unknown allergen record created successfully with ID: {allergies_id}")
    except Exception as e:
        print(f"Error: {e}")
        logging.info(f"Error: {e}")
        conn.rollback() 



def create_occupation(create_clinical_history_and_physical_id, occupation, conn, cursor):
    """
    Function to create an occupation record for a clinical history and physical entry.
    Args:
        create_clinical_history_and_physical_id: ID of the clinical history and physical entry.
        occupation: Name of the occupation (string).
        conn: Database connection object.
        cursor: Database cursor object.
    
    """

    if occupation is None:
        return  # Skip if occupation is None
    
    occupation = occupation.strip().lower()  # Normalize the occupation name

    try:
        # Query to check if the occupation exists in the database
        query_occupation_id = "SELECT id FROM occupations WHERE name = %s"
        cursor.execute(query_occupation_id, (occupation,))
        result = cursor.fetchone()

        if result:
            # If the occupation exists, insert into the clinical history table
            occupation_id = result[0]
            query = """
                INSERT INTO clinical_history_and_physical_patient_occupations (clinical_history_and_physical_id, occupation_id)
                VALUES (%s, %s)
            """
            cursor.execute(query, (create_clinical_history_and_physical_id, occupation_id))
            conn.commit()

            record_id = cursor.lastrowid
            print(f"Occupation record created successfully with ID: {record_id}")
            logging.info(f"Occupation record created successfully with ID: {record_id}")    
        else:
            # If the occupation does not exist, insert it as a detail
            query = """
                INSERT INTO clinical_history_and_physical_patient_occupations (clinical_history_and_physical_id, detail)
                VALUES (%s, %s)
            """
            cursor.execute(query, (create_clinical_history_and_physical_id, occupation))
            conn.commit()

            record_id = cursor.lastrowid
            print(f"Unknown occupation record created successfully with ID: {record_id}")
            logging.info(f"Unknown occupation record created successfully with ID: {record_id}")
    except Exception as e:
        print(f"Error: {e}")
        logging.info(f"Error: {e}")
        conn.rollback() 

def create_pshx(clinical_history_and_physical_id, pshx_value, conn, cursor):
    other = pshx_value
    default_value = 12  # Set your default value for procedure_type_id

    query = """
    INSERT INTO clinical_history_and_physical_past_surgical_procedures 
    (clinical_history_and_physical_id, procedure_type_id, other)
    VALUES (%s, %s, %s)
    """
    try:
        sections = other.split('\v')  # Split the pshx_value by vertical tab
        for i, section in enumerate(sections, start=1):
            # Skip empty sections
            if not section.strip():  # strip removes leading/trailing whitespaces
                print(f"Skipping empty section {i}")
                continue

            cursor.execute(query, (clinical_history_and_physical_id, default_value, section))  # Use section instead of other
            # Get the ID of the newly inserted record
            pshx_id = cursor.lastrowid
            print(f"create_pshx created successfully with ID: {pshx_id}")
            logging.info(f"create_pshx created successfully with ID: {pshx_id}")

        # Commit the transaction once after the loop
        conn.commit()

    except Exception as e:
        print(f"Error during create_pshx: {e}")
        logging.error(f"Error during create_pshx: {e}")
        conn.rollback()  # Rollback in case of error to avoid partial data insert

def create_pmhx(clinical_history_and_physical_id, PMHX, conn, cursor):
    """
    Inserts records into the clinical_history_and_physical_admission_pmhx_options table
    based on the provided PMHX data, split by vertical tabs.

    Args:
        clinical_history_and_physical_id (int): ID for the clinical history and physical entry.
        PMHX (str): Past medical history data, potentially containing multiple sections separated by vertical tabs.
        conn: The database connection object.
        cursor: The database cursor object.
    """
    pmhx_option_id = 87
    query = """
    INSERT INTO clinical_history_and_physical_admission_pmhx_options (clinical_history_and_physical_id, pmhx_option_id, other)
    VALUES (%s, %s, %s)
    """
    try:
        sections = PMHX.split("\v")  # Split the PMHX value by vertical tabs
        for i, section in enumerate(sections, start=1):
            other_value = section.strip()  # Remove any leading/trailing whitespace

            # Skip empty or whitespace-only sections
            if not other_value:
                print(f"Skipping empty section {i}")
                logging.info(f"Skipping empty section {i}")
                continue

            cursor.execute(query, (clinical_history_and_physical_id, pmhx_option_id, other_value))

            # Get the ID of the newly inserted record
            clinical_history_and_physical_admission_pmhx_options_id = cursor.lastrowid
            print(f"create_pmhx created successfully with ID: {clinical_history_and_physical_admission_pmhx_options_id}")
            logging.info(f"create_pmhx created successfully with ID: {clinical_history_and_physical_admission_pmhx_options_id}")

        # Commit the transaction once after all sections are processed
        conn.commit()

    except Exception as e:
        print(f"Error create_pmhx not created: {e}")
        logging.error(f"Error create_pmhx not created: {e}")
        conn.rollback()  # Rollback in case of error to avoid partial data insert


def create_contraception(clinical_history_and_physical_id, contraception, conn, cursor):
    """
    Function to create a contraception record for a clinical history and physical entry.
    Args:
        clinical_history_and_physical_id: ID of the clinical history and physical entry.
        contraception: Name of the contraception method (string).
        conn: Database connection object.
        cursor: Database cursor object.
    """
    if contraception is None:
        return  # Skip if contraception is None
    
    contraception = contraception.strip().lower()  # Normalize the contraception name

    try:
        # Query to check if the contraception method exists in the database
        query_contraception_id = "SELECT id FROM contraception_methods WHERE name = %s"
        cursor.execute(query_contraception_id, (contraception,))
        result = cursor.fetchone()

        if result:
            # If the contraception method exists, insert into the clinical history table
            contraception_method_id = result[0]
            query = """
                INSERT INTO clinical_history_and_physical_contraceptions (clinical_history_and_physical_id, contraception_method_id)
                VALUES (%s, %s)
            """
            cursor.execute(query, (clinical_history_and_physical_id, contraception_method_id))
            conn.commit()

            record_id = cursor.lastrowid
            print(f"Contraception record created successfully with ID: {record_id}")
            logging.info(f"Contraception record created successfully with ID: {record_id}")
        else:
            # If the contraception method does not exist, insert it as a detail
            query = """
                INSERT INTO clinical_history_and_physical_contraceptions (clinical_history_and_physical_id, other)
                VALUES (%s, %s)
            """
            cursor.execute(query, (clinical_history_and_physical_id, contraception))
            conn.commit()

            record_id = cursor.lastrowid
            print(f"Unknown contraception method record created successfully with ID: {record_id}")
            logging.info(f"Unknown contraception method record created successfully with ID: {record_id}") 

    except Exception as e:
        print(f"Error Contraception not created: {e}")
        logging.info(f"Error Contraception not created: {e}")
        conn.rollback() 


def fix_gtpal_type(s):
    if s == "":
        return None
    s = re.sub(r"\D", "", s)
    return int(s) if s else None

def create_gtpals(clinical_history_and_physical_id, G, T, P, A, L, description,  conn, cursor): 

    

    # cheeks if gtpals is empty, true = stop function
    if G == T== P == A == L == description ==None :
        print('gptals is empty')
        logging.info('gptals is empty')
        return
    
    # fix gtpals to int

    G = fix_gtpal_type(G)
    T = fix_gtpal_type(T)
    P = fix_gtpal_type(P)
    A = fix_gtpal_type(A)
    L = fix_gtpal_type(L)
    
    query = """
    INSERT INTO clinical_history_and_physical_gtpals (clinical_history_and_physical_id,gravida,term,preterm,abortions,living_children,description)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (clinical_history_and_physical_id, G, T, P, A, L, description))
    
         # Commit the transaction
        conn.commit()

        # Get the ID of the newly inserted patient
        clinical_history_and_physical_patient_occupations_id = cursor.lastrowid
        print(f"create_gtpals created successfully with ID: {clinical_history_and_physical_patient_occupations_id}")
        logging.info(f"create_gtpals created successfully with ID: {clinical_history_and_physical_patient_occupations_id}")
    except Error as e:
        print(f"Error: {e}")
        logging.info(f"Error: {e}")
        conn.rollback() 



def get_sdpr_patient_id(patient_unique_id ,created_at ,conn,  cursor):# no need for conn, no commit required
    updated_at = created_at
    try:
        # Query to get the sdpr_patient_id
        query_patient_id = """
        INSERT INTO sdpr_patients (id_number,created_at,updated_at)
        VALUES (%s, %s, %s)
        """  # Adjust column name
        cursor.execute(query_patient_id, (patient_unique_id, created_at ,updated_at))
        conn.commit()
        sdpr_patient_id = cursor.lastrowid
        print(f"sdpr_patient_id created successfully with ID: {sdpr_patient_id}")
        logging.info(f"sdpr_patient_id created successfully with ID: {sdpr_patient_id}")
        return sdpr_patient_id
        

    except Error as e:
        print(f"Error while fetching sdpr_patient_id: {e}")
        logging.info(f"Error while fetching sdpr_patient_id: {e}")
        conn.rollback() 
        return None

def create_socialhx(admission_form_id, social_hx, conn, cursor):
    """
    Inserts records into the sdpr_patient_admission_form_options table with formatted social history data.

    Args:
        created_at (str): The creation timestamp.
        updated_at (str): The update timestamp.
        sdpr_patient_id (int): The ID of the patient.
        social_hx (str): Social history data, potentially containing multiple sections separated by vertical tabs.
        conn: The database connection object.
        cursor: The database cursor object.
    """
    cancelled = 0
    admission_form_option_id = 11
    query = """
    INSERT INTO admission_form_option_answers (admission_form_id,admission_form_option_id, other, cancelled)
    VALUES ( %s, %s, %s, %s)
    """
    try:
        sections = social_hx.split("\v")  # Split the social_hx string by vertical tabs
        for section in sections:
            other = section.strip()  # Remove any leading or trailing whitespace
            if not other:  # Skip empty or whitespace-only sections
                continue

            cursor.execute(query, (admission_form_id, admission_form_option_id, other, cancelled))
            
            # Commit the transaction
            conn.commit()

            # Get the ID of the newly inserted record
            socialhx_id = cursor.lastrowid
            print(f"create_socialhx created successfully with ID: {socialhx_id}")
            logging.info(f"create_socialhx created successfully with ID: {socialhx_id}")

    except Error as e:
        print(f"Error create_socialhx not created: {e}")
        logging.info(f"Error create_socialhx not created: {e}")
        conn.rollback()



def create_familyhx(admission_form_id, family_hx, conn, cursor):
    """
    Inserts records into the sdpr_patient_admission_form_options table with formatted family history data.

    Args:
        created_at (str): The creation timestamp.
        updated_at (str): The update timestamp.
        sdpr_patient_id (int): The ID of the patient.
        family_hx (str): Family history data, potentially containing multiple sections separated by vertical tabs.
        conn: The database connection object.
        cursor: The database cursor object.
    """
    cancelled = 0
    admission_form_option_id = 14
    query = """
    INSERT INTO admission_form_option_answers (admission_form_id,admission_form_option_id, other, cancelled)
    VALUES (%s, %s, %s, %s)
    """
    try:
        sections = family_hx.split("\v")  # Split the family_hx string by vertical tabs
        for section in sections:
            other = section.strip()  # Remove any leading or trailing whitespace
            if not other:  # Skip empty or whitespace-only sections
                continue

            cursor.execute(query, (admission_form_id,admission_form_option_id, other, cancelled))
            
            # Commit the transaction
            conn.commit()

            # Get the ID of the newly inserted record
            familyhx_id = cursor.lastrowid
            print(f"create_familyhx created successfully with ID: {familyhx_id}")
            logging.info(f"create_familyhx created successfully with ID: {familyhx_id}")

    except Error as e:
        print(f"Error create_familyhx not created: {e}")
        logging.info(f"Error create_familyhx not created: {e}")
        conn.rollback()



def create_past_gyne_surg(patient_id, created_at, updated_at, prev_gyn_surg, conn, cursor):
    procedure_type_id = 1041
    procedure_catagory_id = 29
    cancelled = 0
    other = prev_gyn_surg
    start_date = created_at  # Returns a formatted time string
    end_date = created_at  # Returns a formatted time string

    # First, add the procedure to the database
    query_procedure = """
    INSERT INTO procedures (patient_id, start_date, end_date, procedure_type_id,procedure_category_id, other, cancelled, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query_procedure, (patient_id, start_date, end_date, procedure_type_id, procedure_catagory_id, other, cancelled, created_at, updated_at))
        conn.commit()
        # Get the ID of the newly inserted procedure
        procedure_id = cursor.lastrowid
        print(f"Procedure created successfully with ID: {procedure_id}")
        logging.info(f"Procedure created successfully with ID: {procedure_id}")
    except Error as e:
        print(f"Error inserting procedure: {e}")
        logging.info(f"Error inserting procedure: {e}")
        conn.rollback() 
        return  # Exit the function to avoid referencing `procedure_id` if the insertion fails

    # Now, add the surgery to the database
    drains = 0
    unscheduled_return = 0
    incomplete = 0
    query_surgery = """
    INSERT INTO surgeries (procedure_id, created_at, updated_at, drains, cancelled, unscheduled_return, incomplete)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query_surgery, (procedure_id, created_at, updated_at, drains, cancelled, unscheduled_return, incomplete))
        conn.commit()
        # Get the ID of the newly inserted surgery
        surgery_id = cursor.lastrowid
        print(f"Surgery created successfully with ID: {surgery_id}")
        logging.info(f"Surgery created successfully with ID: {surgery_id}")
    except Error as e:
        print(f"Error inserting surgery: {e}")
        logging.info(f"Error inserting surgery: {e}")
        conn.rollback() 

    
def create_rxhx(patient_id, rxhx ,created_at,updated_at, conn, cursor):# this still has to be worked on , reppurosed database check function
    mark = 0
    drug_name = rxhx
    start_date = created_at
    end_date = created_at
    is_surgical_prophylaxis = 0

    try:
        # Query to check the drugfrom the pms , if its in the database.
        query_drug_id = "SELECT id FROM drugs WHERE name = %s"  # Adjust column name
        cursor.execute(query_drug_id, (drug_name,))
        result = cursor.fetchone()



        if result:
            drug_id = result[0]
            query = """
            INSERT INTO patient_drugs (patient_id ,drug_id ,start_date ,end_date ,is_surgical_prophylaxis ,created_at ,updated_at ,mark)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            try:
                cursor.execute(query, (patient_id,drug_id,start_date,end_date,is_surgical_prophylaxis,created_at,updated_at,mark))
    
                # Commit the transaction
                conn.commit()

                # Get the ID of the newly inserted patient
                surgery_id = cursor.lastrowid
                print(f"create_rxhx created successfully with ID: {surgery_id} with drug id {drug_id}")
                logging.info(f"create_rxhx created successfully with ID: {surgery_id} with drug id {drug_id}")
        
        
            except Error as e:
                print(f"Error create_rxhx not created: {e}")
                logging.info(f"Error create_rxhx not created: {e}")
                conn.rollback() 


        elif not result:
            print(f"this is the patient id {patient_id}")
            logging.info(f"this is the patient id {patient_id}")
            drug_id = 4397
            query = """
            INSERT INTO patient_drugs (patient_id,drug_id,start_date,end_date,is_surgical_prophylaxis,created_at,updated_at,mark)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            try:
                cursor.execute(query, (patient_id,drug_id,start_date,end_date,is_surgical_prophylaxis,created_at,updated_at,mark))
    
                # Commit the transaction
                conn.commit()

                # Get the ID of the newly inserted patient
                surgery_id = cursor.lastrowid
                print(f"create_rxhx default created successfully with ID: {surgery_id}")
                logging.info(f"create_rxhx default created successfully with ID: {surgery_id}")
        
        
            except Error as e:
                print(f"Error create_rxhx 'other': {e}")
                logging.info(f"Error create_rxhx 'other': {e}")
                conn.rollback() 

        else:
            print("Error create_rxhx , other failure: Patient record not found.")
            logging.info("Error create_rxhx , other failure: Patient record not found.")
            return None
        
    except Error as e:
        print(f"Error while fetching sdpr_patient_id(query failure): {e}")
        logging.info(f"Error while fetching sdpr_patient_id(query failure): {e}")
        conn.rollback() 
        

#create patient done --> create Admission_form --> create clinical_history_and_physical_id --> continue normal flow.
#separate the extraction of id's (patient_id/clinical_history_and_physical_id, admission_di) 

#Theres still more to do, but untill i figure it out, lemme work on how the the PROCESS works.



def importing_data_from_stapleton_file(user_id,file_path, conn, cursor):
    # Open the CSV file
    with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
    
        # Loop through each row in the CSV
        for row_number, row in enumerate(csv_reader, start=1):
            
            title = row['Title']
            name_last = row['Namelast']
            name_first = row['NameFirst']
            id_number = row['ID'] ######### When creating the export try to merge in the id number - this is required for the patient table.
            dob = row['DOB'] ###### When creating the export try to merge in the DOB  - this is required for the patient table.
            gender = row['Gender'] ###### When creating the export try to merge in the gender - this is required for the patient table.
            contraception = row['Contraception'] ######## when creating the export try to merge in the Contraception - this is required for the Contraception table.
            #partner = row['partner']
            #referral = row['Referral']
            #med_aid = row['Med.Aid']
            folder_number = row['FolderNumber']
            #salutation = row['Salutation']
            #age_calc = row['Age calc']
            #lmp = row['LMP:']
            occupation = row['Occupation']
            allergies = row['Allergies']
            social_hx = row['SocialHx:']
            family_hx = row['FamilyHx:']
            pmhx = row['PMHx']
            pshx = row['PSHx']
            rxhx = row['RxHx']
            problem_list = row['Problemlist']
            #confidential = row['Confidential']
            g = row['G']
            t = row['T']
            p = row['P']
            a = row['A']
            l = row['L']
            births = row['births'] # GTPALs description
            prev_gyn_surg = row['prev.gynsurg.']
            #problem_1 = row['Problem1']
            #hx_problem = row['Hxproblem']
            #temp = row['Temp']
            #pulse = row['Pulse']
            #bp = row['B.P.']
            #waist_circ = row['WaistCirc']
            #weight = row['Weight']
            #height = row['Height']
            #bmi = row['BMI']
            #general_exam = row['Generalexam.']
            #investigations = row['Investigations']
            #ultrasound = row['ultrasound']
            #assessment = row['Assessment:']
            #plan = row['Plan']
            #dr_name = row['Drname']
            #time modification to the normal format

            current_time = datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

            created_at = formatted_time
            updated_at = formatted_time

            merged = "0"
            organisation_id = "67571" #######, organisation id hard coded for now, for this one use case.
            canonical = "1"

            print(f"Processing row {row_number}")
            logging.info(f"Processing row {row_number}")

            #These store ID's that would be used in the other tables.
            # Create the patient record and store the patient_id
            patient_id = create_patient(folder_number,id_number,name_first,name_last,title,dob,gender,created_at,updated_at,merged,organisation_id,canonical,conn,cursor)

            # Create the admission_form record and store the admission_form_id
            admission_form_id = create_admission_forms(patient_id,created_at,updated_at,conn,cursor)

            # Create the clinical_history_and_physical_id record and store the clinical_history_and_physical_id
            clinical_history_and_physical_id = create_clinical_history_and_physical(user_id, patient_id,admission_form_id, conn, cursor, created_at,updated_at)

            # Creates the ongoing_problems record
            create_ongoing_problems(clinical_history_and_physical_id, problem_list,conn,cursor)

            # Creates the allergies record
            create_allergies(patient_id ,allergies,conn,cursor,created_at)

            # Creates the Occupation record
            create_occupation(clinical_history_and_physical_id, occupation,conn,cursor)

            # Creates the pmhx record
            create_pmhx(clinical_history_and_physical_id, pmhx,conn,cursor)

            # Creates the Contraception record
            create_contraception(clinical_history_and_physical_id, contraception,conn,cursor)
            
            # Creates the GTPALS records
            create_gtpals(clinical_history_and_physical_id, g, t, p, a, l, births,conn,cursor)

            # Creates pshx record
            create_pshx(clinical_history_and_physical_id,pshx,conn,cursor )

            # Creates the sdpr_patient_id value for social_hx and Family Hx
            #sdpr_patient_id = get_sdpr_patient_id(id_number,created_at ,conn, cursor)

            # Creates the social_hx record
            create_socialhx(admission_form_id ,social_hx,conn,cursor)

            # Creates the family_hx record
            create_familyhx(admission_form_id ,social_hx,conn,cursor)
            
            # Creates the past gyne surg record
            create_past_gyne_surg(patient_id,created_at,updated_at ,prev_gyn_surg ,conn,cursor)

            create_rxhx(patient_id, rxhx ,created_at,updated_at, conn, cursor)
            print("\n")
            logging.info("\n")
# Down here, you want to create a make it run, the connection to the database and the tables. then between you are gonna want to add the importing patient data function.

def Main_function():
    conn = None  # Declare the connection object
    cursor = None  # Declare the cursor object
    file_path = "tester.csv"
    # Create the database connection
    try:
        # Establish the database connection
        conn = mysql.connector.connect(
            host='',
            port='',
            database='',
            user='',
            password=''
        )
        
        # Initialize the cursor
        cursor = conn.cursor() 
        importing_data_from_stapleton_file(user_id,file_path, conn, cursor)

    except Error as e:
        print(f"Error to connect to MySQL database")
        logging.error(f"Error to connect to MySQL database")

    finally:
        # Close the cursor and the connection
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
        print("Database connection closed.\n\n")
        logging.info("Database connection closed.\n\n")


########### Now that all is done we should be able to run the main function
Main_function()
















