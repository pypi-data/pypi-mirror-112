# Google Scholar Report
<center><img src="https://raw.githubusercontent.com/colav/colav.github.io/master/img/Logo.png"/></center>

# Description
Google Scholar Report is a tool for collecting data from Google Scholar profiles and storing it with metadata for each scientific paper. This tool has three main forms of use: generic, authenticated and admin; which differ in the amount and quality of the collected metadata. The default output is xlsx.

## Usage from python-cli

## Installation Package
`$pip install GoogleScholarReport`

For the first option of use (generic), use: 

```python
>>> from GoogleScholarReport import collector
>>> collector.gsr('url_to_google_scholar_profile', ouput='json')
```
Example
```python
>>> from GoogleScholarReport import collector
>>> collector.gsr('https://scholar.google.com/citations?user=1sKULCoAAAAJ&hl=en', ouput='json')
```

For the second option of use (user authenticate):
```python
>>> from GoogleScholarReport import collector
>>> collector.gsr('url_to_google_scholar_profile',email='user_email_google_scholar',password='pass_user_gs',' ouput='json')
```

Finally, for admin mode, use: 
```python
>>> from GoogleScholarReport import collector
>>> collector.gsr('url_to_google_scholar_profile',email='user_email_google_scholar',password='pass_user_gs', ouput='some_ouput(csv,json)',admin=True)
```

# Usage from command-line 
From command line, this tool has three main forms of use: generic, authenticated and admin; which differ in amount and quality of the collected metadata results.

For the first option of use (generic), use: 

```bash
collector "url_for_the_google_scholar_profile"
```
Example:
```bash
collector "https://scholar.google.com/citations?user=1sKULCoAAAAJ&hl=en"
```

The above option return one xlsx file report in the current working directory with the following metadata:

'title', 'author', 'journal', 'volume', 'number','pages', 'year', 'cite_id', 'cites', 'TitleU'.

If you want the output in csv or json format aggregate the bellow flag and the desire output format, for instance:

```bash
collector "url_for_the_google_scholar_profile" --output csv
```

For the second option of use (user authenticate):

```bash
collector "url_for_the_google_scholar_profile" --email <email> --password <password>
```

This return one xlsx file report in the current working directory with the following metadata:

'cite_id', 'cites', 'publisher', 'year', 'pages', 'number', 'volume', 'journal', 'author', 'title','ENTRYTYPE', 'ID', 'school', 'booktitle', 'organization', 'note','month', 'institution'
 
 Finally, for admin mode, issue: 
 
```bash
collector "url_for_the_google_scholar_profile" --email <email> --password <password> --admin
```

This returns by default an xlsx file with the same metadata that option two plus one fiedl 'bibtex'.

In general this command line tool have the following form:

```bash
collector "url_for_the_google_scholar_profile" --email <user_email> --password <password> --output <format> --admin
```
