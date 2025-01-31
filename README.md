# DATA-script for Importing PMS Data into MySQL Database

This script, `Conglomerate.py`, is designed to import data from a CSV file into a MySQL database. It processes each row of the CSV to insert records into multiple database tables while ensuring data consistency and logging operations. This document outlines the script’s functionality, required setup, and detailed explanations of each function.

---

## Usage
### Command Line Execution
Run the script with the following command:
```bash
python Conglomerate.py <user_id> <csv_file>
```
Here:
- `<user_id>`: The ID of the user performing the import.
- `<csv_file>`: The path to the CSV file containing the data to be imported.

---

## Prerequisites
1. **Dependencies:** Install the required package:
   ```bash
   pip install mysql-connector-python
   ```
2. **Environment:** Ensure the following:
   - Python is installed and configured.
   - The CSV file exists in the directory where the script is executed, or update the file path in `Main_function`.
3. **Database Connection:** Update the database connection details (`host`, `database`, `user`, `password`) in the `Main_function` with your MySQL credentials.

---

## CSV File Format
The CSV file must include the following headers. Each column corresponds to a field in the database and is used by specific functions in the script:

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
| `SocialHx`        | `create_socialhx`                         | Maps to `social_hx` for social history records.                            |
| `FamilyHx`        | `create_familyhx`                         | Maps to `family_hx` for family history records.                            |
| `PMHx`            | `create_pmhx`                             | Used for past medical history (`other` field in `pmhx_options`).           |
| `PSHx`            | `create_pshx`                             | Maps to surgical history records (`other` field in past surgical procedures). |
| `RxHx`            | `create_rxhx`                             | Used for the `drug_name` field in `patient_drugs`.                         |
| `Problemlist`     | `create_ongoing_problems`                 | Maps to `Problem_list` in ongoing problems.                                |
| `G`               | `create_gtpals`                           | Maps to `gravida` in obstetric history.                                    |
| `T`               | `create_gtpals`                           | Maps to `term` in obstetric history.                                       |
| `P`               | `create_gtpals`                           | Maps to `preterm` in obstetric history.                                    |
| `A`               | `create_gtpals`                           | Maps to `abortions` in obstetric history.                                  |
| `L`               | `create_gtpals`                           | Maps to `living_children` in obstetric history.                            |
| `births`          | `create_gtpals`                           | Maps to the `description` field for obstetric history.                     |
| `prev.gynsurg.`   | `create_past_gyne_surg`                   | Used for past gynecological surgeries (`other` field).                     |

---

## Key Functionality

### 1. `create_patient`
- **Purpose:** Inserts a new patient record into the `patients` table.
- **Key Operations:**
  - Checks if the patient already exists based on `folder`, `org_id`, and `canonical`.
  - If found, returns the existing `patient_id`.
  - If not found, inserts a new record and returns the `patient_id`.
- **Field Handling:**
  - `dob`: Defaults to `0000/00/00` if empty; formats valid dates.
  - `Gender`: Converts `m/f` to `0/1`, and unspecified to `2`.
- **Error Handling:** Catches and logs database errors.

### 2. `create_admission_forms`
- **Purpose:** Links a patient to an admission form in the `admission_forms` table.
- **Key Operations:**
  - Inserts a new record with timestamps (`created_at`, `updated_at`).
  - Returns the `admission_form_id` for further use.

### 3. `create_clinical_history_and_physical`
- **Purpose:** Adds a clinical history and physical record linked to a patient and admission form.
- **Key Operations:**
  - Sets default values (e.g., `signed_off` = 0, `note_category_id` = 6).
  - Inserts the record and retrieves the `clinical_history_and_physical_id`.

### 4. `create_ongoing_problems`
- **Purpose:** Logs ongoing problems for a patient.
- **Key Operations:**
  - Inserts records into `clinical_history_and_physical_patient_ongoing_problems`, linking them to the `clinical_history_and_physical_id`.

### 5. `create_allergies`
- **Purpose:** Records patient allergies.
- **Key Operations:**
  - Checks for existing allergens in the `allergens` table.
  - If found, links the allergen to the patient.
  - If not, logs the allergy as "unknown allergen."

### 6. `create_occupation`
- **Purpose:** Adds a patient's occupation.
- **Key Operations:**
  - Checks for existing occupations in the `occupations` table.
  - Links known occupations or logs unknown ones as `detail` records.

### 7. `create_pshx`
- **Purpose:** Logs past surgical history.
- **Key Operations:**
  - Adds records to `clinical_history_and_physical_past_surgical_procedures`.
  - Uses a default `procedure_type_id` and appends additional details.

### 8. `create_pmhx`
- **Purpose:** Records past medical history.
- **Key Operations:**
  - Links `clinical_history_and_physical_id` with a default `pmhx_option_id`.
  - Stores additional details in the `other` field.

### 9. `create_contraception`
- **Purpose:** Logs contraception methods.
- **Key Operations:**
  - Checks for existing methods in `contraception_methods`.
  - Links known methods or logs unknown ones as `detail` records.

### 10. `create_gtpals`
- **Purpose:** Adds obstetric history (GTPAL).
- **Key Operations:**
  - Inserts data into `clinical_history_and_physical_gtpals`.
  - Skips empty records.

### 11. `get_sdpr_patient_id`
- **Purpose:** Links `sdpr_patient_id` with the `patients_id`.
- **Key Operations:**
  - Inserts data into the `sdpr_patients` table and returns the `sdpr_patient_id`.

### 12. `create_socialhx`
- **Purpose:** Logs social history.
- **Key Operations:**
  - Inserts records into `sdpr_patient_admission_form_options`.
  - Uses a specific `admission_form_option_id`.

### 13. `create_familyhx`
- **Purpose:** Logs family history.
- **Key Operations:**
  - Similar to `create_socialhx` but with a different `admission_form_option_id`.

### 14. `create_past_gyne_surg`
- **Purpose:** Records past gynecological surgeries.
- **Key Operations:**
  - Inserts data into `procedures` and `surgeries` tables.

### 15. `create_rxhx`
- **Purpose:** Logs prescription history.
- **Key Operations:**
  - Checks for existing drugs in the `drugs` table.
  - Links known drugs or logs unknown ones using a default ID.

### 16. `Main_function`
- **Purpose:** Serves as the script’s entry point.
- **Key Operations:**
  - Connects to the MySQL database.
  - Calls `importing_data_from_stapleton_file`.
  - Ensures proper cleanup of resources.

### 17. `importing_data_from_stapleton_file`
- **Purpose:** Processes the CSV file and orchestrates record creation.
- **Key Operations:**
  - Reads the CSV file.
  - Iterates through rows, calling the appropriate functions to create records.
  - Ensures relationships between records are correctly established.
- **Error Handling:** Logs errors for diagnostics.

---

