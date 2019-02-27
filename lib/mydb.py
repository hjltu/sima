#!/usr/bin/env python3

"""
20-oct-17 - 16-feb-19 hjltu@ya.ru
mydb.py contain methods for sqlite3 operations:

create(dbName, tbNname) - create new table
    options: dbName - base name, tbName - table name
drop(dbName, tbNname) - drop table
    options: dbName - base name, tbName - table name
insert(dbName, tbNname, name, stat) - insert new row
    option: dbName - base name, tbName - table name,
        name - column, stat - status
select(dbName, tbNname, name) - query stat_value from row where name = names
    option: dbName - base name, tbName - table name, name - column_name
select_all(dbName, tbNname) - query for all names and stat
    options: dbName - base name, tbName - table name
update(dbName, tbNname, name, status) - update where_name = name and
        if new_status != status
    options: dbName - base name, tbName - table name,
        name - column1, status - column2
delete(dbName, tbNname, name) - delete row where_name
    option: dbName - base name, tbName - table name, name - column

name:   user_id(string, yandex device id)
stat:   sn(integer, RPi serial number)
"""

import sqlite3,time

DB = "id.db"
TB = "id"

def create(dbName=DB, tbName=TB):
    tbSchema='id INTEGER PRIMARY KEY, name TEXT, stat INTEGER, date TEXT'
    query=('CREATE TABLE '+tbName+'('+tbSchema+')')
    db=sqlite3.connect(dbName)
    cursor=db.cursor()
    try:
        cursor.execute(query)
    except:
        db.rollback()
        return 1
    db.commit()
    db.close()
    return 0

def drop(dbName=DB, tbName=TB):
    query=('DROP TABLE '+tbName)
    db=sqlite3.connect(dbName)
    cursor=db.cursor()
    try:
        cursor.execute(query)
    except:
        db.rollback()
        return 1
    db.commit()
    db.close
    return 0

def insert(dbName=DB, tbName=TB, name='test', stat=None):
    query=('SELECT name FROM '+tbName+' WHERE name = ?')
    db=sqlite3.connect(dbName)
    cursor=db.cursor()
    try:
        cursor.execute(query, (name,))
    except:
        return 1
    rows=cursor.fetchone()
    if rows is None:
        query=('INSERT INTO '+tbName+'(name, stat, date) VALUES(?,?,?)')
        tm=time.ctime()
        try:
            cursor.execute(query, (name, stat, tm))
        except:
            db.rollback()
            return 2
        db.commit()
        db.close()
        return 0
    else:
        db.close()
        return 3

def select(dbName=DB, tbName=TB, name='test'):
    query=('SELECT stat FROM '+tbName+' WHERE name = ?')
    db=sqlite3.connect(dbName)
    cursor=db.cursor()
    try:
        cursor.execute(query, (name,))
    except:
        return 1
    rows=cursor.fetchone()
    if rows is None:
        db.close()
        return 2
    else:
        db.close()
        return str(rows[0])

def select_last(dbName=DB, tbName=TB):
    query=('SELECT stat FROM '+tbName+' WHERE id = (SELECT MAX(id)  FROM '+tbName+')')
    db=sqlite3.connect(dbName)
    cursor=db.cursor()
    try:
        cursor.execute(query)
    except:
        return 1
    rows=cursor.fetchone()
    if rows is None:
        db.close()
        return 2
    else:
        db.close()
        return str(rows[0])

def select_between(dbName=DB, tbName=TB, col='test', first=None, last=None):
    query=('SELECT '+col+',stat FROM '+tbName+' WHERE '+col+' BETWEEN '+\
        str(first)+' AND '+str(last))
    db=sqlite3.connect(dbName)
    cursor=db.cursor()
    try:
        cursor.execute(query)
    except:
        return 1
    rows=cursor.fetchall()
    if rows is None:
        db.close()
        return 2
    else:
        db.close()
        return dict(rows)


def select_all(dbName=DB, tbName=TB):
    query=('SELECT name,stat FROM '+tbName+'')
    db=sqlite3.connect(dbName)
    cursor=db.cursor()
    try:
        cursor.execute(query)
    except:
        return 1
    rows=cursor.fetchall()
    if rows is None:
        db.close()
        return 2
    else:
        db.close()
        return dict(rows)

def update(dbName=DB, tbName=TB, name='test', stat=None):
    query=('SELECT stat FROM '+tbName+' WHERE name = ?')
    db=sqlite3.connect(dbName)
    cursor=db.cursor()
    try:
        cursor.execute(query, (name,))
    except:
        return 1
    rows=cursor.fetchone()
    if rows is None:
        db.close()
        return 2
    else:
        if rows[0] != stat:
            query=('UPDATE '+tbName+' SET stat = ?, date = ? WHERE name = ?')
            try:
                cursor.execute(query, (stat, time.ctime(),name))
            except:
                db.rollback()
                return 3
            db.commit()
            db.close()
            return 0
        else:
            db.close()
            return 4

def delete(dbName=DB, tbName=TB, name='test'):
    db=sqlite3.connect(dbName)
    cursor=db.cursor()
    try:
        cursor.execute('SELECT name FROM '+tbName+' WHERE name = ?', (name,))
    except:
        return 1
    rows=cursor.fetchone()
    if rows is None:
        db.close()
        return 2
    else:
        if str(rows[0]) == name:
            try:
                cursor.execute('DELETE FROM '+tbName+' WHERE name = ? ', (name,))
            except:
                db.rollback()
                return 3
            db.commit()
            db.close()
            return 0
        else:
            db.close()
            return 4


import unittest

class TestStringMethods(unittest.TestCase):

    def test_mydb(self):
        # self.assertEqual(create(), 0)
        # self.assertEqual(insert(), 0)
        # self.assertNotEqual(select(), 1)
        # self.assertNotEqual(select(), 2)
        # self.assertNotEqual(selectall(), 1)
        # self.assertNotEqual(selectall(), 2)
        # self.assertEqual(update(), 0)
        # self.assertEqual(delete(), 0)
        # self.assertEqual(drop(), 0)
        print('all tests done')

if __name__=='__main__':
    unittest.main()
