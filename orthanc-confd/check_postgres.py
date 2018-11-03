#!/usr/bin/python

# Check for pg database connection, create database if missing

import psycopg2
import argparse

def parse_args():

    p = argparse.ArgumentParser()
    p.add_argument('-H', '--host', default='localhost')
    p.add_argument('-p', '--port', default='5432')
    p.add_argument('-u', '--user', default='postgres')
    p.add_argument('-w', '--password', default='password')
    p.add_argument('-d', '--database', default='orthanc')

    return p.parse_args()


if __name__=="__main__":

    opts = parse_args()
    try:
        con = psycopg2.connect(database=opts.database,
                            user = opts.user,
                            password = opts.password,
                            host = opts.host,
                            port = opts.port )

        print("Opened database '{0}' successfully".format( opts.database ))
        exit()

    except Exception as e:
        print("Failed to open db")
        print(e)

    try:
        con = psycopg2.connect(
                            user = opts.user,
                            password =opts.password,
                            host = opts.host,
                            port = opts.port )
        con.autocommit = True

        cur = con.cursor()
        cur.execute('CREATE DATABASE {};'.format(opts.database))
        print("Created db")
        exit()

    except Exception as e:
        print("Failed to create db")
        raise(e)
