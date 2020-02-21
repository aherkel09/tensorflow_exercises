class Queries:
    def __init__(self):    
        self.all = {
            'verified_t1_t2': ['veri', '''
                                    SELECT DISTINCT subjectkey FROM verified_t1_t2;
                                '''], # start with subjects having good t1 & t2 data
            'ehis01': ['ehis', '''
                                    SELECT DISTINCT subjectkey FROM ehis01
                                    WHERE ehi1b=100 AND ehi2b=100
                                    AND ehi3b=100 AND ehi4b=100;
                                '''], # filter by handedness
            'tbss01': ['tbss', '''
                                    SELECT DISTINCT subjectkey FROM tbss01
                                    WHERE nihtbx_picvocab_fc>44
                                    AND nihtbx_flanker_fc>44
                                    AND nihtbx_list_fc>44
                                    AND nihtbx_cardsort_fc>44
                                    AND nihtbx_pattern_fc>44
                                    AND nihtbx_picture_fc>44
                                    AND nihtbx_reading_fc>44
                                    AND nihtbx_fluidcomp_fc>44
                                    AND nihtbx_cryst_fc>44
                                    AND nihtbx_totalcomp_fc>44;
                                '''] # filter by cognitive test scores
        }
