# Reads the CSV file for stapleton , then loops through each row of the csv file, the following would be done to each of the rows.
# Note , connect to the database before running the loop. and disconnect after.

# The reson cursor and con arent defined is because they would need to defined before the functions are called, so before the loop would start.

import csv
import mysql.connector
from mysql.connector import Error
import datetime


#Create_patient()# save id
#Create_vist()# None.
#Create_admissionn_note()# save id

def create_patient(Folder_number,Id_number,First_name,last_name,title,dob,Gender,created_at,updated_at,merged,organisation_id,canonical):#open connection before, or after this runs, check with mike.
    query = """
        INSERT INTO patients (Folder_number, Id_number, First_name, last_name, title, dob, Gender, created_at, updated_at, merged, organisation_id, canonical)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
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

def create_admission_forms(patient_id,created_at,updated_at):

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



def create_clinical_history_and_physical(user_id, patient_id,admission_form_id):
    user_id = 12345 ############################################################# Update user_id with the correct one mike gives.
    signed_off = 0
    time_for_import = datetime.now()
    recorded_at = time_for_import
    created_at = time_for_import
    updated_at = time_for_import
    note_catagory_id = 6

    created_at = datetime.now()
    updated_at = datetime.now()

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



def create_ongoing_problems(clinical_history_and_physical_id,Problem_list ):
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

def create_allergies(patient_id ,Allergies, allergens_dict): 

    Allergies = allergy

    allergy = allergy.strip().lower() #Normalise the input

    # Iterate over the dictionary to find the allergen ID
    for allergen, allergen_id in allergens_dict.items():
        if allergen.lower() == allergy:#if Found the allergen
            #Allergen id can be used,
            recorded_at = datetime.now()
            start_date = datetime.now()
            
            
            query = """
            INSERT INTO allergies (patient_id, allergen_id, recorded_at, start_date)
            VALUES (%s, %s, %s, %s)
            """
            try:
                cursor.execute(query, (patient_id, allergen_id, recorded_at, start_date))
    
                 # Commit the transaction
                conn.commit()

                # Get the ID of the newly inserted patient
                Allergies_id = cursor.lastrowid
                print(f"Admission_form created successfully with ID: {Allergies_id}")
        
            except Error as e:
                print(f"Error: {e}")
        
    query = """
            INSERT INTO allergies (patient_id, allergen_id, other, recorded_at, start_date)
            VALUES (%s, %s, %s, %s)
            """
    Failed_allergen_id = 9
    try:
        cursor.execute(query, (patient_id, Failed_allergen_id, allergy,recorded_at, start_date))
    
         # Commit the transaction
        conn.commit()

        # Get the ID of the newly inserted patient
        Allergies_id = cursor.lastrowid
        print(f"Admission_form created successfully with ID: {Allergies_id}")
        
    except Error as e:
        print(f"Error: {e}")


# For OCCUPATION

occupations_dict = {
    1: "Actor",
    2: "Baker",
    3: "Butcher",
    4: "Carpenter",
    5: "Cook",
    6: "Doctor",
    7: "Engineer",
    8: "Farmer",
    9: "Fireman",
    10: "Fisherman",
    11: "Gardener",
    12: "Goldsmith",
    13: "Hairdresser",
    14: "Journalist",
    15: "Judge",
    16: "Lawyer",
    17: "Mason",
    18: "Mechanic",
    19: "Nurse",
    20: "Painter",
    21: "Pilot",
    22: "Plumber",
    23: "Policeman",
    24: "Postman",
    25: "Secretary",
    26: "Shoe-Shine Boy",
    27: "Singer",
    28: "Soldier",
    29: "Tailor",
    30: "Taxi Driver",
    31: "Teacher",
    32: "Waiter",
    33: "Accountant",
    34: "Bank Clerk",
    35: "Clerical",
    36: "Estate Agent",
    37: "Fashion",
    38: "Flight Attendant",
    39: "Graphic Artist",
    40: "Hairstylist",
    41: "Housewife",
    42: "Marketing",
    43: "Model",
    44: "Own Business",
    45: "Personal Assistant",
    46: "Public Relations",
    47: "Receptionist",
    48: "Retired",
    49: "Social Worker",
    50: "Student",
    51: "Travel Consultant",
    52: "Scientist",
    53: "Physiotherapist",
    54: "Medical Practitioner",
    55: "Actuary",
    56: "Business Executive",
    57: "Police",
    58: "Firefighter",
    59: "Unemployed",
    60: "Translator",
    61: "Restauranteur",
    62: "Packer",
    63: "Salesperson",
    64: "Tour Guide",
    65: "Copywriter (Advertising)",
    66: "Chef",
    67: "Hotelier",
    68: "Electrician",
    69: "Bookkeeper"
}

def create_occupation(create_clinical_history_and_physical_id, Occupation, occupations_dict):

    # Search for a match in the occupations_dict
    for occupation_id, occupation_name in occupations_dict.items():
        if Occupation.strip().lower() == occupation_name.lower():
             # occupation_id Ready to be used.
            query = """
            INSERT INTO clinical_history_and_physical_patient_occupations (create_clinical_history_and_physical_id, occupation_id)
            VALUES (%s, %s)
            """
            try:
                cursor.execute(query, (create_clinical_history_and_physical_id, occupation_id))
    
                 # Commit the transaction
                conn.commit()

                # Get the ID of the newly inserted patient
                clinical_history_and_physical_patient_occupations_id = cursor.lastrowid
                print(f"Admission_form created successfully with ID: {clinical_history_and_physical_patient_occupations_id}")
        
            except Error as e:
                print(f"Error: {e}")
            
    
    # If no match is found, return empty ID and unmatched value in details
    query = """
    INSERT INTO clinical_history_and_physical_patient_occupations (create_clinical_history_and_physical_id, detail)
    VALUES (%s, %s)
    """
    try:
        cursor.execute(query, (create_clinical_history_and_physical_id, Occupation))
    
         # Commit the transaction
        conn.commit()

        # Get the ID of the newly inserted patient
        clinical_history_and_physical_patient_occupations_id = cursor.lastrowid
        print(f"Admission_form created successfully with ID: {clinical_history_and_physical_patient_occupations_id}")
        
    except Error as e:
        print(f"Error: {e}")

def create_pshx(clinical_history_and_physical_id,pshx_value ):
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


def create_pmhx(clinical_history_and_physical_id, PMHX):
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



contraception_dict = {
    1: "Caps",
    2: "Combined pill",
    3: "Condoms (female)",
    4: "Condoms (male)",
    5: "Contraceptive Implant" ,
    6: "Contraceptive Injection" ,
    7: "Contraceptive Patch",
    8: "Diaphragms",
    9: "Intrauterine Device (IUD)",
    10: "Intrauterine System (IUD)",
    11: "Natural Family Planning",
    12: "Progestogen-only Pill",
    13: "Vaginal Ring",
    14: "Nil"
}


def create_contraception(clinical_history_and_physical_id, contraception, contraception_disc):######Create contraception_disc

    # Search for a match in the occupations_dict
    for contaception_method_id, contraception_name in contraception_dict.items():
        if contraception.strip().lower() == contraception_name.lower():
             # occupation_id Ready to be used.
            query = """
            INSERT INTO clinical_history_and_physical_patient_contraception (clinical_history_and_physical_id, occupation_id)
            VALUES (%s, %s)
            """
            try:
                cursor.execute(query, (clinical_history_and_physical_id, occupation_id))
    
                 # Commit the transaction
                conn.commit()

                # Get the ID of the newly inserted patient
                clinical_history_and_physical_patient_occupations_id = cursor.lastrowid
                print(f"Admission_form created successfully with ID: {clinical_history_and_physical_patient_occupations_id}")
        
            except Error as e:
                print(f"Error: {e}")
            
    
    # If no match is found, return empty ID and unmatched value in details
    query = """
    INSERT INTO clinical_history_and_physical_patient_contraception (create_clinical_history_and_physical_id, detail)
    VALUES (%s, %s)
    """
    try:
        cursor.execute(query, (clinical_history_and_physical_id, contraception))
    
         # Commit the transaction
        conn.commit()

        # Get the ID of the newly inserted patient
        clinical_history_and_physical_patient_occupations_id = cursor.lastrowid
        print(f"Admission_form created successfully with ID: {clinical_history_and_physical_patient_occupations_id}")
        
    except Error as e:
        print(f"Error: {e}")


def create_gtpals(clinical_history_and_physical_id, G, T, P, A, L, description): 
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



def get_sdpr_patient_id(patient_unique_id):
    """
    Fetches the sdpr_patient_id for a given unique patient identifier.
    
    Args:
        patient_unique_id (str): The unique identifier for the patient (e.g., name, patient ID).
    
    Returns:
        int: The sdpr_patient_id if found, or None if the patient does not exist.
    """
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

def create_socialhx(created_at, updated_at, sdpr_patient_id ,social_hx):# This social_hx would be the data from stapletons files. ///// When sorted, duplicate the code for the other family_hx options.
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


def create_familyhx(created_at, updated_at, sdpr_patient_id ,family_hx):# This family_hx would be the data from stapletons files. 
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


def create_past_gyne_surg(patient_id,created_at,updated_at ,prev_gyn_surg ):
    procedure_type_id = 1041
    procedure_catagory_id = 29
    cancelled = 0
    other = prev_gyn_surg
    start_date = datetime.now()
    end_date = datetime.now()

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

    

    









    
def create_rxhx(patient_id, drug_name,start_date,end_date,is_surgical_prophylaxis,created_at,updated_at,mark):# this still has to be worked on , reppurosed database check function
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
            drug_id = result
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
        return None












#create patient done --> create Admission_form --> create clinical_history_and_physical_id --> continue normal flow.
#separate the extraction of id's (patient_id/clinical_history_and_physical_id, admission_di) 

#Theres still more to do, but untill i figure it out, lemme work on how the the PROCESS works.

file_path = None #this will be stapletons export file.

def importing_data_from_stapleton_file(file_path):
    # Open the CSV file
    with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
    
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
            created_at = datetime.now()
            updated_at = datetime.now()

            merged = row['merged']
            organisation_id = "1" #######, organisation id hard coded for now, for this one use case.
            canonical = "1"



            #These store ID's that would be used in the other tables.
            # Create the patient record and store the patient_id
            patient_id = create_patient(folder_number,id_number,name_first,name_last,title,dob,gender,created_at,updated_at,merged,organisation_id,canonical)

            # Create the admission_form record and store the admission_form_id
            admission_form_id = create_admission_forms(patient_id,created_at,updated_at)

            # Create the clinical_history_and_physical_id record and store the clinical_history_and_physical_id
            clinical_history_and_physical_id = create_clinical_history_and_physical(patient_id,admission_form_id)


            # Creates the ongoing_problems record
            create_ongoing_problems(clinical_history_and_physical_id, problem_list)

            # Creates the allergies record
            create_allergies(patient_id ,allergies, allergens_dict)

            # Creates the Occupation record
            create_occupation(clinical_history_and_physical_id, occupation, occupations_dict)

            # Creates the pmhx record
            create_pmhx(clinical_history_and_physical_id, pmhx)

            # Creates the Contraception record
            create_contraception(clinical_history_and_physical_id, contraception, contraception_dict)
            
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

















