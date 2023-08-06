'''
Created on 2021-04-06

@author: wf
'''
import re
from ormigrate.fixer import PageFixer
from ormigrate.rating import Rating
from ormigrate.toolbox import HelperFunctions as hf


class DateFixer(PageFixer):
    '''
    fixer for Date being incorrect
    https://github.com/SmartDataAnalytics/OpenResearch/issues/71
    '''

    def __init__(self, wikiClient, debug=False,restoreOut=False):
        '''
        Constructor
        '''
        # call super constructor
        super(DateFixer, self).__init__(wikiClient)
        self.debug = debug
        self.restoreOut = restoreOut

    def fixEventRecord(self, event, datelist=['Start date' , 'End date'], errors=None):
        if errors is None:
            errors={}
        for element in datelist:
            eventDate = event.get(element)
            if eventDate is not None:
                fixedDate = hf.parseDate(eventDate)
                if fixedDate is not None:
                    if fixedDate != eventDate:
                        event[element] = fixedDate
                else:
                    errors['fixNotPossible']=True
            else:
                key= element+'notFound'
                errors[key]= True
        if self.debug and errors.get('fixNotPossible'): print(self.generateLink(event['pageTitle']))
        return event,errors


    def getFixedDateWikiFile(self, page, event, datetype='date'):
        '''
        fix the date of the given page and event and mark unfixable pages
        Returns:
            Fixed text of the page.
        '''
        generateLink=False
        change=False
        dates = re.findall('|.*'+datetype+'.*=.*\n', event)
        if len(dates) != 0:
            for element in dates:
                name,value=self.getNameValue(element)
                if name is not None and value is not None:
                    fixedDate = hf.parseDate(value)
                    if fixedDate is not None:
                        if fixedDate != value:
                            change = True
                        event = event.replace(element,'|'+name+'='+fixedDate)
                    else:
                        generateLink=True
        if self.debug and generateLink: print(self.generateLink(page))
        if change:
            return event
        else:
            return None

    @classmethod
    def getRating(self,eventRecord):
        painrating= None
        startDate = None
        endDate = None
        if 'startDate' in eventRecord: startDate = eventRecord['startDate']
        if 'endDate' in eventRecord: endDate = eventRecord['endDate']

        if startDate is not None and endDate is not None:
            painrating= Rating(1,Rating.ok,f'Dates,  {startDate} , {endDate} valid')
        elif startDate is None and endDate is None:
            painrating=Rating(5,Rating.missing,f'Dates not found')
        elif startDate is None and endDate is not None:
            painrating=Rating(7,Rating.missing,f'Start Date is not there while end date exists')
        elif startDate is not None and endDate is None:
            painrating=Rating(3,Rating.missing,f'Start Date is there but end date is not')
        return painrating





if __name__ == "__main__":
    fixer = DateFixer()
    fixer.debug = True
    # fixer.checkAllFiles(fixer.getFixedDate, 'deadline')
    fixer.fixAllFiles(fixer.getFixedDateWikiFile, "Date", 'date')
    fixer.fixAllFiles(fixer.getFixedDateWikiFile, "Deadline", 'deadline')
