# Google Scholar Report
<center><img src="https://raw.githubusercontent.com/colav/colav.github.io/master/img/Logo.png"/></center>

# Description
Google scholar report is a tool for collect data from google scholar profiles and store it with metadata for each scientific paper. This tool have three main forms of use: generic, authenticated and admin; which difer in amount and cuality of metadata results. Default output is xlsx.

## Usage from python-cli

## Installation Package
`$pip install GoogleScholarReport`

For the firts option of use (generic), issue: 

```python
>>> from GoogleScholarReport import collector
>>> collector.gsr('url_to_google_scholar_profile', ouput='json')

```
For the second option of use (user authenticate):
```python
>>> from GoogleScholarReport import collector
>>> collector.gsr('url_to_google_scholar_profile',email='user_email_google_scholar',password='pass_user_gs',' ouput='json')

```

Finally, for admin mode, issue: 
```python
>>> from GoogleScholarReport import collector
>>> collector.gsr('url_to_google_scholar_profile',email='user_email_google_scholar',password='pass_user_gs', ouput='some_ouput(csv,json)',admin=True)

```

# Usage from comman-line 
From comman line, this tool have three main forms of use: generic, authenticated and admin; which difer in amount and cuality of metadata results.

For the firts option of use (generic), issue: 

```bash
python3 collector.py "url_for_the_google_scholar_profile"
```
The above option return one xlsx file report in the current working directory with the following metadata:

'title', 'author', 'journal', 'volume', 'number','pages', 'year', 'cite_id', 'cites', 'TitleU'.

If you want the output in csv or json format agregate the bellow flag and the desire ouput format, for instance:

```bash
python3 collector.py "url_for_the_google_scholar_profile" --output csv
```

For the second option of use (user authenticate):

```bash
python3 collector.py "url_for_the_google_scholar_profile" --email <email> --password <password>
```

This return one xlsx file report in the current working directory with the following metadata:

'cite_id', 'cites', 'publisher', 'year', 'pages', 'number', 'volume', 'journal', 'author', 'title','ENTRYTYPE', 'ID', 'school', 'booktitle', 'organization', 'note','month', 'institution'
 
 Finally, for admin mode, issue: 
 
 ```bash
python3 collector.py "url_for_the_google_scholar_profile" --email <email> --password <password> --admin
```

This return by default an xlsx file with the same metadata that option two plus one fiedl 'bibtex'.

In general this commanline tool have the following form:

```bash
python3 collector.py "url_for_the_google_scholar_profile" --email <user_email> --password <password> --output <format> --admin
```
