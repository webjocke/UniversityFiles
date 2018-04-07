#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2011, IDA, Linköping University
# Copyright (C) 2011, Torbjörn Lönnemark <tobbez@ryara.net>
# Copyright (C) 2014, Daniel Persson
import unittest
import data
import hashlib
import sys
from operator import itemgetter

def print_tech_dict(d):
    for k,v in d.items():
        print("{}: {}".format(k,v))
        for e in v:
            print(e)
        print()

def sort_dict(d,sort_key):
    for k in d.keys():
        d[k] = sorted(d[k], key = itemgetter(sort_key))
    return d;

md5 = hashlib.md5
class DataTest(unittest.TestCase):
    def setUp(self):
        self.expected_data = [{"start_date": "2009-09-05",
                              "short_description": "no",
                              "course_name": "OK\u00c4NT",
                              "long_description": "no no no",
                              "group_size": 2,
                              "academic_credits": "WUT?",
                              "lulz_had": "many",
                              "external_link": "YY",
                              "small_image": "X",
                              "techniques_used": [
                                  "python"
                              ],
                              "project_name": "python data-module test script",
                              "course_id": "TDP003",
                              "end_date": "2009-09-06",
                              "project_id": 1,
                              "big_image": "XXX"
                              },
                              {"start_date": "2016-09-05",
                               "short_description": "En JÄÄÄÄÄÄÄTTEEEEE FUL beskrivning",
                               "course_name": "TDP008",
                               "long_description": "Fin fin looove it",
                               "group_size": 23,
                               "academic_credits": "NONE",
                               "lulz_had": "too little",
                               "external_link": "http://hej.se",
                               "small_image": "sdkjf",
                               "techniques_used": [
                                  "python",
                                  "html"
                                ],
                                "project_name": "Finaste projektet någonsin",
                                "course_id": "TDP008",
                                "end_date": "2016-09-20",
                                "project_id": 99,
                                "big_image": "XXXdf"},
                               {"start_date": "2009-09-07",
                                "short_description": "no",
                                "course_name": "OK\u00c4NT",
                                "long_description": "no no no",
                                "group_size": 4,
                                "academic_credits": "WUT?",
                                "lulz_had": "few",
                                "external_link": "YY",
                                "small_image": "X",
                                "techniques_used": [
                                  "c++",
                                  "csv",
                                  "python"
                                ],
                                "project_name": "NEJ",
                                "course_id": "TDP003",
                                "end_date": "2009-09-08",
                                "project_id": 3,
                                "big_image": "XXX"},
                               {"start_date": "2009-09-08",
                                "short_description": "no",
                                "course_name": "OK\u00c4NT",
                                "long_description": "no no no",
                                "group_size": 6,
                                "academic_credits": "WUT?",
                                "lulz_had": "medium",
                                "external_link": "YY",
                                "small_image": "X",
                                "techniques_used": [
                                  "ada",
                                  "python"
                                ],
                                "project_name": "2007",
                                "course_id": "TDP003",
                                "end_date": "2009-09-09",
                                "project_id": 2,
                                "big_image": "XXX"},
                               {"start_date": "2009-09-06",
                                "short_description": "no",
                                "course_name": "HOHO",
                                "long_description": "no no no",
                                "group_size": 8,
                                "academic_credits": "WUT?",
                                "lulz_had": "over 9000",
                                "external_link": "YY",
                                "small_image": "X",
                                "techniques_used": [],
                                "project_name": "test",
                                "course_id": " \"",
                                "end_date": "2009-09-07",
                                "project_id": 4,
                                "big_image": "XXX"}
                            ]

        self.expected_data = sorted(self.expected_data, key=itemgetter('project_id'))

        self.expected_technique_data = ['ada', 'c++', 'csv', 'html', 'python']
        self.expected_technique_stat_data = {'python': [{'id': 1, 'name': 'python data-module test script'},
                                                        {'id': 99, 'name': 'Finaste projektet någonsin'},
                                                        {'id': 3, 'name': 'NEJ'},
                                                        {'id': 2, 'name': '2007'}],
                                             'csv': [{'id': 3, 'name': 'NEJ'}],
                                             'c++': [{'id': 3, 'name': 'NEJ'}],
                                             'ada': [{'id': 2, 'name': '2007'}],
                                             'html': [{'id': 99, 'name': 'Finaste projektet någonsin' }]}
        self.loaded_data = sorted(data.load("data.json"), key=itemgetter('project_id'))

    def test_load(self):
        self.assertEqual(self.loaded_data[0], self.expected_data[0])
        self.assertEqual(data.load("/dev/this_file_does_not_exist"), None)

    def test_get_project_count(self):
        self.assertEqual(data.get_project_count(self.loaded_data), 5)
        
    def test_get_project(self):
        self.assertEqual(data.get_project(self.loaded_data, 99)['project_id'], 99)
        self.assertEqual(data.get_project(self.loaded_data, 3)['project_id'], 3)
        self.assertEqual(data.get_project(self.loaded_data, 2)['project_id'], 2)
        self.assertEqual(data.get_project(self.loaded_data, 4)['project_id'], 4)
        self.assertEqual(data.get_project(self.loaded_data, 42), None)

    def test_search(self):
        self.assertEqual(len(data.search(self.loaded_data)), 5)

        self.assertEqual(len(data.search(self.loaded_data, techniques=['csv'])), 1)

        res = data.search(self.loaded_data, sort_order='asc',techniques=["python"])
        self.assertEqual(res[0]['start_date'], '2009-09-05')
        self.assertEqual(res[1]['start_date'], '2009-09-07')
        self.assertEqual(res[2]['start_date'], '2009-09-08')
        self.assertEqual(res[3]['start_date'], '2016-09-05')


        res = data.search(self.loaded_data, 
                                     sort_by="end_date", 
                                     search='okänt', 
                                     search_fields=['project_id','project_name','course_name'])
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0]['project_id'], 2)
        self.assertEqual(res[1]['project_id'], 3)
        self.assertEqual(res[2]['project_id'], 1)
        
        res = data.search(self.loaded_data, 
                                     search="okänt", 
                                     search_fields=["project_id","project_name","course_name"])
        self.assertEqual(len(res), 3)

        res = data.search(self.loaded_data,
                                     techniques=[],
                                     search="okänt",
                                     search_fields=["project_id","project_name","course_name"])
        self.assertEqual(len(res), 3)

        res = data.search(self.loaded_data, search="okänt", search_fields=[])
        self.assertEqual(len(res), 0)
        res = data.search(self.loaded_data, sort_by='group_size')
        #default is descending order
        self.assertEqual(res[0]['project_id'], 99) #1
        self.assertEqual(res[1]['project_id'], 4) #2
        self.assertEqual(res[2]['project_id'], 2) #3
        self.assertEqual(res[3]['project_id'], 3) #4
        self.assertEqual(res[4]['project_id'], 1) #4

        res = data.search(self.loaded_data, search="okänt", search_fields=['whops'])
        self.assertEqual(len(res), 0)

        res = data.search(self.loaded_data, search="test", search_fields=['whops', 'project_name'])
        self.assertEqual(len(res), 2)

        res = data.search(self.loaded_data, search="NEJ", search_fields=['hej', 'boll', 'project_name'])
        self.assertEqual(len(res), 1)

        res = data.search(self.loaded_data, techniques=['ada', 'c++'])
        self.assertEqual(len(res), 0)

        res = data.search(self.loaded_data, techniques=['python'], search="HOHO", search_fields=['course_name'])
        self.assertEqual(len(res), 0)

    def test_get_techniques(self):
        res = data.get_techniques(self.loaded_data)
        self.assertEqual(res, self.expected_technique_data)

    def test_get_technique_stats(self):
        res = data.get_technique_stats(self.loaded_data)
        res = sort_dict(res,'id')
        
        self.expected_technique_stat_data = sort_dict(self.expected_technique_stat_data,'id')

        self.assertEqual(res, self.expected_technique_stat_data)


if __name__ == '__main__':
    print ("Test:     ", md5(sys.argv[0].encode('UTF-8')).hexdigest())
    print ("Test data:", md5(b"data.json").hexdigest())
    print()
    unittest.main()
