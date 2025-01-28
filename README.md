# DATA-script
For Importing,pms data to bb 

#Note, need to update sql server details when used.

`User_id is added with a command line argument` so 

Command line:

`python process_user_id.py 12345`

/# On another note . fields below carry values above 255 char, so columns would need to be updated to handle the fields.

`clinical_history_and_physical_past_surgical_procedures:other` ,

`clinical_history_and_physical_patient_ongoing_problems:name`, 

`clinical_history_and_physical_admission_pmhx_options:other`

/# Another note, 

These fields have been modified to split the text field with (/v), and add a record for each split section of the text. Also ignoring blank sections created by the split.

`create_clinical_history_and_physical_past_surgical_procedures `

`create_pmhx`

`create_ongoing_problems`

`create_rxhx`

`create_familyhx`

`create_socialhx`


# The Conglomerate.py

Script facilitates importing data from a CSV file into a MySQL database. The script processes each row of the CSV to insert records into multiple database tables, ensuring data consistency and logging operations.

1. Ensure Required Dependencies
Install mysql-connector-python if not already installed:

`pip install mysql-connector-python`

Ensure you have Python installed and properly configured.

2. Set Up the Environment

Ensure that the Test.csv file exists in the directory where the script is executed or update `file_path` in `Main_function` with the correct absolute path.

3. Provide Database Connection Details
   
Replace the placeholders in the database connection (host, database, user, password) in the `Main_function` with the correct credentials for your `MySQL database`.

# CSV File Format

The CSV file must include the following headers. Each column corresponds to a field in the database and is used by specific functions in the code.

| **Header**        | **Used In Function**                       | **Purpose**                                                                 |
|--------------------|--------------------------------------------|-----------------------------------------------------------------------------|
| `Title`           | `create_patient`                          | Used for the `title` field in the `patients` table.                        |
| `Name Last`       | `create_patient`                          | Maps to `last_name` in the `patients` table.                               |
| `Name First`      | `create_patient`                          | Maps to `First_name` in the `patients` table.                              |
| `ID`              | `create_patient`, `get_sdpr_patient_id`   | Used as `Id_number` for `patients` and `unique_identifier` for `sdpr_patient`. |
| `DOB`             | `create_patient`                          | Used for the `dob` field in the `patients` table.                          |
| `Gender`          | `create_patient`                          | Used for the `Gender` field in the `patients` table.                       |
| `Contraception`   | `create_contraception`                    | Maps to `contraception` for contraception methods.                         |
| `Occupation`      | `create_occupation`                       | Maps to `occupation` for the `clinical_history_and_physical_patient_occupations` table. |
| `Allergies`       | `create_allergies`                        | Contains allergy data to be linked with `allergens`.                       |
| `SocialHx`       | `create_socialhx`                         | Maps to `social_hx` for social history records.                            |
| `FamilyHx`       | `create_familyhx`                         | Maps to `family_hx` for family history records.                            |
| `PMHx`            | `create_pmhx`                             | Used for past medical history (`other` field in `pmhx_options`).           |
| `PSHx`            | `create_pshx`                             | Maps to surgical history records (`other` field in past surgical procedures). |
| `RxHx`            | `create_rxhx`                             | Used for the `drug_name` field in `patient_drugs`.                         |
| `Problemlist`    | `create_ongoing_problems`                 | Maps to `Problem_list` in ongoing problems.                                |
| `G`               | `create_gtpals`                           | Maps to `gravida` in obstetric history.                                    |
| `T`               | `create_gtpals`                           | Maps to `term` in obstetric history.                                       |
| `P`               | `create_gtpals`                           | Maps to `preterm` in obstetric history.                                    |
| `A`               | `create_gtpals`                           | Maps to `abortions` in obstetric history.                                  |
| `L`               | `create_gtpals`                           | Maps to `living_children` in obstetric history.                            |
| `births`          | `create_gtpals`                           | Maps to the `description` field for obstetric history.                     |
| `prev.gynsurg.` | `create_past_gyne_surg`                   | Used for past gynecological surgeries (`other` field).                     |



# BreakDown

1. `create_patient`

How it works:

This function builds an INSERT SQL query to add a new patient record into the patients table.
It uses the cursor.execute() method to execute the query with provided field values

 (e.g.,Id_number,Folder_number,Id_number,First_name,last_name,title,dob,Gender,created_at,updated_at,merged,organisation_id,canonical).

 Also check if patient already exists, based on folder + org_id + canonical , then uses the last record found and returns the patient id.
if it finds nothing it creates the patient record.

 `dob` - if there is no dob, it defaults to adding "0000/00/00"
       if there is a dob, it strips it leading/trailing whitespace and formats any spacers to "/" and formats date to qa spec.

`Gender` - Converts m/f to 0/1 and unspecified to 2

After executing the query, cursor.lastrowid fetches the patient_id of the newly inserted record for further use.
Error Handling: Catches database errors and prints them.

2. `create_admission_forms`

How it works:

It constructs an INSERT query for the admission_forms table, linking the patient_id to the admission form.

The created_at and updated_at timestamps are included to track when the record was created and last updated.
After insertion, it retrieves the admission_form_id via cursor.lastrowid.

3. `create_clinical_history_and_physical`

How it works:

This function generates an INSERT query for the clinical_history_and_physicals table.

Key fields like user_id, patient_id, and admission_form_id establish relationships with other records.
It sets defaults (e.g., signed_off is 0, note_catagory_id is 6).
After execution, it retrieves the new clinical_history_and_physical_id.

4. `create_ongoing_problems`

How it works:

The function inserts a record into clinical_history_and_physical_patient_ongoing_problems, linking the clinical_history_and_physical_id to a Problem_list.

This ensures ongoing problems are associated with the relevant clinical history.

5. `create_allergies`

How it works:

First, the function checks if the allergy exists in the allergens table by querying with unique_identifier.

If found, it inserts the allergen_id into the allergies table.
If not found, it inserts the allergy into the allergies table as an "unknown allergen" using a default ID (failed_allergen_id).
Ensures proper linkage to the patient_id.

6. `create_occupation`

How it works:

It first queries the occupations table to check if the occupation already exists.

If found, it associates the occupation_id with clinical_history_and_physical_patient_occupations.
If not found, it inserts the occupation as a `detail` instead.
This ensures all occupations, known or unknown, are captured.

7. `create_pshx`

How it works:

The function inserts past surgical history into the clinical_history_and_physical_past_surgical_procedure table.

It uses a default procedure_type_id (12) and appends the provided other field for additional details.

8. `create_pmhx`

How it works:

Past medical history is recorded by linking the clinical_history_and_physical_id with a default pmhx_option_id.

Additional information is stored in the `other` field.

9. `create_contraception`

How it works:

It queries the contraception_methods table to check if the provided method exists.

If found, it links the contraception_method_id to the clinical history.
If not, it stores the method as a detail in the same table.

10. `create_gtpals`

How it works:

GTPAL (Gravida, Term, Preterm, Abortions, Living children) data is inserted directly into the clinical_history_and_physical_patient_contraception table.

Use the fix_gtpal_type() function to convert string to int's.

Also checks if the GTPALS' + description is empty, if empty skips the gtpals record.

This provides a structured record of obstetric history, including an optional description.

11. `get_sdpr_patient_id`

How it works:

The function inserts a sdpr patient into the sdpr_patients table.
links the records with the `patients_id` and adds the `created_at,updated_at` time, which is the time the record is processed.
Then returns the `sdpr_patient_id`, for uses in other functions

12. `create_socialhx`

How it works:

Social history data is inserted into spdr_patient_admission_form_options using a specific admission_form_option_id (11 for social history).

The function ensures proper linkage via sdpr_patient_id.

13. `create_familyhx`

How it works:

Similar to create_socialhx, but uses an admission_form_option_id of 14 for family history.

Stores additional information in the other field.

14. `create_past_gyne_surg`

How it works:

This function performs a two-step process:

Inserts surgical data into the procedures table (e.g., start_date, procedure_type_id).
Uses the resulting procedure_id to insert data into the surgeries table, capturing further details (e.g., drains, cancelled).

15. `create_rxhx`

How it works:

Checks if the drug exists in the drugs table using unique_identifier.

If found, it adds the drug_id to patient_drugs for the specified patient.
If not, it uses a default drug_id to log unknown drugs.
Captures additional fields like start_date, end_date, and whether it is for surgical prophylaxis.

16. `Main_function`
Purpose:

Serves as the entry point for the script. It establishes the database connection, initializes the cursor, and invokes importing_data_from_stapleton_file.

How it works:

Attempts to connect to the MySQL database using the mysql.connector.connect() method with the provided credentials (host, database, user, password).

If the connection is successful:

Initializes the cursor for executing SQL queries.

Calls importing_data_from_stapleton_file with the database connection (conn) and cursor as arguments.

After the file processing completes, it closes the cursor and the database connection, ensuring resources are properly released.
Implements a try-finally block for error handling and cleanup.

17. `importing_data_from_stapleton_file`

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
