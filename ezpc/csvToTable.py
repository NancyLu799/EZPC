import sys
import csv


if len(sys.argv) < 4:
    print ("Usage: csvToTable.py csv_file html_file solution_file")
    exit(1)

solutionfile = open(sys.argv[3], "r")
list1 = solutionfile.read()
arr1 = list1.split(',')

reader = csv.reader(open(sys.argv[1]))
htmlfile = open(sys.argv[2],"w")
rownum = 0
htmlfile.write('<head><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="http://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.css"><script src="http://code.jquery.com/jquery-1.11.3.min.js"></script><script src="http://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.js"></script><script src="http://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script><script type="text/javascript" src="http://www.kunalbabre.com/projects/table2CSV.js" > </script> </head>')
htmlfile.write('<body><div data-role="page" id="pageone"><div data-role="main" class="ui-content"><form><input id="filterTable-input" data-type="search" placeholder="Search For People..."></form>')

htmlfile.write('<table data-role="table" data-mode="columntoggle" class="ui-responsive sortable", "sortable" id="testTable" data-filter="true" data-input="#filterTable-input">')
htmlfile.write('<thead>')
for row in reader: 
    if rownum == 0:
        htmlfile.write('<tr>')
        counter = 1
        for column in row:
            htmlfile.write('<th data-priority=' + str(counter) + '>' + column + '</th>')
            counter+=1
        htmlfile.write('</tr>')
        
    else:
        htmlfile.write('</thead>')
        htmlfile.write('<tr>')
        for column in row:
            temp = str(column)
            if temp in arr1:
                htmlfile.write('<td bgcolor="#228B22">' + column + '</td>')
            else:
                htmlfile.write('<td>' + column + '</td>')
        htmlfile.write('</tr>')   
    rownum += 1
htmlfile.write('</table></div></body>')
button = '<input value="Export to CSV" type="button" onclick="$(\'' + "#" + 'testTable\').table2CSV()">'
print (button)
htmlfile.write(button)
exit(0)
