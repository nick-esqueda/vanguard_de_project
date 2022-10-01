from .utils import DB, db_view_names, db_view_queries


# VIEWS #########################################
def create_views(db: DB) -> None:
    """
    this function will create all of the pre-determined set of views, using the
    SQL queries provided by db_views.py.
    
    NOTE: all views are dropped before executing the "CREATE VIEW" queries again.
    this is to pick up on any future changes to the views.
    """
    for v_name in db_view_names:
        db.execute(f"DROP VIEW IF EXISTS {v_name};")
        
    for v_query in db_view_queries:
        db.execute(v_query)
