# imports
import os
import pdfplumber

# from openpyxl import load_workbook
import xlwt


# excel utilities


style1 = xlwt.easyxf("font:bold 1,color blue;")
style2 = xlwt.easyxf("font:bold 1,color red;")
style3 = xlwt.easyxf("font:bold 1,color green;")

wb = xlwt.Workbook()
sheet1 = wb.add_sheet("Result")
sheet1.write(1, 0, "FileName", style1)
sheet1.write(1, 1, "Keyword", style1)
sheet1.write(1, 2, "Result", style1)

# get file list

file_list = [file for file in os.listdir() if file.endswith(".pdf")]


def ehe():
    row = 2
    for file in file_list:
        sheet1.write(row, 0, file)
        content = ""

        keywords = [
            x.lower()
            for x in input(
                f"Enter Keywords in smallcase TO search in file {file} : "
            ).split()
        ]

        with pdfplumber.open(file) as pdf:
            num_of_pages = len(pdf.pages)

            for i in range(num_of_pages):
                page = pdf.pages[i]
                content += page.extract_text()
                content = content.lower()

        for key in keywords:
            if key in content:
                sheet1.write(row, 1, key)
                sheet1.write(row, 2, True, style3)
            else:
                sheet1.write(row, 1, key)
                sheet1.write(row, 2, False, style2)
            row += 1
    wb.save("xlwt result.xls")


ehe()
