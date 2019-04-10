import argparse
import requests
import csv 
from urllib.parse import urljoin

parser = argparse.ArgumentParser(description='Import restaurant rating data.')
parser.add_argument('-b', dest='base_url', help='The base url for the service.', required=True)
parser.add_argument('source_file')

args = parser.parse_args()
base_url = args.base_url
rows_processed = 0
with open(args.source_file) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if rows_processed % 1000 == 0:
            print(rows_processed)
        camis = row['CAMIS']
        establishment_data = dict(
            dba=row['DBA'], boro=row['BORO'], building=row['BUILDING'], street=row['STREET'], 
            zipcode=row['ZIPCODE'], phone=row['PHONE'], cuisine=row['CUISINE DESCRIPTION'], inspection_date=row['INSPECTION DATE']
        )
        
        rating_data = dict(grade=row['GRADE'], date=row['GRADE DATE'])
        
        if establishment_data['dba']:
            r1 = requests.put(urljoin(base_url, "establishments/{}".format(camis)), json=establishment_data)
            if r1.status_code == 400:
                print(r1.json())
                
            if rating_data['grade'] in ['A', 'B', 'C']:                    
                r2 = requests.post(urljoin(base_url, "establishments/{}/ratings".format(camis)), json=rating_data)
                if r2.status_code == 400:
                    print(r2.json())
        
        rows_processed += 1
            

