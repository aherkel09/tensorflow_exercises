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
                                    WHERE subjectkey NOT IN (
                                        SELECT subjectkey FROM fastqc01 
                                        WHERE ftq_complete=0 OR ftq_quality=0 
                                        OR ftq_recalled=1 OR ftq_usable=0
                                    )
                                    AND ftq_complete=1 AND ftq_quality=1 
                                    AND ftq_recalled=0 AND ftq_usable=1 
                                    AND NULLIF(ftq_notes, " ") IS NULL;
                                    '''],
            'mrinback02': ['mrin', 'SELECT DISTINCT subjectkey FROM mrinback02;'],
            'tbss01': ['tbss', '''
                                    SELECT DISTINCT subjectkey FROM tbss01
                                    WHERE nihtbx_picvocab_fc>49
                                    AND nihtbx_flanker_fc>49
                                    AND nihtbx_list_fc>49
                                    AND nihtbx_cardsort_fc>49
                                    AND nihtbx_pattern_fc>49
                                    AND nihtbx_picture_fc>49
                                    AND nihtbx_reading_fc>49
                                    AND nihtbx_fluidcomp_fc>49
                                    AND nihtbx_cryst_fc>49
                                    AND nihtbx_totalcomp_fc>49;
                                ''']
        }
