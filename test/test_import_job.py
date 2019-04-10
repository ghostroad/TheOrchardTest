from scripts.importer import ImportJob, DataRow
import logging


class FakeStream(object):
    def run(self):
        return [
            DataRow(camis=1234, establishment_data=dict(dba=''), rating_data=dict(grade='A', date='01/02/2019')),
            DataRow(camis=4567, establishment_data=dict(dba='Beauty'), rating_data=dict(grade='P', date='01/02/2019')),
            DataRow(camis=8908, establishment_data=dict(dba='Beauty'), rating_data=dict(grade='A', date='01/02/2019'))
        ]


class FakeDestination(object):
    def __init__(self):
        self.establishment_camises = []
        self.rating_camises = []
    
    def send_establishment_data(self, camis, data, error_reporter):
        self.establishment_camises.append(camis)
    
    def send_rating_data(self, camis, data, error_reporter):
        self.rating_camises.append(camis)


def test_import_job():
    destination = FakeDestination()
    job = ImportJob(FakeStream(), destination, logging.NullHandler())
    job.run()
    
    assert destination.establishment_camises == [4567, 8908]
    assert destination.rating_camises == [1234, 8908]
