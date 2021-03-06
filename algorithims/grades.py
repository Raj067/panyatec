from numpy import *
from pathlib import Path
from pandas import DataFrame
import matplotlib.pyplot as plt
import pandas as pd
import time
import fpdf

BASE_DIR = Path(__file__).resolve().parent.parent

class Grade:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def grade(self, x):
        '''The internal function that return
          the grade and their corresponding points
          for each subject
          note: x = array of subject whose grade
          has to be calculated
          darasa = type of school'''
        code = []
        label = []
        # Checking if the array does exist
        if len(x) > 0:
            for i in x:
                #Checking for advance students
                if self.kwargs['darasa'] == 'a':
                    # for grade A
                    if 100 >= float(i) and float(i) >= int(self.kwargs['A']):
                        code.append(1)
                        label.append('A')
                    # for grade B
                    elif float(i) >= int(self.kwargs['B']) and float(i) < int(self.kwargs['A']):
                        code.append(2)
                        label.append('B')
                    # for grade C
                    elif float(i) >= int(self.kwargs['C']) and float(i) < int(self.kwargs['B']):
                        code.append(3)
                        label.append('C')
                    # for grade d
                    elif float(i) >= int(self.kwargs['D']) and float(i) < int(self.kwargs['C']):
                       code.append(4)
                       label.append('D')
                    # for grade e
                    elif float(i) >= int(self.kwargs['E']) and float(i) < int(self.kwargs['D']):
                        code.append(5)
                        label.append('E')
                        #for grade s
                    elif float(i) >= int(self.kwargs['S']) and float(i) < int(self.kwargs['E']):
                        code.append(6)
                        label.append('S')
                    # for grade f
                    elif float(i) >= int(self.kwargs['F']) and float(i) < int(self.kwargs['S']):
                        code.append(7)
                        label.append('F')
                    else:###for data exceeding 100 or nan
                        code.append(7)
                        label.append(' ')

                # Checking for ordinary students, primary and k students
                if self.kwargs['darasa'] != 'a':
                    # for grade A
                    if 100 >= float(i) and float(i) >= int(self.kwargs['A']):
                        code.append(1)
                        label.append('A')
                    # for grade B
                    elif float(i) >= int(self.kwargs['B']) and float(i) < int(self.kwargs['A']):
                        code.append(2)
                        label.append('B')
                    # for grade C
                    elif float(i) >= int(self.kwargs['C']) and float(i) < int(self.kwargs['B']):
                        code.append(3)
                        label.append('C')
                    # for grade d
                    elif float(i) >= int(self.kwargs['D']) and float(i) < int(self.kwargs['C']):
                        code.append(4)
                        label.append('D')
                    # for grade f
                    elif float(i) >= int(self.kwargs['F']) and float(i) < int(self.kwargs['D']):
                        code.append(5)
                        label.append('F')
                    else:#for nan data
                        code.append(5)
                        label.append(' ')
                    pass
                # Checking for primary students
                #if self.kwargs['darasa'] == 'p':
                #    pass
                # Checking for nursery students
                #if self.kwargs['darasa'] == 'k':
                #    pass

        return array(code).reshape(-1, 1), array(label).reshape(-1, 1)

    def encode(self):
        '''The function which return the data in array
         format in grades, division and division points
         also return label ie
         :return data, label
         note: for div, the last limit is required
         ie div 1 = 7-18 etc
         list_of_marks = [marks1, marks2,.....marksn]
         list_of_subject = [subject names]
         sex = [list of sexes ]
         name = [list of names]
         number = [list of numbers ]
         ** they should be arranged in order
         '''

        sub_data_points = concatenate(
            [self.grade(i)[0] for i in self.kwargs['list_of_marks']], axis=1)

        sub_data_points = concatenate([i.reshape(-1, 1) for i in sub_data_points], axis=1)

        sub_data_grade = concatenate(
            [self.grade(i)[1] for i in self.kwargs['list_of_marks']], axis=1)
        sub_data_grade = concatenate([i.reshape(-1, 1) for i in sub_data_grade], axis=1)


        div_points = None
        if self.kwargs['darasa'] == 'o':
            #for o level
            div_points = [sum(sorted(i)[:7]) for i in sub_data_points]
        elif self.kwargs['darasa'] == 'a':
            # for advance
            div_points = [sum(sorted(i)[:3]) for i in sub_data_points]
        elif self.kwargs['darasa'] == 'p':
            # for primary
            div_points = [sum(sorted(i)[:7]) for i in sub_data_points]
        else:
            #for nursery
            div_points = [sum(i) for i in sub_data_points]

        div = []
        for i in div_points:
            if i >= int(self.kwargs['div_1']) and i <= int(self.kwargs['div_1']):
                div.append(1)
            elif i > int(self.kwargs['div_1']) and i <= int(self.kwargs['div_2']):
                div.append(2)
            elif i > int(self.kwargs['div_2']) and i <= int(self.kwargs['div_3']):
                div.append(3)
            elif i > int(self.kwargs['div_3']) and i <= int(self.kwargs['div_4']):
                div.append(4)
            else:
                div.append(0)
        # Arrays of division and division points
        div = array(div).reshape(-1, 1)
        div_points = array(div_points).reshape(-1, 1)

        #Column of sexes
        sex = array(self.kwargs['sex']).reshape(-1, 1)

        #Column of names
        name = array(self.kwargs['name']).reshape(-1, 1)

        #row of label
        label = ['Name', 'sex'] + self.kwargs['list_of_subject'] + ['division', 'points']
        #data table
        data = concatenate([name, sex, sub_data_grade, div, div_points], axis=1)
        return data, label
    def male(self):
        '''Returning encoded data of male only'''
        return array([i for i in self.encode()[0] if i[:][1] == 'M'])

    def female(self):
        '''Returning encoded data for female only'''
        return array([i for i in self.encode()[0] if i[:][1] == 'F'])

    ###################### without sex #############################
    def div1(self):
        '''Returning data containing students with division 1 only'''
        return array([i for i in self.encode()[0] if int(i[-2]) == 1])

    def div2(self):
        '''Returning data containing students with division 2 only'''
        return array([i for i in self.encode()[0] if int(i[-2]) == 2])

    def div3(self):
        '''Returning data containing students with division 3 only'''
        return array([i for i in self.encode()[0] if int(i[-2]) == 3])

    def div4(self):
        '''Returning data containing students with division 4 only'''
        return array([i for i in self.encode()[0] if int(i[-2]) == 4])

    def div0(self):
        '''Returning data containing students with division 0 only'''
        return array([i for i in self.encode()[0] if int(i[-2]) == 5])

    #################### with sex #####################################
    def div1male(self):
        '''Returning data containing males with division 1 only'''
        return array([i for i in self.male() if int(i[-2]) == 1])

    def div2male(self):
        '''Returning data containing males with division 2 only'''
        return array([i for i in self.male() if int(i[-2]) == 2])

    def div3male(self):
        '''Returning data containing males with division 3 only'''
        return array([i for i in self.male() if int(i[-2]) == 3])

    def div4male(self):
        '''Returning data containing males with division 4 only'''
        return array([i for i in self.male() if int(i[-2]) == 4])

    def div0male(self):
        '''Returning data containing males with division 0 only'''
        return array([i for i in self.male() if int(i[-2]) == 5])

    def div1female(self):
        '''Returning data containing females with division 1 only'''
        return array([i for i in self.female() if int(i[-2]) == 1])

    def div2female(self):
        '''Returning data containing females with division 2 only'''
        return array([i for i in self.female() if int(i[-2]) == 2])

    def div3female(self):
        '''Returning data containing females with division 3 only'''
        return array([i for i in self.female() if int(i[-2]) == 3])

    def div4female(self):
        '''Returning data containing females with division 4 only'''
        return array([i for i in self.female() if int(i[-2]) == 4])

    def div0female(self):
        '''Returning data containing females with division 0 only'''
        return array([i for i in self.female() if int(i[-2]) == 5])

    def required_data(self):
        '''
        Return data in form of pandas dataframe
        '''
        data = self.encode()[0]
        data_key = self.encode()[1]
        req_data = DataFrame({i: data[:, data_key.index(i)] for i in data_key},
                             index=range(1, len(data) + 1))
        return req_data

    def sorted_data(self):
        av = [round(average([float(j) for j in i]), 2) for i in self.kwargs['list_of_marks']]
        dc = {'average': av}
        return pd.concat([self.required_data(), DataFrame(dc, index=range(1, len(av)+1))], axis=1)

    def sorted_results_csv(self):
        tm = time.strftime('%d-%m-%Y_') + str(self.kwargs['class_of_students']) + '__' + self.kwargs[
            'type_of_exam']+'_sorted_data_csv.csv'
        pat = BASE_DIR / 'static/images' /tm

        self.sorted_data().to_csv(pat)
        return tm

    def sorted_results_html(self):
        tm = time.strftime('%d-%m-%Y_') + str(self.kwargs['class_of_students']) + '_' + \
             self.kwargs['type_of_exam'] + '_sorted_data_html.html'
        pat = BASE_DIR / 'static/images' / tm

        self.sorted_data().to_html(pat)
        return tm

    def unsorted_results_csv(self):
        tm = time.strftime('%d-%m-%Y_') + str(self.kwargs['class_of_students']) + '_' + \
             self.kwargs['type_of_exam'] + '_unsorted_data_csv.csv'
        pat = BASE_DIR/'static/images'/tm

        self.required_data().to_csv(pat)
        return tm

    def unsorted_results_html(self):
        tm = time.strftime('%d-%m-%Y_') + str(self.kwargs['class_of_students']) + '__' + self.kwargs[
            'type_of_exam']+'_unsorted_data_html.html'
        fpath = BASE_DIR/'static/images'/tm
        self.required_data().to_html(fpath)
        return tm

    def best_students(self):
        data = [[float(j) for j in i] for i in self.kwargs['list_of_marks']]
        return data

    def first_graph(self):
        '''The graph showing the comparisons between
        number of students and their divisions.....
        Return the path of the saved image first_graph.png'''
        plt.pie(
            [len(self.div0male()), len(self.div0female()),
             len(self.div1male()), len(self.div1female()),
             len(self.div2male()), len(self.div2female()),
             len(self.div3male()), len(self.div3female()),
             len(self.div4male()), len(self.div4female())]
             , labels=['male dvn 0 ', 'female dvn 0 ', 'male dvn 1 ', 'female dvn 1 ',
                           'male dvn 2 ', 'female dvn 2 ', 'male dvn 3 ', 'female dvn 3 ',
                           'male dvn 4 ', 'female dvn 4 ',])
        plt.title('THE PIE CHART SHOWING NO OF STUDENTS AND THEIR DIVISIONS')
        plt.xlabel('')
        plt.ylabel('')
        tm = time.strftime('%d-%m-%Y_') + str(self.kwargs['class_of_students']) + '_' + \
             self.kwargs['type_of_exam'] + '_first_graph.png'
        pat = BASE_DIR/'static/images'/tm
        plt.savefig(pat)
        plt.clf()
        return tm

    def second_graph(self):
        '''The graph showing the comparisons between
        number of students and their divisions in both
        male and female students....
        Return the path to the saved image second_graph.png'''
        aa = pd.DataFrame(
            data=[[len(self.div0male()), len(self.div0female())],
                    [len(self.div1male()), len(self.div1female())],
                    [len(self.div2male()), len(self.div2female())],
                    [len(self.div3male()), len(self.div3female())],
                    [len(self.div4male()), len(self.div4female())]],
                    columns=['Male', 'Female'],
                    index=['division 0 ', 'division 1', 'division 2', 'division 3', 'division 4'])
        aa.plot(kind='bar', rot=30, figsize=(10, 5),
                title='THE GRAPH SHOWING THE COMPARISONS OF PERFORMANCE\n IN MALE AND FEMALE')
        plt.ylabel('Number of students')
        tm = time.strftime('%d-%m-%Y_') + str(self.kwargs['class_of_students']) + '_' + \
             self.kwargs['type_of_exam'] + '_second_graph.png'
        pat = BASE_DIR/'static/images'/tm
        plt.savefig(pat)
        plt.clf()
        return tm

    def third_graph(self):
        '''Returning the graph showing the comparisons
         in performance of students in each subject
          for both male and female..... Returning the path
          of the saved third_graph.png image'''
        sub_data = concatenate(
            [array(i).reshape(-1, 1) for i in self.kwargs['list_of_marks']], axis=1)

        average_data = [round(mean([float(j) for j in i]), 2) for i in sub_data]
        subj = [i for i in self.kwargs['list_of_subject']]
        plt.title('THE GRAPH SHOWING THE GENERAL PERFORMANCE\n IN EACH SUBJECT')
        plt.xlabel('Subjects')
        plt.ylabel('Marks')
        plt.plot(subj, average_data)
        tm = time.strftime('%d-%m-%Y_') + str(self.kwargs['class_of_students']) + '_' + \
             self.kwargs['type_of_exam'] + '_third_graph.png'
        pat = BASE_DIR/'static/images'/tm
        plt.savefig(pat)
        plt.clf()
        return tm

    def each_student(self):
        '''Return the result of each student in pdf format'''
        avg = [round(average([float(j) for j in i]), 2) for i in self.kwargs['list_of_marks']]
        tm = time.strftime('%d-%m-%Y')

        pdf = fpdf.FPDF()
        pdf.add_page()
        for i, j in enumerate(self.encode()[0]):
            pdf.set_font('Arial', size=12)
            pdf.cell(200, 30, txt='', ln=1, align='C')
            pdf.cell(200, 10, txt='Name of the school: '+str(self.kwargs['name_of_school']), ln=1, align='L')
            pdf.cell(200, 10, txt='Type of the examination: '+str(self.kwargs['type_of_exam']), ln=1, align='L')
            pdf.cell(200, 10, txt='Date: ' + str(tm), ln=1, align='L')
            pdf.cell(200, 10, txt='Class: ' + str(self.kwargs['class_of_students']), ln=1, align='L')
            pdf.set_font('Arial', size=12)
            pdf.cell(200, 10, txt='Name of the student: ' + str(j[0]), ln=1, align='L')
            pdf.cell(200, 10, txt='Sex of the student: ' + str(j[1]), ln=1, align='L')
            pdf.cell(200, 10, txt='Average of all subject: ' + str(avg[i]), ln=1, align='L')
            pdf.cell(200, 20, txt='Results', ln=1, align='C')

            for index, item in enumerate(self.kwargs['list_of_subject']):
                #print(item, j[index+2])
                pdf.set_font('Arial', size=12)
                pdf.cell(200, 10, txt=str(item) + '-' * 50 + str(j[index+2]), ln=1, align='L')

            pdf.cell(200, 10, txt='Division' + '-' * 50 + str(j[-2]), ln=1, align='L')
            pdf.cell(200, 10, txt='Points' + '-' * 50 + str(j[-1]), ln=1, align='L')
            pdf.cell(200, 30, txt='\t\tHeadmaster' + '\t' * 80 + 'Class teacher\t\t', ln=1, align='C')
            pdf.cell(200, 5, txt='\t\t' + '.' * 20 + '\t' * 80 + '.' * 20 + '\t\t', ln=1, align='C')
            pdf.add_page()

        tm = time.strftime('%d-%m-%Y_') + str(self.kwargs['class_of_students']) + '_' + \
             self.kwargs['type_of_exam'] + '_each_student.pdf'
        pat = BASE_DIR/'static/images'/tm
        pdf.output(pat)
        return tm

    def general_analysis(self):
        '''Retutning the path of the pdf file containing
                 the analysis of the results'''
        sub_data = concatenate(
            [array(i).reshape(-1, 1) for i in self.kwargs['list_of_marks']], axis=1)

        avg = [round(mean([float(j) for j in i]), 2) for i in sub_data]
        med = [round(median([float(j) for j in i]), 2) for i in sub_data]

        pdf = fpdf.FPDF()
        #Title page
        pdf.add_page()
        pdf.set_font('Arial', size=20)
        pdf.cell(200, 30, txt='ANALYSIS OF THE FORM ' + str(self.kwargs['class_of_students'])+' RESULTS', ln=1, align='C')
        pdf.set_font('Arial', size=15)
        pdf.cell(200, 10, txt='Author: ...........................', ln=2, align='L')
        pdf.cell(200, 60, txt='signature:.........................', ln=3, align='L')
        pdf.cell(200, 10, txt='Revisited by:...........................', ln=4, align='L')
        pdf.cell(200, 60, txt='signature:..........................', ln=5, align='L')
        pdf.cell(200, 10, txt='Time: '+str(time.asctime()), ln=6, align='L')

        pdf.add_page()
        pdf.set_font('Arial', size=20)
        pdf.cell(200, 10, txt='Introduction', ln=2, align='C')
        pdf.cell(200, 10, txt='', ln=1, align='L')
        pdf.set_font('Arial', size=15)
        pdf.cell(200, 10, txt='-> Total number of students who attempted the exam are ' + str(len(self.encode()[0])), ln=3,
                 align='L')

        pdf.cell(200, 10, txt='-> Total number of boys students are ' + str(len(self.male())), ln=4, align='L')
        pdf.cell(200, 10, txt='-> Total number of girls students are ' + str(len(self.female())), ln=5, align='L')

        pdf.set_font('Arial', size=15)

        pdf.cell(200, 10, txt='> Total number of students who score division one are  '
                              +str(len(self.div1())), ln=4, align='L')
        pdf.cell(200, 10, txt='> Total number of students who score division two are  '
                              +str(len(self.div2())), ln=5, align='L')
        pdf.cell(200, 10, txt='> Total number of students who score division three are '
                              +str(len(self.div3())), ln=6, align='L')
        pdf.cell(200, 10, txt='> Total number of students who score division four are '
                              +str(len(self.div4())), ln=7, align='L')
        pdf.cell(200, 10, txt='> Total number of students who score division zero are '
                              +str(len(self.div0())), ln=8, align='L')

        pdf.set_font('Arial', size=20)
        pdf.cell(200, 10, txt='', ln=1, align='L')
        pdf.cell(200, 10, txt='', ln=1, align='L')
        pdf.cell(200, 10, txt='GENERAL PERFORMANCE IN MALE AND FEMALE', ln=2, align='C')
        pdf.cell(200, 10, txt='', ln=1, align='L')
        pdf.set_font('Arial', size=15)
        pdf.cell(200, 10, txt='> Total number of male students who score division one are  '
                              + str(len(self.div1male())), ln=5, align='L')
        pdf.cell(200, 10, txt='> Total number of female students who score division one are  '
                              + str(len(self.div1female())), ln=6, align='L')
        pdf.cell(200, 10, txt='> Total number of male students who score division two are  '
                              + str(len(self.div2male())), ln=7, align='L')
        pdf.cell(200, 10, txt='> Total number of female students who score division two are  '
                              + str(len(self.div2female())), ln=8, align='L')
        pdf.cell(200, 10, txt='> Total number of male students who score division three are '
                              + str(len(self.div3male())), ln=9, align='L')
        pdf.cell(200, 10, txt='> Total number of female students who score division three are '
                              + str(len(self.div3female())), ln=10, align='L')
        pdf.cell(200, 10, txt='> Total number of male students who score division four are '
                              + str(len(self.div4male())), ln=11, align='L')
        pdf.cell(200, 10, txt='> Total number of female students who score division four are '
                              + str(len(self.div4female())), ln=12, align='L')
        pdf.cell(200, 10, txt='> Total number of male students who score division zero are '
                              + str(len(self.div0male())), ln=13, align='L')
        pdf.cell(200, 10, txt='> Total number of female students who score division zero are '
                              + str(len(self.div0female())), ln=14, align='L')
        pdf.cell(200, 10, txt='', ln=1, align='L')
        pdf.cell(200, 10, txt='Analysis of each subject', ln=2, align='C')
        pdf.cell(200, 10, txt='', ln=1, align='L')
        for index, item in enumerate(self.kwargs['list_of_subject']):
            pdf.cell(200, 10, txt='Name of the Subject: ' + str(item), ln=1, align='L')
            pdf.cell(200, 10, txt='The average of the subject is: ' + str(avg[index]), ln=1, align='L')
            pdf.cell(200, 10, txt='The median mark of the subject is : ' + str(med[index]), ln=1, align='L')
            pdf.cell(200, 10, txt='', ln=1, align='L')

        tm = time.strftime('%d-%m-%Y_') + str(self.kwargs['class_of_students']) + '_' + \
             self.kwargs['type_of_exam'] + '_general_analysis.pdf'
        pat = BASE_DIR/'static/images'/tm

        pdf.output(pat)
        return tm

    def files(self):
        data = [self.unsorted_results_csv(), self.unsorted_results_html(),
                self.sorted_results_html(), self.sorted_results_csv(),
                self.each_student(), self.first_graph(), self.second_graph(),
                self.third_graph(), self.general_analysis()]
        return data

'''a = Grade(
    A=80, B=70, C=60, D=50, F=0, E=45, S=39, darasa='o', list_of_marks=[
        [12, 45, 76, 86, 65, 78],
        [12, 45, 76, 86, 65, 67],
        [12, 45, 76, 86, 65, 98],
        [1, 3, 4, 5, 6, 76],
        [12, 45, 76, 86, 65, 50],
    ],
        div_1=7, div_2=18, div_3=21, div_4=25, sex=['M', 'F', 'M', 'M', 'F'],
        name=['male11', 'female11', 'female11', 'female11', 'female11'],
        list_of_subject=['s1', 's2', 's3', 's4', 's5', 's6'],
        type_of_exam='exam', name_of_school='mimi', class_of_students='form 1')
#print(a.graphs_performance())

for i in a.files():
    print(i)'''

#a = dict(dict1, **dict2)
