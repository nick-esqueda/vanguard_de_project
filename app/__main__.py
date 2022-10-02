import textwrap
from app.app import extract_and_transform_all, load_all, run_analytics
from app.utils import DB, read_all_from_csv


def run():
    # ASK TO READ FROM CSV ###############################################
    read = textwrap.dedent("""\
        ********************** Welcome! *****************************
        Would you like to read files from .csv? 
        This will skip the extraction process and move on to the 
        transformation, loading, and analytics processes.\n
        NOTE: this will only work if you have previously chosen to write to .csv.\n
        Please choose 'n' if you haven't ran the program yet.\n
        Read from csv? [y/n] """)
    read = input(read)

    # PREFERRED METHOD OF EXTRACTION #####################################
    data = None
    if read.lower() == 'n':
        write = textwrap.dedent("""\
            
            *************************************************************
            Would you like to save the data to individual .csv files?\n
            These .csv's will be written to the app/data directory.
            This will help save time when running this program again.
            Feel free to check them out after the program is done!\n
            Write to .csv? [y/n] """)
        write = input(write)
        
        print("\n******************* EXTRACT AND TRANSFORM *******************")
        data = extract_and_transform_all(True if write.lower() == 'y' else False)
        
    elif read.lower() == 'y':
        data = read_all_from_csv()
        if data is None:
            return
        
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