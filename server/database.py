# -*- coding: utf-8 -*-

'''
Created on 5 de nov. de 2015

@author: Oliver Careaga, Xabier Casado
'''

import mysql.connector

# ---------------------------------------- Functions ----------

# ---------------------------------------- Class ----------
class Database:
    '''
    Connection and tools for database management.
    '''

    def __init__(self, database, host='127.0.0.1', user='root', password='investime'):
        '''
        @param {string} database
        @param {string} host
        @param {string} user
        @param {string} password

        Attributes

        connection {mysql.connector.connect()}
        cursor {mysql.connector.connect().cursor()}
        '''
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.connection.cursor()

        except (mysql.connector.errors.ProgrammingError, mysql.connector.errors.InterfaceError) as e:
            print('# ERROR [' + type(e).__name__ + ']: ' + e.msg)

            self.connection = None
            self.cursor = None

    def getPageData(self, pageCode, languageCode):
        '''
        Data return of established page and language.

        @param {string} pageCode
        @param {string} languageCode

        @return {string} - Query result with requested page data.
        '''

        self.cursor.execute('SELECT c.idcontent, a.code, c.code, c.parent, c.index, d.plaintext ' +
                            'FROM language la, page p ' +
                                'JOIN located lo ON p.idpage = lo.idpage ' +
                                'JOIN article a ON lo.idarticle = a.idarticle ' +
                                'JOIN content c ON a.idarticle = c.idarticle ' +
                                'LEFT JOIN description d ON c.idcontent = d.idcontent ' +
                            'WHERE ((d.plaintext IS NOT NULL AND d.idlanguage = la.idlanguage) ' +
                                    'OR (c.index IS NOT NULL AND d.plaintext IS NULL) ' +
                                    'OR (c.index IS NULL AND d.plaintext IS NULL)) ' +
                                'AND p.code = "' + pageCode + '" ' +
                                'AND la.abbr = "' + languageCode + '"'
                            )

        pageData = self.cursor.fetchall()

        return pageData
