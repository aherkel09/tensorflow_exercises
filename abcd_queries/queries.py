class Queries:
    def __init__(self):    
        self.all = {
            'fastqc01': ['fast', 'SELECT * FROM fastqc01 WHERE ftq_complete=1 ' + 
                         'AND ftq_quality=1 AND ftq_recalled=0'],
            'mrinback02': ['mrin', 'SELECT * FROM mrinback02']
        }
