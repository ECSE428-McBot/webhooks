import json

class ExamDateService:

    posted = True

    # Organize raw to usage data.
    # CAUTION: This will overwrite the original "ExamDate.txt".
    @staticmethod
    def organizeData(showWaste):
        try:
            data = open('RawExamDates.txt', 'r')
            d = data.readlines()
            data.close()
        except:
            return "error - no such file"

        raw = d[0].split()

        examDates = {}  # the dictionary containing all subjects, courses, sections, and corresponding exam dates, times, and notes
        wastebucket = []  # list containing strings not in "examDates"

        subjectName = ""
        courseCount = -1
        state = 0

        while len(raw) > 0:
            a = raw.pop(0)

            # if the string is note...
            if (a == "HOME" or a == "DEPT" or a == "MAC" or a == "CS" or a == "ORAL" or a == "Written" or a == "Practical" or a == "LAB" or a == "MACLAB" or a == "MACHOME" or a == "SEECS" or a == "AllDayOral") and state == 5:
                examDates[subjectName][courseCount].append(a)
                state = 6
            # if the string is subject...
            elif (len(a) == 4 and a.isupper()) and (state >= 5 or state == 0):
                if a != subjectName:
                    subjectName = a
                    examDates[a] = []
                    courseCount = -1
                state = 1
            # if the string is course number...
            elif ((len(a) == 3 and a.isdigit()) or (len(a) == 5 and a[:3].isdigit() and a[-1:].isdigit())) and state == 1:
                examDates[subjectName].append([a])
                courseCount = courseCount + 1
                state = 2
            # if the string is section number...
            elif ((((len(a) == 3 and a.isdigit()) or (len(a) == 4 and (a[-1:] == 'L' or a[-1:] == 'P'))) and a[:2] == "00") or a == "051" or a == "061" or a == "071" or a == "081" or a == "720" or a == "761") and state == 2:
                examDates[subjectName][courseCount].append(a)
                state = 3
            # if the string is date...
            elif ((len(a) == 6 or (len(a) == 9 and a[3:5].isdigit())) and a[-4] == '-' and a[:2].isdigit()) and state == 3:
                examDates[subjectName][courseCount].append(a)
                state = 4
            # if the string is time...
            elif ((len(a) == 5 or len(a) == 4) and a[-3] == ':' and a[-2:].isdigit()) and state == 4:
                examDates[subjectName][courseCount].append(a)
                state = 5
            else:
                wastebucket.append(a + ", state:" + str(state))

        file = open('ExamDates.txt', 'w')
        json.dump(examDates, file)
        file.close()

        # CAUTION: This will overwrite the original "ExamDate.txt".
        if showWaste is True:
            return wastebucket

    @staticmethod
    def readData():
        try:
            data = open('ExamDates.txt', 'r')
            examDates = json.load(data)
            data.close()
            return examDates
        except:
            return "error - no such file"

    @staticmethod
    def searchExamDate(subjectID, courseNum):
        examDates = ExamDateService.readData()

        output = ""

        if examDates is not "error - no such file":

            try:
                courseList = examDates[subjectID.upper()]

                for course in courseList:
                    if course[0] == courseNum:
                        if len(course) == 4:
                            output = output + " section " + str(course[1]) + " " + str(course[2]) + " " + str(course[3]) + ","
                        elif len(course) == 5:
                            output = output + " section " + str(course[1]) + " " + str(course[2]) + " " + str(course[3]) + " note: " + str(course[4]) + ","

                output = output[:-1]  # Remove the last comma.

                if output == "":
                    output = "This course does not have a listed final exam."

                return str(subjectID) + str(courseNum) + ":" + output
            except:
                return "subject not in the list"
        else:
            return examDates  # "error - no such file" message

    @staticmethod
    def giveExamDates(user):
        # Verify user type.
        if user.user_type == 'student':

            # Check if the dates are posted.
            if ExamDateService.posted is True:

                if user.courses is not None:

                    output = ""

                    for course in user.courses.all():
                        subjectID = course.name[:4]
                        courseNum = course.name[-3:]
                        output = output + str(ExamDateService.searchExamDate(subjectID, courseNum)) + " "

                    output = output[:-1]  # Remove the last white space.
                    return output

                else:
                    return "You have not chosen any course yet."  # no course error

            else:
                return "This service is not open since the school has not published the exam dates yet."  # not posted table yet error

        else:
            return "This service is not open due to your user type."  # user type error