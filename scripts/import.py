import argparse
import requests
import csv 
from urllib.parse import urljoin
from uuid import uuid4
import logging

# A slightly more abstract version of the relevant data contained in each row
# of the CSV file
class DataRow(object):
    def __init__(self, camis, establishment_data, rating_data):
        self.camis = camis
        self.establishment_data = establishment_data
        self.rating_data = rating_data

# Encapsulates knowledge about the source and format, yields a stream
# of DataRows
class CSVDataRowStream(object):
    def __init__(self, source_file):
        self.source_file = source_file
    
    def run(self):
        with open(args.source_file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                camis = row['CAMIS']
                establishment_data = dict(
                    dba=row['DBA'], boro=row['BORO'], building=row['BUILDING'], street=row['STREET'], 
                    zipcode=row['ZIPCODE'], phone=row['PHONE'], cuisine=row['CUISINE DESCRIPTION'], 
                    inspection_date=row['INSPECTION DATE']
                )
        
                rating_data = dict(grade=row['GRADE'], date=row['GRADE DATE'])
                
                yield DataRow(camis=camis, establishment_data=establishment_data, rating_data=rating_data)


 
class HttpDestination(object):
    def __init__(self, service_url):
        self.service_url = service_url
    
    def _handle_response(self, response, camis, data, error_reporter):
        if response.status_code == 400:
            error_reporter.error("camis: {}, data: {}, message: {}".format(camis, data, response.json()))
            return False
        else:
            return True
        
    def send_establishment_data(self, camis, data, error_reporter):
        return self._handle_response(requests.put(urljoin(self.service_url, "establishments/{}".format(camis)), json=data), camis, data, error_reporter)
    
    def send_rating_data(self, camis, data, error_reporter):
        return self._handle_response(requests.post(urljoin(self.service_url, "establishments/{}/ratings".format(camis)), json=data), camis, data, error_reporter)


class ImportJob(object):
    def __init__(self, datarow_stream, destination, log_handler):
        self.datarow_stream = datarow_stream
        self.destination = destination
        self.id = str(uuid4())
        self.rows_processed = 0
        self.logger = logging.getLogger("Import job {}".format(self.id))
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(log_handler)
        
    def error(self, message):
        self.logger.error(message)
    
    def info(self, message):
        self.logger.info(message)
    
    def _process(self, datarow):
        if not datarow.establishment_data['dba']: return
        if not self.destination.send_establishment_data(datarow.camis, datarow.establishment_data, self): return
        if not datarow.rating_data['grade'] in ['A', 'B', 'C']: return
        self.destination.send_rating_data(datarow.camis, datarow.rating_data, self)
        
    def run(self):
        for datarow in self.datarow_stream.run():
            self._process(datarow)
            self.rows_processed += 1
            if self.rows_processed % 500 == 0: self.info("Processed {} rows.".format(self.rows_processed))
                    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Import restaurant rating data.')
    parser.add_argument('-b', dest='base_url', help='The base url for the service.', required=True)
    parser.add_argument('source_file')

    args = parser.parse_args()
    base_url = args.base_url
    
    logging_handler = logging.StreamHandler()
    logging_handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))

    job = ImportJob(CSVDataRowStream(args.source_file), HttpDestination(args.base_url), logging_handler)
    job.run()
