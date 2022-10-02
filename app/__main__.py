from app.app import extract_and_transform_all, load_all, run_analytics
from app.utils import DB, read_all_from_csv


PROMPT_READ = """
********************** Welcome! *****************************
*************************************************************
Would you like to read files from .csv? 
This will save time by bypassing the long extraction process.\n
NOTE: this will only work if you have previously chosen to write to .csv.
Choose 'n' if you haven't ran the program yet.\n
Read from csv? [y/n] """

PROMPT_WRITE = """
*************************************************************
Would you like to save all data to individual .csv files?
This will save you time when running this program again.\n
These .csv's will be written to the app/data directory.\n
Write to .csv? [y/n] """

def run():
    # ASK TO READ FROM CSV ###############################################
    read = input(PROMPT_READ)

    # PREFERRED METHOD OF EXTRACTION #####################################
    data = None
    if read.lower() == 'n':
        write = input(PROMPT_WRITE)
        
        print("\n******************* EXTRACT AND TRANSFORM *******************")
        data = extract_and_transform_all(True if write.lower() == 'y' else False)
    
    elif read.lower() == 'y':
        data = read_all_from_csv()
        
    else:
        print("\nPlease run the program again and enter either 'y' or 'n' for responses.")
        return

    # LOADING PHASE ######################################################
    print("\n******************* LOAD INTO DATABASE **********************")
    db = DB()
    load_all(db, *data)

    # ANALYTICS PHASE ####################################################
    print("\n******************* CREATE ANALYTICS ************************")
    run_analytics(db)

    print("\nDONE: exiting successfully.")

    # FEEL FREE TO DO ANY DB TESTING HERE WITH THE DB OBJECT #############
    res = db.query("SELECT * FROM artists LIMIT 10")
    print(res)

    db.close()
    
run()