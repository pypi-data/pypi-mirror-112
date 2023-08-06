#/usr/bin/python3
import re
import os
import sys
import time
import argparse

import lxml
import helium
from pandas.core.indexes.base import Index

import unidecode
from bs4 import BeautifulSoup
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import pandas as pd

def command_line_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument("url", help="public url for google scholar profile", type=str)

    parser.add_argument("--email", help="email for google scholar account",type=str)

    parser.add_argument("--password", help="password for google scholar account",type=str)

    parser.add_argument("-output","--output", help="format of output file csv or json; default is xlsx",type=str)

    parser.add_argument("-admin","--admin", default=False, action='store_true', help="admin mode True")
    
    #parser.add_argument("-no_admin","--no_admin",dest="admin", action='store_false', help="admin mode True")

    args = parser.parse_args()

    return args

def store_data(df,name, output):
    
    # csv
    if output == 'csv':
        df.to_csv(name+'.csv',index=False)
    # json
    elif output == 'json':
        df.to_json(name + '.json',orient='records')


def read_bibtex(str_bib_tex):
    '''
    Read bibtext database and return a dictionary
    '''
    parser = BibTexParser(common_strings=True)
    
    parser.ignore_nonstandard_types = False
    
    parser.homogenize_fields = True
    
    parser.customization = convert_to_unicode

    bib_data = bibtexparser.loads(str_bib_tex, parser=parser)

    return bib_data

def unidecode_character(match):
    """
    This function takes a re 'match object' and performs
    The appropriate substitutions
    """

    group = match.group(1)
    return 'í'+unidecode.unidecode(group)

def scrapergsp(file,prefix='src_'):
    '''scraper google scholar profile page source'''
    soup = BeautifulSoup(file, 'lxml') # Parse the HTML as a string
    tables = soup.find_all('table')
    if len(tables)>1:
        table =tables[1]
        rows=table.find_all('tr')

    scr_articles=[]
    i=-1
    for row in rows:
        i=i+1
        #*********************
        #Table have 3 columns without authentication (or checkbox column plus 3 columns with authentication): metadadata, citation info and year
        #... Extract the three columns: metadadata, citation info and year
        #... Initialize with non-authentication values
        m=0 # Initialize metada
        c=1 # Initialize citations
        y=2 # Initialize year
        cols=row.find_all('td')
        #...Check that is an article row 
        if len(cols)==0:
            #print('Entries',len(cols))
            continue
        elif len(cols)==4:
            m=m+1
            c=c+1
            y=y+1

        citedby=''; year=''
        if len(cols)>=3:
            metadata=cols[m]
            citedby=cols[c]
            year=cols[y]
        #*********************

        #Metadata scrapping    
        title=metadata.find('a').text
        authors=metadata.find_all('div')[0].text
        #*****************************
        #Metadata → Journal scrapping
        pub=metadata.find_all('div')[1].text.split(', ')
        pages=''
        if len(pub)==3:
            pages=pub[1]
        full_journal=pub[0]
        journal=pub[0]

        #...Intialize
        journal=full_journal
        volume=''
        issue=''
        #...Get real values
        s=re.split(r'\s([0-9]+)+\s',full_journal)
        if len(s)==1:
            s=re.split(r'\s([0-9]+)$',full_journal)
        if len(s)==1:
            s=s+['','']
        if len(s)==2:
            s=s+['']
        #Interpreat real values only if proper length
        if len(s)==3:
            journal=s[0]
            volume=s[1]
            issue=s[2]
        try:
            cite_id=citedby.find('a').get('href').split('cites=')[-1].split(',')[0]
        except:
            cite_id=None
        try:
            cites=citedby.find('a').text
        except:
            cites=None
        #*****************************

        #Fill dictionary
        d={}
        d[f'{prefix}title']=title
        d[f'{prefix}author']=authors
        d[f'{prefix}journal']=journal
        d[f'{prefix}volume']=volume
        d[f'{prefix}number']=issue
        d[f'{prefix}pages']=pages
        d[f'{prefix}year']=year.text
        d['cite_id']=cite_id
        d['cites']=cites
        if d:
            scr_articles.append(d)
        #if i==5:
        #    break
    return scr_articles

def scraping_gs(url):
    # Scraping Google Scholar
 # Scraping Google Scholar
    #url='https://scholar.google.com/citations?hl=en&user=5Fh1OLwAAAAJ'

    url=str(re.sub(r'hl=[a-zA-Z][a-zA-Z]','hl=en', url))

    #    '''
    #    Go to google scholar profile and make scroll to end and catch two html tables: scientific production and index citations. 
    #  '''

    browser=helium.start_firefox(url,headless=True)
    clicks=0

        # Scroll to end
    #print(helium.Button.is_enabled(helium.Button('SHOW MORE')))
    while helium.Button.is_enabled(helium.Button('SHOW MORE')):

        helium.scroll_down(2000000)
        print('reading page:',clicks, 'of Gs profile')
        helium.click(helium.Button('SHOW MORE'))
        helium.scroll_down(100000)
        time.sleep(1.5)
        clicks+=1
    

    # get scraping data and metadata
    rec=scrapergsp(browser.page_source)

    # handle scraping data -> not login 
    dfs = pd.DataFrame(data=rec)
    
    dfs = dfs.drop_duplicates(subset=['src_title']).reset_index(drop=True)

    browser.close()
    
    return dfs

def export_gs(email,password):
    
    '''This function automatice log-in and export article records from Google scholar profile'''
    
    sleep = 1.5
    url_to_gs='https://scholar.google.com/citations?hl=es&login' 

    browser=helium.start_firefox(url_to_gs,headless=False)
    print('Authenticating in google scholar profile...')

    # Login
    helium.write(email,into='Correo electrónico o teléfono')
    print("correOK")

    time.sleep(sleep)
    helium.click(helium.Button('Siguiente'))

    time.sleep(sleep)
    helium.write(password,into='Introduce tu contraseña')

    time.sleep(sleep)
    helium.click(helium.Button('Siguiente'))
    print('Auth google scholar ok')

    # Wait until load page
    helium.wait_until(helium.Text('TÍTULO').exists)

    # Select articles
    print('collecting google scholar records...')
  
    
    time.sleep(3)
    browser.find_element_by_id('gsc_x_all').click()

    time.sleep(sleep)
    helium.click('EXPORTAR')

    time.sleep(sleep)
    helium.click('BibTeX')

    time.sleep(sleep)
    helium.click('Exportar todos mis artículos')

    time.sleep(sleep)
    # Button EXPORTAR
    browser.find_element_by_id('gsc_md_exa_export').click()

    time.sleep(sleep)

    # Handle response bibtext export-> high cuality metadata
    time.sleep(sleep)
    bib_data = read_bibtex(browser.find_element_by_tag_name('html').text)

    dfe=pd.DataFrame(bib_data.entries)

    dfe['ID']=dfe['ID'].apply(unidecode.unidecode)

    # Handle raw bib text data
    bib_raw=browser.find_element_by_tag_name('html').text

    # Generate bib_list 
    bib_list = [re.sub(r'^(\w)', r'@\1',l,re.UNICODE) for l in re.split(r'\n@',re.sub(r'^@',r'\n@',bib_raw)) if l]

    # Generate unicode bibtext data ids
    bib_ids = [l.split('{')[1].split(',')[0] for l in bib_list]
    bib_ids = [unidecode.unidecode(l) for l in bib_ids]    #

    # Build dict with ids and bibtex data
    bibtex_dict = dict(zip(bib_ids,bib_list))

    # Combine response bibtex and raw bibtext 
    dfe['bibtex']=dfe['ID'].apply(lambda s: bibtex_dict.get(s))

    # Validate results
    assert dfe['bibtex'].shape[0] == dfe['bibtex'].dropna().shape[0]
    # dfe[dfe['bibtex'].isna()]['ID']

    dfe['author'].apply(lambda s: re.sub(r'\\(.)',unidecode_character,s,flags=re.I))
    
    return dfe

def merge(dfs,dfe):
    
    '''Merge scraping and export google scholar profile data'''
    
    # preparing scraping dataframe                                           
    dfs['TitleU']=dfs['src_title'].apply(lambda s: unidecode.unidecode(s)) 

    dfs=dfs.drop_duplicates(subset=['TitleU']).reset_index(drop=True)

    dfs.reset_index(drop=True)

    # preparing dataframe exported gs
    dfe['TitleU'] = dfe['title'].apply(lambda s: unidecode.unidecode(s)
                               ).apply(lambda s: s.replace('$','')
                               ).apply(lambda s: s.replace('--','')
                               ).apply(lambda s: re.sub(r'backslash\w+([\s\)])',r'\1',s.replace('\\',''))
                               ).apply(lambda s: s.replace('^','')
                               ).apply(lambda s: s.replace('_','')
                               ).apply(lambda s: s.replace('  ',' '))  # siempre al final

    dfe = dfe.drop_duplicates(subset=['TitleU']).reset_index(drop=True)

    dfe=dfe.reset_index(drop=True)

    # Merge dfs and dfe
    gs=dfs.merge(dfe,on='TitleU',how='left')

    # Result Merge
    gs=gs.reset_index(drop=True) # ouput if all its good

    print('Exporting google scholar records with all metadata...')
    
    # fix empty results right side
    gsn = gs[~gs['title'].isna()].reset_index(drop=True) # not empty

    gsy = gs[gs['title'].isna()].reset_index(drop=True) # yes, empty right side

    gsy = gsy.dropna(axis=1)

    if gsy.shape[0] > 0:

        g=pd.DataFrame()

        for i in gsy.index:

            d = gsy.loc[[i]].to_dict(orient='records')[0]

            rs = process.extractOne(d['TitleU'],dfe['TitleU'],scorer=fuzz.ratio)

            if rs[1] > 90:

                idx = rs[2]

                d.update(dfe.loc[[idx]].to_dict(orient='records')[0])

                g = g.append(d,ignore_index=True)

            elif (rs[1] > 70) :

                rsp = process.extractOne(d['TitleU'],dfe['TitleU'],scorer=fuzz.partial_ratio)

                if rsp[1] > 90:

                    idx = rsp[2]

                    d.update(dfe.loc[[idx]].to_dict(orient='records')[0])

                    g = g.append(d,ignore_index=True)

                elif rsp[1] > 50:

                    rspp = process.extractOne(d['TitleU'],dfe['TitleU'],scorer=fuzz.token_sort_ratio)

                    if rspp[1] > 70:

                        idx = rspp[2]

                        d.update(dfe.loc[[idx]].to_dict(orient='records')[0])

                        g = g.append(d,ignore_index=True)

                    else:
                        print('problem with record:')
                        print(gsy.loc[i])

                else:
                    print('problem with record:')
                    print(gsy.loc[i])
                    print('\n')

            else:
                print('problem with record:')
                print(gsy.loc[i])
                print('\n')

        gs =pd.concat([gsn,g]) # output if all isn't good
    
    # cleaning columns
    c = [c for c in gs.columns if 'src' not in c and 'TitleU' not in c]

    return gs[c]

def gsr(url, email = '', password = '',output='', admin = False):
    
    if email != '' and password !='' and 'gmail' not in email:
        
        dfs = scraping_gs(url)

        #print('dfs.shape:',dfs.shape)
        
        dfe = export_gs(email, password)

        #print('dfe.shape:', dfe.shape)
        
        gsr = merge(dfs,dfe)

        print('gsr.shape',gsr.shape)

        if admin:
            
            # store df admin

            if output == 'csv' or output == 'json':

                store_data(gsr,'google_scholar_report_admin',output)

                print('Admin  report stored with %s records in format %s' % (gsr.shape[0],output))
            
            else:

                gsr.to_excel('google_scholar_report_admin.xlsx',index=False)

                print('Admin report stored with %s records in format xlsx' % gsr.shape[0])

        else:

            # store df user authenticate

            #gsr=gsr.loc[:, gsr.columns != 'bibtex']

            if output == 'csv' or output == 'json':

                store_data(gsr,'google_scholar_report_user',output)

                print('User authenticated report stored with %s records in format %s' % (gsr.shape[0],output))
            
            else:

                gsr.to_excel('google_scholar_report_user.xlsx',index=False)

                print('User authenticated report stored with %s records in format xlsx' % gsr.shape[0])
    
    else:
        
        dfs = scraping_gs(url)
        
        dfs.rename(columns={    'src_title':'title',
                                'src_author':'author',
                                'src_journal':'journal',
                                'src_volume':'volume', 
                                'src_number':'number',
                                'src_pages':'pages',
                                'src_year':'year'
                           }, 
                   inplace=True)

        # store df generic

        if output == 'csv' or output == 'json':

            store_data(dfs,'google_scholar_report_user',output)

            print('generic report stored with %s records in format %s' % (dfs.shape[0],output))
            
        else:

            dfs.to_excel('google_scholar_report_user.xlsx',index=False)

            print('generic report stored with %s records in format xlsx' % dfs.shape[0])
        

if __name__ == "__main__":

    args = command_line_parser()
    
    print('Conecting With Google Scholar Profile...')

    url = str(args.url)

    if args.email and args.password:

        email = args.email

        if "gmail" in email:

            print("Warning!:loggin by gmail account does not work... a generic report will be generated ")

        password = args.password

        if args.admin:

            admin = args.admin

            print(admin)

            if args.output:

                output = args.output

                gsr(url, email, password, output, admin)

            else:

                gsr(url, email, password, admin=admin)

        else:

            if args.output:

                output = args.output

                gsr(url, email, password,output=output)

            else:

                gsr(url, email, password)
    
    else:

        if args.output:

            output = args.output

            gsr(url,output=output)

        else:

            gsr(url)