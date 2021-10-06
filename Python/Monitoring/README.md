# Monitoring
This code was made to access the EUIPN API and search the industrial design that was release in the period of one month and save in a .docx file as a table.

## Requirements
Python 3.3 or higher

[python-docx](https://python-docx.readthedocs.io/en/latest/)

* Instalation: `pip install python-docx`

[requests](https://docs.python-requests.org/en/master/)

* Instalation: `pip install requests`

[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

* Instalation: `pip install beautifulsoup4`

[tqdm](https://tqdm.github.io/)

* Instalation: `pip install tqdm`


## Instructions

1. The *query_parameters.json* file should containin the parameters to searche the data through the API, the file structure should be like the follow exemple. In this exemple, there are two searchs, the first one will create the file Monitoramento DIs (File1) - Month.Year.docx, where Month is the three first letters of the month name, like 'Jan' for January. The Year is the year in format YYYY. Also, the values like "start_date" and "end_date" can be replaced with the due value.

`[`

    {
        "fileName": "File1",
        "parameter1": "value1",
        "parameter2": "value2"
        "parameter3": "start_date",
        "parameter4": "end_date"
    },
    {
        "fileName": "File2",
        "parameter1": "value3",
        "parameter2": "value4",
        "parameter3": "start_date",
        "parameter4": "end_date"
    }

`] `

2. The *ModelStyle.docx* file should containing the table header and the style, such as the document, the table or paragraph style. The first one can be set by changing the document and save as a model. The others can be set in the saved styles, by create a style and set it while writing the file, like showed in the [python-docx documentation](https://python-docx.readthedocs.io/en/latest/).

3. Then just run the main file, the files will be saved in the 'files' folder.