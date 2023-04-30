from psycopg_pool import ConnectionPool
import os
import re
import sys
from flask import current_app as app

class DB():
  def __init__(self):
    self.init_pool()
    
  def template(self,*args):
    pathing = list((app.root_path,'db','sql') + args)
    pathing[-1] = pathing[-1] + '.sql'
    print('pathing')
    print(pathing)
    
    template_path = os.path.join(*pathing)
    cyan = '\033[96m'
    green = '\033[92m'
    no_color = '\033[0m'
    print(f"{green}Load Sql Template-[{template_path}] {no_color}")
    
    with open(template_path, "r") as file:
      sql = file.read()
    return sql

 # This code connects to a database using a connection URL. The connection URL is
# read from the environment variable CONNECTION_URL. The connection is stored
# in the pool variable.
  def init_pool(self):
    connection_url = os.getenv("CONNECTION_URL")
    self.pool = ConnectionPool(connection_url)
  
  def print_sql(self,title, sql,params={}):
    
    cyan = '\033[96m'
    no_color = '\033[0m'
    print(f"{cyan}SQL query statement [{title}]-------------{no_color}")
    print(sql,params)
    
  #  
  def print_params(self, params):
    blue = '\033[94m'
    no_color = '\033[0m'
    print(f'{blue} SQL Params:')
    for key,value in params.items():
      print(key, ":", value)
      
# Be sure to check RETURNING in all UPPER CASE 
  def query_commit(self,sql,params={}, verbose=True):
    if verbose:
      self.print_sql('commit with returning', sql,params)
      
    pattern = r"\bRETURNING\b"
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
  # when we want to return a a single value
  def query_value(self,sql,params={},verbose=True):
    if verbose:
      self.print_sql('value',sql,params)

    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(sql,params)
        json = cur.fetchone()
        return json[0]
        
  

  # Function: query_array_json
  # Description: This function executes a SQL query statement and returns a JSON object.
  # Parameters: sql -> SQL query statement
  # Returns: JSON object
  # Context: This function is used to execute a SQL query statement and return the results in JSON format.
  # Other Info: None
  def query_array_json(self,sql,params={},verbose=True):
      if verbose:
        self.print_sql('array', sql,params)
      
      wrapped_sql = self.query_wrap_array(sql)
      with self.pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(wrapped_sql,params)
          json = cur.fetchone()
          return json[0]
  
  
  # when we want to return a json object
  def query_object_json(self, sql,params={},verbose=True):
    if verbose:
      self.print_sql('json', sql,params)
    wrapped_sql = self.query_wrap_object(sql)
    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql,params)
        json = cur.fetchone()
        if json == None:
          return "{}"
        else:
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
    print ("\npsycopg ERROR:", err, "on line number:", line_num)
    print ("psycopg traceback:", traceback, "-- type:", err_type)

    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")
    
    
    

db = DB()