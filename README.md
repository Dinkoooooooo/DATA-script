# DATA-script
For Importing,pms data to bb 

`User_id is added with a command line argument` so `python process_user_id.py "12345"`


1. Ensure Required Dependencies
Install mysql-connector-python if not already installed:

`pip install mysql-connector-python`

Ensure you have Python installed and properly configured.

2. Set Up the Environment

Ensure that the Test.csv file exists in the directory where the script is executed or update `file_path` in `Main_function` with the correct absolute path.

3. Provide Database Connection Details
   
Replace the placeholders in the database connection (host, database, user, password) in the `Main_function` with the correct credentials for your `MySQL database`.

# BreakDown

1. `create_patient`

How it works:

This function builds an INSERT SQL query to add a new patient record into the patients table.
It uses the cursor.execute() method to execute the query with provided field values (e.g., Folder_number, Id_number, etc.).

After executing the query, cursor.lastrowid fetches the patient_id of the newly inserted record for further use.
Error Handling: Catches database errors and prints them.

3. `create_admission_forms`

How it works:

It constructs an INSERT query for the admission_forms table, linking the patient_id to the admission form.

The created_at and updated_at timestamps are included to track when the record was created and last updated.
After insertion, it retrieves the admission_form_id via cursor.lastrowid.

4. `create_clinical_history_and_physical`

How it works:

This function generates an INSERT query for the clinical_history_and_physicals table.

Key fields like user_id, patient_id, and admission_form_id establish relationships with other records.
It sets defaults (e.g., signed_off is 0, note_catagory_id is 6).
After execution, it retrieves the new clinical_history_and_physical_id.

5. `create_ongoing_problems`

How it works:

The function inserts a record into clinical_history_and_physical_patient_ongoing_problems, linking the clinical_history_and_physical_id to a Problem_list.

This ensures ongoing problems are associated with the relevant clinical history.

6. `create_allergies`

How it works:

First, the function checks if the allergy exists in the allergens table by querying with unique_identifier.

If found, it inserts the allergen_id into the allergies table.
If not found, it inserts the allergy into the allergies table as an "unknown allergen" using a default ID (failed_allergen_id).
Ensures proper linkage to the patient_id.

7. `create_occupation`

How it works:

It first queries the occupations table to check if the occupation already exists.

If found, it associates the occupation_id with clinical_history_and_physical_patient_occupations.
If not found, it inserts the occupation as a detail instead.
This ensures all occupations, known or unknown, are captured.

8. `create_pshx`

How it works:

The function inserts past surgical history into the clinical_history_and_physical_past_surgical_procedure table.

It uses a default procedure_type_id and appends the provided other field for additional details.

9. `create_pmhx`

How it works:

Past medical history is recorded by linking the clinical_history_and_physical_id with a default pmhx_option_id.

Additional information is stored in the other field.

10. `create_contraception`

How it works:

It queries the contraception_methods table to check if the provided method exists.

If found, it links the contraception_method_id to the clinical history.
If not, it stores the method as a detail in the same table.

11. `create_gtpals`

How it works:

GTPAL (Gravida, Term, Preterm, Abortions, Living children) data is inserted directly into the clinical_history_and_physical_patient_contraception table.

This provides a structured record of obstetric history, including an optional description.

12. `get_sdpr_patient_id`

How it works:

The function queries the sdpr_patient table using a unique_identifier.

If a matching record exists, it fetches the id of the patient for use in related functions.

13. `create_socialhx`

How it works:

Social history data is inserted into spdr_patient_admission_form_options using a specific admission_form_option_id (11 for social history).

The function ensures proper linkage via sdpr_patient_id.

14. `create_familyhx`

How it works:

Similar to create_socialhx, but uses an admission_form_option_id of 14 for family history.

Stores additional information in the other field.

15. `create_past_gyne_surg`

How it works:

This function performs a two-step process:

Inserts surgical data into the procedures table (e.g., start_date, procedure_type_id).
Uses the resulting procedure_id to insert data into the surgeries table, capturing further details (e.g., drains, cancelled).

16. `create_rxhx`

How it works:

Checks if the drug exists in the drugs table using unique_identifier.

If found, it adds the drug_id to patient_drugs for the specified patient.
If not, it uses a default drug_id to log unknown drugs.
Captures additional fields like start_date, end_date, and whether it is for surgical prophylaxis.

17. `Main_function`
Purpose:

Serves as the entry point for the script. It establishes the database connection, initializes the cursor, and invokes importing_data_from_stapleton_file.

How it works:

Attempts to connect to the MySQL database using the mysql.connector.connect() method with the provided credentials (host, database, user, password).

If the connection is successful:

Initializes the cursor for executing SQL queries.

Calls importing_data_from_stapleton_file with the database connection (conn) and cursor as arguments.

After the file processing completes, it closes the cursor and the database connection, ensuring resources are properly released.
Implements a try-finally block for error handling and cleanup.

18. `importing_data_from_stapleton_file`
Purpose:
Processes patient data from a CSV file (specified by file_path), creates records in various tables, and maintains relationships between the records.
How it works:

1.Opens the CSV File:

Reads the CSV using Python's csv.DictReader, which treats the first row as headers and parses subsequent rows into dictionaries.

2.Loops Through Each Row:

Extracts values from the CSV (e.g., title, dob, gender) and formats them for database insertion.
Generates created_at and updated_at timestamps using datetime.now().

3.Calls Record-Creation Functions in Sequence:

Patient: Calls create_patient to insert a new patient and retrieve the patient_id.
Admission Form: Calls create_admission_forms using the patient_id.
Clinical History and Physical: Calls create_clinical_history_and_physical to create a record tied to the patient and admission form, retrieving the clinical_history_and_physical_id.

4.Additional Records:

Calls various functions (e.g., create_allergies, create_occupation, create_socialhx) to insert related data like allergies, occupation, and family history.
Handles Relationships:
Functions like get_sdpr_patient_id ensure data is correctly linked by fetching IDs from other tables (e.g., sdpr_patient).

5.Error Handling:
Includes safeguards in each function to handle database errors gracefully and print diagnostic messages.
