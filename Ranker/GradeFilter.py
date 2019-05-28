import re


class gradeFilter:
    
    
    def GradeTranform(self,sentences):
        self.grade = "Good"
        self.gradeType = "Good"
        
        for sentence in sentences:
            self.grade1 = re.search('[0-9].[0-9][0-9]?',sentence)
            self.grade2 = re.search('[0-9][0-9](.[0-9][0-9]?)?%',sentence)
            self.grade3 = re.search('Excellent|Very Good|Good|Fair|Pass',sentence,re.I)
            
            if (self.grade2):
                self.grade = self.grade2.group()
                self.gradeType = "Percentage"
            elif (self.grade1):
                self.grade = self.grade1.group()
                self.gradeType = "GPA"
            elif (self.grade3):
                self.grade = self.grade3.group()
                self.gradeType = "Word"
            else:
                self.gradeType = "Not Found!"
                self.grade = "Good"
                
            if self.gradeType == "Percentage":
                self.grade = float(self.grade[:-1])
                if self.grade >= 90.0:
                    self.grade = "Excellent"
                elif self.grade >= 80.0:
                    self.grade = "Very Good"
                elif self.grade >= 70.0:
                    self.grade = "Good"
                else:
                    self.grade = "Pass"
                break
            elif self.gradeType == "GPA":
                self.grade = float(self.grade)
                if self.grade >= 3.7:
                    self.grade = "Excellent"
                elif self.grade >= 2.8:
                    self.grade = "Very Good"
                elif self.grade >= 2.0:
                    self.grade = "Good"
                else:
                    self.grade = "Pass"
                break
            
        return self.grade