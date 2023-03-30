from psycopg_pool import ConnectionPool
import os
import re
from flask import current_app as app

class DB():
  def __init__(self):
    self.init_pool()
    
  def template(self,name):
    template_path = os.path.join(app.root_path, 'db','sql', name + '.sql')
    print(template_path)
    with open(template_path, "r") as file:
      sql = file.read()
    return sql
    

    
 # This code connects to a database using a connection URL. The connection URL is
# read from the environment variable CONNECTION_URL. The connection is stored
# in the pool variable.
  def init_pool(self):
    connection_url = os.getenv("CONNECTION_URL")
    self.pool = ConnectionPool(connection_url)
  # Be sure to check RETURNING in all UPPER CASE
  def print_sql(self,title, sql):
    
    cyan = '\033[96m'
    no_color = '\033[0m'
    print(f"{cyan}SQL query statement [{title}]-------------{no_color}")
    print(sql, "sqllll")
    
    
  def query_commit(self,sql, params):
    self.print_sql('commit with returning', sql)
    
    pattern = r"\bRETURNING\b"
    print(pattern,sql)
    is_returning_id = re.search(pattern, sql)

    try:
      with self.pool.connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        if is_returning_id:
          returning_id = cur.fetchone()[0]
        conn.commit()
        
        if is_returning_id:
          return returning_id
      
    except (Exception) as errors:
      self.print_sql_err(errors)
    
  # when we want to return a json object
  def query_object_json(self,sql):
      # Query the database for the requested data and return a JSON object.
      # The query is wrapped in a function that returns the data in an object.
      # This function is passed to the database cursor as a parameter.
      # The cursor executes the query and returns the results as a JSON object.
      print("SQL query statement [object]------------------")
      print(sql + "\n")
      # Wrap an array of SQL statements in a transaction
      # Use the database pool to get a database connection
      with self.pool.connection() as conn:
        # Use the connection to get a database cursor
        with conn.cursor() as cur:
          # Execute the SQL query using the cursor
          cur.execute(wrapped_sql)
          # Return the first row of the result set
          # This row contains the JSON object
          json = cur.fetchone()
          # Return the JSON object
          return json[0]

  # Function: query_array_json
  # Description: This function executes a SQL query statement and returns a JSON object.
  # Parameters: sql -> SQL query statement
  # Returns: JSON object
  # Context: This function is used to execute a SQL query statement and return the results in JSON format.
  # Other Info: None
  def query_array_json(self,sql):
      print("SQL query statement [array]------------------")
      print(sql + "\n")
  
      wrapped_sql = self.query_wrap_array(sql)
  
      with self.pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(wrapped_sql)
          json = cur.fetchone()
          return json[0]
  
  
  # when we want to return a json object
  def query_object_json(self, sql):
    print("SQL query statement [object]------------------")
    print(sql + "\n")
    wrapped_sql = self.query_wrap_object(sql)
    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql)
        json = cur.fetchone()
        return json[0]
    
    
  def query_wrap_object(self, template):
    sql = f"""
    (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
    {template}
    ) object_row);
    """
    return sql
  
  def query_wrap_array(self, template):
    sql = f"""
    (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
    {template}
    ) array_row);
    """
    return sql
  

  def print_sql_err(self,err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print ("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print ("psycopg2 traceback:", traceback, "-- type:", err_type)

    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")
    
    # print the error log
    print("Logging the error")
    
    

db = DB()