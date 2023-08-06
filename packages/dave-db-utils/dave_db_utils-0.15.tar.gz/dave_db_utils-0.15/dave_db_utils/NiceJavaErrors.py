from py4j.protocol import Py4JJavaError

global innerSpark

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

def setSpark(spark):
    global innerSpark
    innerSpark = spark

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
        return innerSpark.conf.get(prop)
    except Py4JJavaError as e:
        niceError = unpackPysparkError(e)
        if (niceError.clazz == 'java.util.NoSuchElementException'):
            print(f'Property not found [{prop}]')
            return ''
        else:
            raise e

def checkPassThrough():
    passthrough = (getProperty("spark.databricks.passthrough.enabled") == 'true')

    print(f'Passthrough enabled [{passthrough}]')

    processIsolation = (getProperty("spark.databricks.pyspark.enableProcessIsolation") == 'true')
    print(f'Process Isolation enabled [{processIsolation}]')

    return (processIsolation or passthrough)
