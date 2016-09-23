# -*- coding: utf-8 -*-

'''
Created on 5 de nov. de 2015

@author: Oliver Careaga
'''

import json
from database import Database

# ---------------------------------------- Functions ----------
def getPositions(pageData, currentRow):
    '''
    Increase counter for each row with same article, code, and parent.

    @param {List} pageData
    @param {Array} currentRow

    @return {int} - Number of positions.
    '''
    positions = 0

    for row in pageData:
        if row[1] == currentRow[1] and row[2] == currentRow[2] and row[3] == currentRow[3]:
            positions += 1

    return positions

def getChildren(pageData, currentRow):
    '''
    Create a list of row children using recursion.

    @param {List} pageData
    @param {Array} currentRow
    @param {List} children

    @return {List} - List representation of row children.
    '''
    children = {}

    for row in pageData:
        # Same level contents
        if row[1] == currentRow[1] and row[3] == currentRow[0]:
            # If has description - Value row
            if row[5] is not None:
                # If hasn't index - String
                if row[4] is None:
                    children[row[2]] = row[5]
                # If has index - Array of strings
                elif row[2] not in children:
                    # Create array and insert string
                    children[row[2]] = [0] * getPositions(pageData, row)
                    children[row[2]][row[4]] = row[5]
                else:
                    children[row[2]][row[4]] = row[5]
            # If hasn't description - Structural row
            else:
                # If hasn't index - Dictionary
                if row[4] is None:
                    children[row[2]] = getChildren(pageData, row)
                # If has index - Array of dictionaries
                elif row[2] not in children:
                    # Create array and call 'getChildren' function
                    children[row[2]] = [0] * getPositions(pageData, row)
                    children[row[2]][row[4]] = getChildren(pageData, row)
                else:
                    children[row[2]][row[4]] = getChildren(pageData, row)

    return children

# ---------------------------------------- Class ----------
class Multilingual:
    '''
    Tools for multilingual management.
    '''

    def __init__(self, database):
        '''
        @param {string} database

        Attributes

        db {Database}
        '''
        self.db = Database(database)

    def getPageObject(self, pageCode, languageCode):
        '''
        Request list-data from a page and format them to JSON object.

        row[0] - content.idcontent
        row[1] - article.code
        row[2] - content.code
        row[3] - content.parent
        row[4] - content.index
        row[5] - description.plaintext

        @param {string} pageCode
        @param {string} languageCode

        @return {List} - List representation of page.
        '''
        pageObject = {}
        pageData = self.db.getPageData(pageCode, languageCode)

        # Console reference
        for row in pageData:
            print(row)

        for row in pageData:
            # Add article
            if row[1] not in pageObject:
                pageObject[row[1]] = {}

            # Add content
            # If hasn't parent - First level contents
            if row[3] is None:
                # If has description - Value row
                if row[5] is not None:
                    # If hasn't index - String
                    if row[4] is None:
                        pageObject[row[1]][row[2]] = row[5]
                    # If has index - Array of strings
                    elif row[2] not in pageObject[row[1]]:
                        # Create array and insert string
                        pageObject[row[1]][row[2]] = [0] * getPositions(pageData, row)
                        pageObject[row[1]][row[2]][row[4]] = row[5]
                    else:
                        pageObject[row[1]][row[2]][row[4]] = row[5]
                # If hasn't description - Structural row
                else:
                    # If hasn't index - Dictionary
                    if row[4] is None:
                        pageObject[row[1]][row[2]] = getChildren(pageData, row)
                    # If has index - Array of dictionaries
                    elif row[2] not in pageObject[row[1]]:
                        # Create array and call 'getChildren' function
                        pageObject[row[1]][row[2]] = [0] * getPositions(pageData, row)
                        pageObject[row[1]][row[2]][row[4]] = getChildren(pageData, row)
                    else:
                        pageObject[row[1]][row[2]][row[4]] = getChildren(pageData, row)

        return json.dumps(pageObject, ensure_ascii=False)
