import argon2.exceptions
from PyPDF2 import PdfFileReader, PdfFileWriter

import argparse


splitoken = "="

def handleCommandFile(demofile):
    f = open(demofile)
    temp = f.readlines()
    PDFFile = ""
    for x in temp:
        if x.startswith("command"):
            commandaction = x.split(splitoken)[1].strip()

        if x.startswith("base"):
            basedir = x.split(splitoken)[1].strip()
        if x.startswith("split") and commandaction == "split":
            PDFFile = x.split(splitoken)[1].strip()
        if x.startswith("merge") and commandaction == "merge":
            mergefiles = x.split(splitoken)[1].strip()
        if x.startswith("out"):
            outPDF = x.split(splitoken)[1].strip()
    # either merge into outPDF file name or use outPDF as base name for the splits

    if commandaction == "merge":
       merge_pdfs(basedir, mergefiles.split(","), outPDF)
    elif commandaction == "split":
        split(basedir, PDFFile, outPDF)
    else:
        print ("Invalid or missing command")

"""
    print(commandaction)
    print(outPDF)
    print(basedir)
"""
def checkMerge(mergefiles):
    allfiles=mergefiles.split(",")
    print (allfiles)

def split(basepath, file_to_split, splitName):
    pdf = basepath+"\\"+file_to_split
    print (pdf)
    outpdf = splitName
    pdfObj = PdfFileReader(pdf, strict=False)
    for page in range(pdfObj.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdfObj.getPage(page))

        output = f'{outpdf}{page}.pdf'
        output = basepath+"\\"+output
        with open(output, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)


def merge_pdfs(basepath, filestomerge, output):
    pdf_writer = PdfFileWriter()
    output = basepath+"\\"+ output
    for path in filestomerge:
        pdfFile = basepath+"\\"+path.strip()
        print (pdfFile)
        pdf_reader = PdfFileReader(pdfFile)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)


if __name__ == '__main__':
#    filename = "testcommandfile.txt"
#    handleCommandFile(filename)
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="command file")
    args = parser.parse_args()
    str = (args.command)
    handleCommandFile(str)
    # if str=="":
    #     print("err")
    # else:
    #     strtemp = str.split("=")[1]
    #     print (strtemp)




"""
command file structure:
	command= split | merge
	base= directory path
	split= pdf file name 
	merge= file1, file2, file3, etc....
	out= file name out for the merged files
	# indicates comment

"""
