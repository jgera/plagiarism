#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, re, string
from plagiarism import downloadfile, readfile, getkeywords, evaluate, timestr
from network import google

langs = ["english", "russian"]

def writelog(log, file1, keywords1, file2, keywords2, blocks, local = False):
    log.write("=" * 30 + "\n")
    log.write("Source file: " + file1 + "\n")
    log.write("Keywords 1: " + ", ".join(keywords1) + "\n")
    if local:
        log.write("Source file 2: " + file2 + "\n")
    else:
        log.write("Googled file: " + file2 + "\n")
    log.write("Keywords 2: " + ", ".join(keywords2) + "\n")
    for ssk, s, t in blocks:
        log.write("-" * 30 + "\n")
        log.write("Plagiated block with ssk: " + "%0.5f\n" % ssk)
        log.write("Source: " + " ".join(s) + "\n")
        log.write("Googled: " + " ".join(t) + "\n")

def main(argc, argv):
    if argc < 2:
        print("No input file specified")
        return
    
    if argv[1].startswith('http://') or argv[1].startswith('ftp://'):
        text = downloadfile(argv[1])
    else:
        text = readfile(argv[1])
    if text == None:
        print("File don't exist or do not have .pdf or .txt extension")
        return

    log = open("log.txt", 'w')

    if (argc == 3):
        if argv[2].startswith('http://') or argv[2].startswith('ftp://'):
            text2 = downloadfile(argv[2])
        else:
            text2 = readfile(argv[2])
            keywords = getkeywords(text, langs=langs)
            keywords2 = getkeywords(text2, langs=langs)
            print("Keywords for text 1: ", ", ".join(keywords))
            print("Keywords for text 2: ", ", ".join(keywords2))
            print("Searching for plagiated blocks ({0})".format(timestr()))
            blocks = evaluate(text, text2, langs=langs, debug=False)
            print("Search ended, found {0} plagiated blocks ({1})".format(len(blocks), timestr()))
            if len(blocks) > 0:
                writelog(log, argv[1], keywords, argv[2], keywords2, blocks, local=True)
                print("\nAll plagiated blocks were written to log.txt")
        log.close()
        return

    keywords = getkeywords(text, langs=langs)
    print("Keywords for source: " + ", ".join(keywords))
    query = "filetype:pdf " + " ".join(keywords)
    print("Googling: ", query)
    g = google(query)
    results = g.get_results(0)
    if len(results) == 0:
        print("Sorry, googling failed, maybe we are banned")
        return
    print("Google'd ", len(results), " documents:")
    for i, result in enumerate(results):
        print(str(i+1) + ": " + result['url'])

    for i, result in enumerate(results):
        try:
            print("\nProcessing file " + str(i+1) + ": " + result['url'])
            text2 = downloadfile(result['url'])
            if text2 == None:
                print("This file appears to be invalid .pdf file")
                continue
            keywords2 = getkeywords(text2, langs=langs)
            print("Keywords: ", ", ".join(keywords2))
            print("Searching for plagiated blocks ({0})".format(timestr()))
            blocks = evaluate(text, text2, langs=langs, debug=False)
            print("Search ended, found {0} plagiated blocks ({1})".format(len(blocks), timestr()))
        except KeyboardInterrupt:
            print("Interrupted by User")
            pass
            continue
        if len(blocks) > 0:
             writelog(log, argv[1], keywords, result['url'], keywords2, blocks)
    print("\nAll plagiated blocks were written to log.txt")
    log.close()

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)