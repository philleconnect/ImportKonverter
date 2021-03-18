#!/usr/bin/env python3

# PhilleConnect import data creator for LUSD data
# © 2020 Johannes Kreutz, Dirk Winkel.

# Include dependencies
import os
import sys
import json
import unicodedata

# Configuration information
CSV_DELIMITER = ";"
STUDENT_HEADER = {
    "firstname": "Schueler_Vorname",
    "lastname": "Schueler_Nachname",
    "class": "Schueler_Klasse",
    "birthdate": "Schueler_Geburtsdatum",
    "email": "Schueler_Email"
}
TEACHER_HEADER = {
    "firstname": "Lehrer_Vorname",
    "lastname": "Lehrer_Nachname",
    "birthdate": "Lehrer_Geburtsdatum",
    "email": "Lehrer_Email",
    "short": "Kuerzel"
}
GROUP_HEADER = {
    #"courseStudent": "Schueler_Name", # Written as "lastname, firstname"
    "courseName": "Kurs_Bezeichnung",
    "courseTeacher": "Fachlehrer_Kuerzel"
}

# DO NOT CONFIGURE ANYTHING BELOW THIS LINE
# Global data
users = []
groups = []

# Helper functions
def checkFolderPaths(PATH):
    if not os.path.exists(PATH):
        return 1
    elif not os.path.isdir(PATH):
        return 2
    elif not os.access(PATH, os.W_OK):
        return 3
    return 0

def fixSpecialChars(name):
    name = name.replace(" ", "_")
    name = name.replace("ä", "ae")
    name = name.replace("ö", "oe")
    name = name.replace("ü", "ue")
    name = name.replace("Ä", "Ae")
    name = name.replace("Ö", "Oe")
    name = name.replace("Ü", "Ue")
    name = name.replace("ß", "ss")
    name = name.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`'~=+"})
    name = unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode("utf-8")
    return name

def userQuestion(text, isSecond = False):
    yesSigns = ["Y", "y", "J", "j"]
    noSigns = ["N", "n"]
    if isSecond:
        print("Unable to interpret input. Please try again.")
    print(text)
    response = input("Y/N: ")
    if any(yesSign in response for yesSign in yesSigns):
        return True
    elif any(noSign in response for noSign in noSigns):
        return False
    else:
        return userQuestion(text, True)

# Check parameters
if len(sys.argv) == 2 and sys.argv[1] == "--help":
    print("This tool creates a PhilleConnect import file for users and groups based on LUSD CSV exports.")
    print("Usage: lusd.py /path/to/students.csv /path/to/teachers.csv /path/to/groups.csv /path/to/output/folder/")
#    print("/path/to/students.csv: A file with all students.")
    print("/path/to/teachers.csv: A file with all teachers.")
    print("/path/to/groups.csv: A file with all student-group relations.")
    print("/path/to/output/folder/: The output file will be generated in this folder.")
elif len(sys.argv) == 4:
    for x in range(1, 3):
        result = checkFolderPaths(sys.argv[x])
        if result == 1:
            print("Error: No such file or directory: " + sys.argv[x])
            sys.exit()
        elif not result == 2 and x < 4:
            print("Error: " + sys.argv[x] + " is a directory.")
            sys.exit()
        elif result == 3 and x == 4:
            print("Error: Directory " + sys.argv[x] + " is not writeable.")
            sys.exit()
else:
    print("Usage: lusd.py /path/to/teachers.csv /path/to/groups.csv /path/to/output/folder/")
    sys.exit()

# Group questions
sGroup = userQuestion("Do you want to add all students to the 'students' group?")
tGroup = userQuestion("Do you want to add all teachers to the 'teachers' group?")
wGroup = userQuestion("Do you want to add all users to the 'wifi' group?")

# Read files
# Students
first = True
with open(sys.argv[2], "r") as f:
    for line in f.readlines():
        data = line.split(CSV_DELIMITER)
        if first:
            first = False
            for key, value in STUDENT_HEADER.items():
                index = 0
                found = False
                for d in data:
                    if value == d:
                        STUDENT_HEADER[key] = index
                        found = True
                    index += 1
                if not found:
                    print('ERROR while setting students: Colum for '+value+' not found!')
                    print('(I saw: '+data+' )')
                    exit(1)
            print('reading students...')
        else:
            if not data[STUDENT_HEADER["firstname"]] == "" and not data[STUDENT_HEADER["lastname"]] == "":
                group = fixSpecialChars(data[STUDENT_HEADER["class"]].strip())
                if (group == ''):
                    continue;
                if (not group in groups):
                    groups.append(group)
                try:
                    user = {
                        "firstname": data[STUDENT_HEADER["firstname"]].strip().replace("'", ""),
                        "lastname": data[STUDENT_HEADER["lastname"]].strip().replace("'", ""),
                        "birthdate": data[STUDENT_HEADER["birthdate"]].strip(),
                        "email": data[STUDENT_HEADER["email"]].strip(),
                        "groups": [group]
                    }
                except:
                    print('did not find all data, are the colums defined for all rows? (solution: define "end of line"-colum with some string in spreadsheet!)')
                    print('Stopped at Student '+
                            data[STUDENT_HEADER["firstname"]]+
                            data[STUDENT_HEADER["lastname"]])
                    exit(1)
                if sGroup:
                    user["groups"].append("students")
                exists = False
                for u in users:
                    if ((u['firstname'] == user['firstname'])
                            and (u['lastname'] == user['lastname'])
                            and (u['birthdate'] == user['birthdate'])):
                        exists = True
                        #if u['class'] != user['class']:
                        #    print('ERRORR: Found same firstname, lastname and birthdate in different classes:\n'+u+'\n'+user)
                        break
                if not exists:
                    users.append(user)
# Teachers
first = True
with open(sys.argv[1], "r") as f:
    for line in f.readlines():
        data = line.split(CSV_DELIMITER)
        if first:
            first = False
            for key, value in TEACHER_HEADER.items():
                index = 0
                found = False
                for d in data:
                    if value == d:
                        TEACHER_HEADER[key] = index
                        found = True
                    index += 1
                if not found:
                    print('ERROR while setting teachers: Colum for '+value+' not found!')
                    exit(1)
            print('reading teachers...')
        else:
            if not data[TEACHER_HEADER["firstname"]] == "" and not data[TEACHER_HEADER["lastname"]] == "":
                try:
                    user = {
                        "firstname": data[TEACHER_HEADER["firstname"]].strip().replace("'", ""),
                        "lastname": data[TEACHER_HEADER["lastname"]].strip().replace("'", ""),
                        "birthdate": data[TEACHER_HEADER["birthdate"]].strip(),
                        "email": data[TEACHER_HEADER["email"]].strip(),
                        "short": data[TEACHER_HEADER["short"]].strip(),
                        "groups": []
                    }
                except:
                    print('did not find all data, are the colums defined for all rows? (solution: define "end of line"-colum with some string in spreadsheet!)')
                if tGroup:
                    user["groups"].append("teachers")
                users.append(user)

# Group connections
first = True
with open(sys.argv[2], "r") as f:
    for line in f.readlines():
        data = line.split(CSV_DELIMITER)
        if first:
            first = False
            for key, value in GROUP_HEADER.items():
                index = 0
                found = False
                for d in data:
                    if value == d:
                        GROUP_HEADER[key] = index
                        found = True
                    index += 1
                if not found:
                    print('ERROR while setting groups: Colum for '+value+' not found!')
                    exit(1)
            print('reading groups...')
        else:
            group = fixSpecialChars(data[GROUP_HEADER["courseName"]].strip() + "_" + data[GROUP_HEADER["courseTeacher"]].strip())
            #username = data[GROUP_HEADER["courseStudent"]].strip()
            if (group == ''):
                continue;
            if (not group in groups):
                groups.append(group)
            for user in users:
                if (user["firstname"] == data[STUDENT_HEADER["firstname"]].strip().replace("'", "") and
                        user["lastname"] == data[STUDENT_HEADER["lastname"]].strip().replace("'", "") and
                        user["birthdate"] == data[STUDENT_HEADER["birthdate"]].strip()):
                    user["groups"].append(group)
                if ("short" in user 
                        and user["short"] == data[GROUP_HEADER["courseTeacher"]].strip()
                        and group not in user['groups']):
                    user["groups"].append(group)

# Add wifi group
if wGroup:
    for user in users:
        user["groups"].append("wifi")

# Create output
output = {
    "type": "philleconnect/users-and-groups",
    "version": 1,
    "users": users,
    "groups": groups
}
outputPath = sys.argv[3]
if not outputPath.endswith("/"):
    outputPath += "/"
outputPath += "philleConnectImport.json"
with open(outputPath, "w") as f:
    f.write(json.dumps(output, indent=4))
print("Done.")
