# Reads the CSV file for stapleton , then loops through each row of the csv file, the following would be done to each of the rows.
# Note , connect to the database before running the loop. and disconnect after.

# The reson cursor and con arent defined is because they would need to defined before the functions are called, so before the loop would start.

import csv
import mysql.connector
from mysql.connector import Error
import datetime
import argparse

#Create_patient()# save id
#Create_vist()# None.
#Create_admissionn_note()# save id


# Set up the argument parser
parser = argparse.ArgumentParser(description="Process user ID from the command line.")
parser.add_argument('user_id', type=str, help="The User ID to be processed")

# Parse the command-line arguments
args = parser.parse_args()

# Assign the user_id from the command-line argument
user_id = args.user_id




def create_patient(Folder_number,Id_number,First_name,last_name,title,dob,Gender,created_at,updated_at,merged,organisation_id,canonical, conn, cursor):#open connection before, or after this runs, check with mike.
    query = """
        INSERT INTO patients (Folder_number, Id_number, First_name, last_name, title, dob, Gender, created_at, updated_at, merged, organisation_id, canonical)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
    try:
        cursor.execute(query, (Folder_number, Id_number, First_name, last_name, title, dob, Gender, created_at, updated_at, merged, organisation_id, canonical))

    # Commit the transaction
        conn.commit()

    # Get the ID of the newly inserted patient
        patient_id = cursor.lastrowid
        print(f"Patient created successfully with ID: {patient_id}")
        
        return patient_id # returns the id for use in the next functions.

    except Error as e:
        print(f"Error: {e}")

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
        
        return admission_form_id # returns the id for use in the next functions.

    except Error as e:
        print(f"Error: {e}")



def create_clinical_history_and_physical(user_id, patient_id,admission_form_id, conn, cursor, created_at,updated_at):

    signed_off = 0
    time_for_import = created_at # created_at , returns a formatted time, which can be used for the other values
    recorded_at = time_for_import
    created_at = time_for_import
    updated_at = time_for_import
    note_catagory_id = 6



    query = """
    INSERT INTO clinical_history_and_physicals (user_id, patient_id, recorded_at, signed_off, created_at, updated_at, note_catagory_id, admission_form_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (user_id, patient_id, recorded_at, signed_off, created_at, updated_at, note_catagory_id, admission_form_id))
    
    # Commit the transaction
        conn.commit()

    # Get the ID of the newly inserted patient
        clinical_history_and_physical_id = cursor.lastrowid
        print(f"Admission_form created successfully with ID: {clinical_history_and_physical_id}")
        
        return clinical_history_and_physical_id # returns the id for use in the next functions.

    except Error as e:
        print(f"Error: {e}")



def create_ongoing_problems(clinical_history_and_physical_id,Problem_list , conn, cursor):
    query = """
    INSERT INTO clinical_history_and_physical_patient_ongoing_problems (clinical_history_and_physical_id, Problem_list)
    VALUES (%s, %s)
    """
    try:
        cursor.execute(query, (clinical_history_and_physical_id,Problem_list))
    
    # Commit the transaction
        conn.commit()

    # Get the ID of the newly inserted patient
        ongoing_problems_id = cursor.lastrowid
        print(f"Admission_form created successfully with ID: {ongoing_problems_id}")
        
    except Error as e:
        print(f"Error: {e}")

allergens_dict = {
    1: "Penicillin",
    2: "Sulfa drugs", 
    3: "Tetracycline",
    4: "Codeine",
    5: "Non-steroidal anti-inflammatory drugs (NSAIDs)",
    6: "Phenytoin", 
    7: "Carbamazepine",
    8: "Rubber",
    9: "Other",
    10: "lodine",
    11: "Bee stings",
    12: "Seafood",
    13: "Latex",
    14: "Elastoplast",
    15: "Asprin",
    16: "Lanzor",
    17: "Local anaesthetics"
}

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
    recorded_at = created_at  # Use the passed timestamp as the recorded_at value
    allergy = allergies.strip().lower()  # Normalize allergy name

    try:
        # Query to check if the allergy exists in the allergens database
        query_allergen_id = "SELECT id FROM allergens WHERE unique_identifier = %s"
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
    except Exception as e:
        print(f"Error: {e}")



def create_occupation(create_clinical_history_and_physical_id, occupation, conn, cursor):
    """
    Function to create an occupation record for a clinical history and physical entry.
    Args:
        create_clinical_history_and_physical_id: ID of the clinical history and physical entry.
        occupation: Name of the occupation (string).
        conn: Database connection object.
        cursor: Database cursor object.
    """
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
                INSERT INTO clinical_history_and_physical_patient_occupations (create_clinical_history_and_physical_id, occupation_id)
                VALUES (%s, %s)
            """
            cursor.execute(query, (create_clinical_history_and_physical_id, occupation_id))
            conn.commit()

            record_id = cursor.lastrowid
            print(f"Occupation record created successfully with ID: {record_id}")
        else:
            # If the occupation does not exist, insert it as a detail
            query = """
                INSERT INTO clinical_history_and_physical_patient_occupations (create_clinical_history_and_physical_id, detail)
                VALUES (%s, %s)
            """
            cursor.execute(query, (create_clinical_history_and_physical_id, occupation))
            conn.commit()

            record_id = cursor.lastrowid
            print(f"Unknown occupation record created successfully with ID: {record_id}")
    except Exception as e:
        print(f"Error: {e}")



def create_pshx(clinical_history_and_physical_id,pshx_value ,conn, cursor ):
    other = pshx_value
    default_value = 12

    query = """
    INSERT INTO clinical_history_and_physical_past_surgical_procedure (clinical_history_and_physical_id, procedure_type_id, other)
    VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(query, (clinical_history_and_physical_id, default_value, other))
    
    # Commit the transaction
        conn.commit()

    # Get the ID of the newly inserted patient
        pshx_id = cursor.lastrowid
        print(f"Admission_form created successfully with ID: {pshx_id}")


    except Error as e:
        print(f"Error: {e}")


def create_pmhx(clinical_history_and_physical_id, PMHX, conn, cursor):
    pmhx_option_id = 87
    other_value = PMHX

    query = """
    INSERT INTO clinical_history_and_physical_admission_pmhx_options (clinical_history_and_physical_id, pmhx_option_id,other)
    VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(query, (clinical_history_and_physical_id, pmhx_option_id, other_value))
    
    # Commit the transaction
        conn.commit()

    # Get the ID of the newly inserted patient
        clinical_history_and_physical_admission_pmhx_options_id = cursor.lastrowid
        print(f"Admission_form created successfully with ID: {clinical_history_and_physical_admission_pmhx_options_id}")


    except Error as e:
        print(f"Error: {e}")


def create_contraception(clinical_history_and_physical_id, contraception, conn, cursor):
    """
    Function to create a contraception record for a clinical history and physical entry.
    Args:
        clinical_history_and_physical_id: ID of the clinical history and physical entry.
        contraception: Name of the contraception method (string).
        conn: Database connection object.
        cursor: Database cursor object.
    """
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
                INSERT INTO clinical_history_and_physical_patient_contraception (clinical_history_and_physical_id, contraception_method_id)
                VALUES (%s, %s)
            """
            cursor.execute(query, (clinical_history_and_physical_id, contraception_method_id))
            conn.commit()

            record_id = cursor.lastrowid
            print(f"Contraception record created successfully with ID: {record_id}")
        else:
            # If the contraception method does not exist, insert it as a detail
            query = """
                INSERT INTO clinical_history_and_physical_patient_contraception (clinical_history_and_physical_id, detail)
                VALUES (%s, %s)
            """
            cursor.execute(query, (clinical_history_and_physical_id, contraception))
            conn.commit()

            record_id = cursor.lastrowid
            print(f"Unknown contraception method record created successfully with ID: {record_id}")
    except Exception as e:
        print(f"Error: {e}")


def create_gtpals(clinical_history_and_physical_id, G, T, P, A, L, description,  conn, cursor): 
    query = """
    INSERT INTO clinical_history_and_physical_patient_contraception (clinical_history_and_physical_id, gravida, term, preterm, abortions, living_children, description)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (clinical_history_and_physical_id, G, T, P, A, L, description))
    
         # Commit the transaction
        conn.commit()

        # Get the ID of the newly inserted patient
        clinical_history_and_physical_patient_occupations_id = cursor.lastrowid
        print(f"Admission_form created successfully with ID: {clinical_history_and_physical_patient_occupations_id}")
        
    except Error as e:
        print(f"Error: {e}")



def get_sdpr_patient_id(patient_unique_id,  cursor):# no need for conn, no commit required

    try:
        # Query to get the sdpr_patient_id
        query_patient_id = "SELECT id FROM sdpr_patient WHERE unique_identifier = %s"  # Adjust column name
        cursor.execute(query_patient_id, (patient_unique_id,))
        result = cursor.fetchone()

        if result:
            sdpr_patient_id = result[0]
            return sdpr_patient_id
        else:
            print("Error: Patient record not found.")
            return None
    except Error as e:
        print(f"Error while fetching sdpr_patient_id: {e}")
        return None

def create_socialhx(created_at, updated_at, sdpr_patient_id ,social_hx, conn, cursor):# This social_hx would be the data from stapletons files. ///// When sorted, duplicate the code for the other family_hx options.
    cancelled = 0
    other = social_hx # This would have to be that data from stapletons files.
    admission_form_option_id = 11
    query = """
    INSERT INTO spdr_patient_admission_form_options (sdpr_patient_id,  admission_form_option_id, other, cancelled, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (sdpr_patient_id,  admission_form_option_id, other, cancelled, created_at, updated_at))
    
         # Commit the transaction
        conn.commit()

        # Get the ID of the newly inserted patient
        socialhx_id = cursor.lastrowid
        print(f"Admission_form created successfully with ID: {socialhx_id}")
        
    except Error as e:
        print(f"Error: {e}")


def create_familyhx(created_at, updated_at, sdpr_patient_id ,family_hx, conn, cursor):# This family_hx would be the data from stapletons files. 
    cancelled = 0
    other = family_hx # This would have to be that data from stapletons files.
    admission_form_option_id = 14
    query = """
    INSERT INTO spdr_patient_admission_form_options (sdpr_patient_id,  admission_form_option_id, other, cancelled, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (sdpr_patient_id,  admission_form_option_id, other, cancelled, created_at, updated_at))
    
         # Commit the transaction
        conn.commit()

        # Get the ID of the newly inserted patient
        familyhx_id = cursor.lastrowid
        print(f"Admission_form created successfully with ID: {familyhx_id}")
        
    except Error as e:
        print(f"Error: {e}")


def create_past_gyne_surg(patient_id,created_at,updated_at ,prev_gyn_surg, conn, cursor):
    procedure_type_id = 1041
    procedure_catagory_id = 29
    cancelled = 0
    other = prev_gyn_surg
    start_date = created_at# Returns a formatted time string
    end_date = created_at# Returns a formatted time string

    # first the procedure gets added to the database.
    query = """
    INSERT INTO procedures (patient_id, start_date ,end_date ,procedure_type_id, procedure_catagory_id,  other, cancelled, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (patient_id, start_date ,end_date ,procedure_type_id,procedure_catagory_id,  other,  cancelled, created_at, updated_at))
    
         # Commit the transaction
        conn.commit()

        # Get the ID of the newly inserted patient
        procedure_id = cursor.lastrowid
        print(f"Admission_form created successfully with ID: {procedure_id}")
        return procedure_id
        
    except Error as e:
        print(f"Error: {e}")
   
    
    drains = 0
    unscheduled_return = 0
    incomplete = 0
    query = """
    INSERT INTO surgeries (procedure_id,created_at,updated_at,drains,cancelled, unscheduled_return,incomplete)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (procedure_id,created_at,updated_at,drains,cancelled, unscheduled_return,incomplete))
    
         # Commit the transaction
        conn.commit()

        # Get the ID of the newly inserted patient
        surgery_id = cursor.lastrowid
        print(f"Admission_form created successfully with ID: {surgery_id}")
        
        
    except Error as e:
        print(f"Error: {e}")

    
def create_rxhx(patient_id, drug_name,start_date,end_date,is_surgical_prophylaxis,created_at,updated_at,mark, conn, cursor):# this still has to be worked on , reppurosed database check function
    mark = 0
    is_surgical_prophylaxis = 0
    """
    Fetches the drugs for a given unique patient identifier.
    
    Args:
        patient_unique_id (str): The unique identifier for the patient (e.g., name, patient ID).
    
    Returns:
        int: The sdpr_patient_id if found, or None if the patient does not exist.
    """
    try:
        # Query to check the drugfrom the pms , if its in the database.
        query_drug_id = "SELECT id FROM drugs WHERE unique_identifier = %s"  # Adjust column name
        cursor.execute(query_drug_id, (drug_name,))
        result = cursor.fetchone()



        if result:
            drug_id = result[0]
            query = """
            INSERT INTO patient_drugs (patient_id,drug_id,start_date,end_date,is_surgical_prophylaxis,created_at,updated_at,mark)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            try:
                cursor.execute(query, (patient_id,drug_id,start_date,end_date,is_surgical_prophylaxis,created_at,updated_at,mark))
    
                # Commit the transaction
                conn.commit()

                # Get the ID of the newly inserted patient
                surgery_id = cursor.lastrowid
                print(f"Admission_form created successfully with ID: {surgery_id}")
        
        
            except Error as e:
                print(f"Error: {e}")


        elif not result:
            drug_id = 4397
            query = """
            INSERT INTO patient_drugs (patient_id,drug_id,start_date,end_date,is_surgical_prophylaxis,created_at,updated_at,mark)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            try:
                cursor.execute(query, (patient_id,drug_id,start_date,end_date,is_surgical_prophylaxis,created_at,updated_at,mark))
    
                # Commit the transaction
                conn.commit()

                # Get the ID of the newly inserted patient
                surgery_id = cursor.lastrowid
                print(f"Admission_form created successfully with ID: {surgery_id}")
        
        
            except Error as e:
                print("Error: Patient record not found.")

        else:
            print("Error: Patient record not found.")
            return None
        
    except Error as e:
        print(f"Error while fetching sdpr_patient_id: {e}")
        

#create patient done --> create Admission_form --> create clinical_history_and_physical_id --> continue normal flow.
#separate the extraction of id's (patient_id/clinical_history_and_physical_id, admission_di) 

#Theres still more to do, but untill i figure it out, lemme work on how the the PROCESS works.

file_path = None #this will be stapletons export file.

def importing_data_from_stapleton_file(user_id,file_path):
    # Open the CSV file
    with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
    
        # Loop through each row in the CSV
        for row_number, row in enumerate(csv_reader, start=1):
            

            title = row['Title']
            name_last = row['Name Last']
            name_first = row['Name First']
            id_number = row['ID'] ######### When creating the export try to merge in the id number - this is required for the patient table.
            dob = row['DOB'] ###### When creating the export try to merge in the DOB  - this is required for the patient table.
            gender = row['Gender'] ###### When creating the export try to merge in the gender - this is required for the patient table.
            contraception = row['Contraception'] ######## when creating the export try to merge in the Contraception - this is required for the Contraception table.
            partner = row['partner']
            referral = row['Referral']
            med_aid = row['Med.Aid']
            folder_number = row['Folder #']
            salutation = row['Salutation']
            age_calc = row['Age calc']
            lmp = row['LMP:']
            occupation = row['Occupation']
            allergies = row['Allergies']
            social_hx = row['SocialHx:']
            family_hx = row['FamilyHx:']
            pmhx = row['PMHx']
            pshx = row['PSHx']
            rxhx = row['RxHx']
            problem_list = row['Problem list']
            confidential = row['Confidential']
            g = row['G']
            t = row['T']
            p = row['P']
            a = row['A']
            l = row['L']
            births = row['births'] # GTPALs description
            prev_gyn_surg = row['prev. gyn surg.']
            problem_1 = row['Problem 1']
            hx_problem = row['Hx problem']
            temp = row['Temp']
            pulse = row['Pulse']
            bp = row['B.P.']
            waist_circ = row['WaistCirc']
            weight = row['Weight']
            height = row['Height']
            bmi = row['BMI']
            general_exam = row['General exam.']
            investigations = row['Investigations']
            ultrasound = row['ultrasound']
            assessment = row['Assessment:']
            plan = row['Plan']
            dr_name = row['Dr name']


            #time modification to the normal format

            current_time = datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

            created_at = formatted_time
            updated_at = formatted_time

            merged = row['merged']
            organisation_id = "1" #######, organisation id hard coded for now, for this one use case.
            canonical = "1"



            #These store ID's that would be used in the other tables.
            # Create the patient record and store the patient_id
            patient_id = create_patient(folder_number,id_number,name_first,name_last,title,dob,gender,created_at,updated_at,merged,organisation_id,canonical)

            # Create the admission_form record and store the admission_form_id
            admission_form_id = create_admission_forms(patient_id,created_at,updated_at)

            # Create the clinical_history_and_physical_id record and store the clinical_history_and_physical_id
            clinical_history_and_physical_id = create_clinical_history_and_physical(patient_id,admission_form_id,user_id)


            # Creates the ongoing_problems record
            create_ongoing_problems(clinical_history_and_physical_id, problem_list)

            # Creates the allergies record
            create_allergies(patient_id ,allergies, allergens_dict)

            # Creates the Occupation record
            create_occupation(clinical_history_and_physical_id, occupation, )

            # Creates the pmhx record
            create_pmhx(clinical_history_and_physical_id, pmhx)

            # Creates the Contraception record
            create_contraception(clinical_history_and_physical_id, contraception,)
            
            # Creates the GTPALS records
            create_gtpals(clinical_history_and_physical_id, g, t, p, a, l, births)

            # Creates pshx record
            create_pshx(clinical_history_and_physical_id,pshx )

            # Creates the sdpr_patient_id value for social_hx and Family Hx
            sdpr_patient_id = get_sdpr_patient_id(id_number)

            # Creates the social_hx record
            create_socialhx(created_at, updated_at, sdpr_patient_id ,social_hx)

            # Creates the family_hx record
            create_familyhx(created_at, updated_at, sdpr_patient_id ,family_hx)

            # Creates the past gyne surg record
            create_past_gyne_surg(patient_id,created_at,updated_at ,prev_gyn_surg )

            create_rxhx(patient_id, rxhx,created_at ,updated_at)

# Down here, you want to create a make it run, the connection to the database and the tables. then between you are gonna want to add the importing patient data function.


def Main_function():
    conn = None  # Declare the connection object
    cursor = None  # Declare the cursor object
    file_path = "Test.csv"
    # Create the database connection
    try:
        # Establish the database connection
        conn = mysql.connector.connect(
            host='your_host',
            database='your_db',
            user='your_user',
            password='your_password'
        )
        
        # Initialize the cursor
        cursor = conn.cursor() 
        importing_data_from_stapleton_file(file_path, conn, cursor)

    except Error as e:
        print(f"Error to connect to MySQL database")

    finally:
        # Close the cursor and the connection
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
        print("Database connection closed.")










########### Now that all is done we should be able to run the main function
Main_function()
















