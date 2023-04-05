import zipfile


jar_file = zipfile.ZipFile('conector-ftp-1.0.jar' ,'r')

jar_file.extractall()
jar_file.close()
