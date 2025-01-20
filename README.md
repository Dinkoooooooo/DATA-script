# DATA-script
For Importing,pms data to bb 

1. Ensure Required Dependencies
Install mysql-connector-python if not already installed:

`pip install mysql-connector-python`

Ensure you have Python installed and properly configured.

2. Set Up the Environment

Ensure that the Test.csv file exists in the directory where the script is executed or update file_path in Main_function with the correct absolute path.

3. Provide Database Connection Details
   
Replace the placeholders in the database connection (host, database, user, password) in the Main_function with the correct credentials for your MySQL database.

# BreakDown

1.`create_patient`
Purpose: Inserts a new patient record into the patients table.

Parameters:

Patient details such as Folder_number, Id_number, First_name, last_name, etc.

conn (database connection) and cursor (to execute the query).

Returns: The patient_id of the newly inserted patient.

Usage: Called during data import to create a patient record in the database.

2. `create_admission_forms`
Purpose: Inserts a new admission form record into the admission_forms table.
Parameters:
patient_id: The ID of the patient this admission form is linked to.
created_at, updated_at: Timestamps for when the record is created/updated.
conn and cursor.
Returns: The admission_form_id of the newly inserted admission form.

3. `create_clinical_history_and_physical`
Purpose: Inserts a record into the clinical_history_and_physicals table.
Parameters:
user_id: ID of the user creating the record (currently hardcoded as 12345).
patient_id, admission_form_id: Links the record to the patient and admission form.
conn and cursor.
Returns: The clinical_history_and_physical_id.

4. `create_ongoing_problems`
Purpose: Inserts a record into the clinical_history_and_physical_patient_ongoing_problems table.
Parameters:
clinical_history_and_physical_id: Links to the clinical history and physical record.
Problem_list: List of ongoing problems for the patient.
conn and cursor.
Returns: None.

5. `create_allergies`
Purpose: Inserts allergy records for a patient into the allergies table.
Parameters:
patient_id: Links the allergy to the patient.
Allergies: Allergy details.
allergens_dict: A dictionary mapping allergen IDs to allergen names.
conn and cursor.
Returns: None.

6. `create_occupation`
Purpose: Inserts the patient’s occupation into the clinical_history_and_physical_patient_occupations table.
Parameters:
create_clinical_history_and_physical_id: Links the occupation to the clinical history and physical record.
Occupation: The patient’s occupation.
occupations_dict: A dictionary mapping occupation IDs to names.
conn and cursor.
Returns: None.

7. `create_pshx`
Purpose: Inserts past surgical history (PSHx) into the clinical_history_and_physical_past_surgical_procedure table.
Parameters:
clinical_history_and_physical_id: Links to the clinical history and physical record.
pshx_value: Description of the surgical procedure.
conn and cursor.
Returns: None.

8. `create_pmhx`
Purpose: Inserts past medical history (PMHx) into the clinical_history_and_physical_admission_pmhx_options table.
Parameters:
clinical_history_and_physical_id: Links to the clinical history and physical record.
PMHX: Details of the past medical history.
conn and cursor.
Returns: None.

9. `create_contraception`
Purpose: Inserts contraception information into the clinical_history_and_physical_patient_contraception table.
Parameters:
clinical_history_and_physical_id: Links to the clinical history and physical record.
contraception: The contraception method used by the patient.
contraception_disc: Dictionary mapping contraception method IDs to names.
conn and cursor.
Returns: None.

10. `create_gtpals`
Purpose: Inserts GTPAL (Gravida, Term, Preterm, Abortions, Living children) data into the database.
Parameters:
clinical_history_and_physical_id: Links to the clinical history and physical record.
G, T, P, A, L, description: Details of the patient’s obstetric history.
conn and cursor.
Returns: None.

11. `get_sdpr_patient_id`
Purpose: Retrieves the sdpr_patient_id for a patient based on a unique identifier.
Parameters:
patient_unique_id: A unique identifier (e.g., name, ID).
conn and cursor.
Returns: The sdpr_patient_id if found, otherwise None.

12. `create_socialhx`
Purpose: Inserts social history into the spdr_patient_admission_form_options table.
Parameters:
sdpr_patient_id: Links to the patient.
social_hx: Details of the patient’s social history.
conn and cursor.
Returns: None.

13. `create_familyhx`
Purpose: Inserts family history into the spdr_patient_admission_form_options table.
Parameters:
sdpr_patient_id: Links to the patient.
family_hx: Details of the patient’s family history.
conn and cursor.
Returns: None.

14. `create_past_gyne_surg`
Purpose: Inserts gynecological surgical history into the procedures and surgeries tables.
Parameters:
patient_id: Links to the patient.
prev_gyn_surg: Details of the gynecological procedure.
conn and cursor.
Returns: The procedure_id if successful.

15. `create_rxhx`
Purpose: Inserts prescription history (RxHx) into the patient_drugs table.
Parameters:
patient_id: Links to the patient.
drug_name, start_date, end_date: Prescription details.
conn and cursor.
Returns: None.

16. `importing_data_from_stapleton_file`
Purpose: Reads a CSV file, extracts data row by row, and calls the above functions to insert the data into the database.
Parameters:
file_path: Path to the CSV file.
conn and cursor.
Returns: None.

17. `Main_function`
Purpose: Establishes the database connection and initializes the import process.
Steps:
Connects to the MySQL database.
Calls importing_data_from_stapleton_file.
Closes the database connection.
Parameters: None.
