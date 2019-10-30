class Queries:
    def __init__(self):    
        self.all = {
            'ehis01': ['ehis', '''
                                    SELECT DISTINCT subjectkey FROM ehis01
                                    WHERE ehi1b=100 AND ehi2b=100
                                    AND ehi3b=100 AND ehi4b=100;
                                '''],
            'fastqc01': ['fast', '''
                                    SELECT DISTINCT subjectkey FROM fastqc01 
                                    WHERE ftq_complete=1 AND ftq_quality=1 
                                    AND ftq_recalled=0 AND AND ftq_usable=1 
                                    AND NULLIF(ftq_notes, " ") IS NULL;
                                    '''],
            'mrinback02': ['mrin', 'SELECT DISTINCT subjectkey FROM mrinback02;'],
            'tbss01': ['tbss', '''
                                    SELECT DISTINCT subjectkey FROM tbss01
                                    WHERE nihtbx_totalcomp_agecorrected>=90;
                                ''']
        }
