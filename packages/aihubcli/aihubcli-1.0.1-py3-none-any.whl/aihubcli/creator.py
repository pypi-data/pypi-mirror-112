import os
from importlib_resources import files, as_file
import zipfile

def createProject(projectname):
    path = os.getcwd()
    print ("setting up new projet in directory %s" % path)

    template_file = files('aihubcli').joinpath('templates/default.zip')

    try:
        os.mkdir(path + '/' + projectname)

        with as_file(template_file) as filepath:
            with open(filepath, 'rb') as f:
                z = zipfile.ZipFile(f)

                for name in z.namelist():
                    outpath = path + '/' + projectname +"/"
                    z.extract(name, outpath)


    except OSError as err:
        print ("Creation of the project directory failed")
        print(err)
    else:
        print (f"Successfully created the project {projectname} in directory {path}")