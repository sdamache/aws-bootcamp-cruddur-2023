# from aws_xray_sdk.core import xray_recorder
from lib.db import db
import logging

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
class UserActivities:
  def run(user_handle):
    # segment = xray_recorder.begin_segment('user_activities')
    # logger.debug("User's handle: %s",user_handle)
    model = {
      'errors': None,
      'data': None
    }

    if user_handle == None or len(user_handle) < 1:
      model['errors'] = ['blank_user_handle']
    else:
      sql = db.template('users','show')
      # logger.info("sql: %s", sql)
      results = db.query_object_json(sql,{'handle': user_handle})
      # logger.info("Results: %s", results)
      model['data'] = results
      
    return model
    # # AWS X-ray
    # subsegment = xray_recorder.begin_subsegment('mock-data')
    
    # dict = {
    #   "now": now.isoformat(),
    #   "results_length": len(results)
    # }
    # subsegment.put_metadata('now', dict, 'namespace')