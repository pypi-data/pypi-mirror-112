from py4j.protocol import Py4JJavaError

valid = False

class NiceJavaError:
  
  def __init__(self, message, clazz, stackTrace):
    self.message = message
    self.clazz = clazz
    self.stackTrace = stackTrace
    
  def getMessage(self):
    return self.message
  
  def getClass2(self):
    return self.clazz
  
  def getStackTrace(self):
    return self.stackTrace

  def __str__(self):
    return f"NiceJavaError {{message: '{self.message}', clazz: '{self.clazz}'}}"
  
def unpackPysparkError(e: Py4JJavaError) -> NiceJavaError:
    javaException = e.java_exception
    exceptionWithMessage = javaException.toString()
    list = exceptionWithMessage.split(': ')
    clazz = list[0]
    message = list[1]

    stackTrace = '\n\t at '.join(map(lambda x: x.toString(), javaException.getStackTrace()))

    return NiceJavaError(message, clazz, stackTrace)
  

def getProperty(prop):
  try:
    return spark.conf.get(prop)
  except Py4JJavaError as e:
    niceError = unpackPysparkError(e)
    if (niceError.clazz == 'java.util.NoSuchElementException'):
      print(f'Property not found [{prop}]')
      return ''
    else:
      raise e    
    
#passthrough = (getProperty("spark.databricks.passthrough.enabled") =='true')
#
#print(f'Passthrough enabled [{passthrough}]')
#
#processIsolation = (getProperty("spark.databricks.pyspark.enableProcessIsolation") =='true')
#print(f'Process Isolation enabled [{processIsolation}]')
#
#if (not processIsolation or not passthrough):
#  #dbutils.notebook.exit("This notebook requires passthrough and process isolation enabled")
#  raise Exception("This notebook requires passthrough and process isolation enabled")
#else:
#  # Set valid is true as last step.
#  valid = True

