plagiarism
==========

Requirements:
* Python 3.3.1
* pdfminer3k: https://pypi.python.org/pypi/pdfminer3k/
* distribute: https://pypi.python.org/pypi/distribute
* nltk: https://github.com/nltk/nltk/
* nltk-data (stopwords): http://nltk.org/data.html
* bs4: http://www.crummy.com/software/BeautifulSoup/

Usage:

To search for plagiated documents in google:

    main.py localfile.txt
    main.py localfile.pdf
    main.py http://example.ru/somefile.txt
    main.py ftp://example.com/somefile.pdf

To compare two documents:

    main.py localfile.txt ftp://example.com/somefile.pdf
    main.py http://example.ru/somefile.txt localfile.pdf
    main.py localfile1.pdf localfile2.pdf

Notice, that somefile.txt must have 'utf-8' encoding.
To change encoding search for data.decode('utf-8') in plagiarism.py

English or russian documents expected. For other languages just change global langs variable in main.py
