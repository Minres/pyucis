'''
Created on Nov 10, 2021

@author: mballance
'''
from _io import StringIO
from unittest.case import TestCase

from ucis.mem.mem_factory import MemFactory
from ucis.mem.mem_ucis import MemUCIS
from ucis.report.coverage_report_builder import CoverageReportBuilder
from ucis.yaml.yaml_reader import YamlReader
from ucis.merge.db_merger import DbMerger


class TestMerge(TestCase):

    def test_null_type_cg_1_cp(self):
        text = """
        coverage:
          covergroups:
          - type-name: cvg
               
            coverpoints:
            - name: cp1
              bins:
              - name: b0
                count: 1
              - name: b1
                count: 0
        """
        
        src_db = YamlReader().loads(StringIO(text))
        rpt = CoverageReportBuilder.build(src_db)
        
        self.assertEqual(len(rpt.covergroups), 1)
        self.assertEqual(rpt.covergroups[0].name, "cvg")
        self.assertEqual(len(rpt.covergroups[0].coverpoints), 1)
        self.assertEqual(len(rpt.covergroups[0].coverpoints[0].bins), 2)
        self.assertEqual(rpt.covergroups[0].coverpoints[0].coverage, 50.0)
        
        dst_db = MemFactory.create()

        merger = DbMerger(dst_db)
        merger.merge(src_db)
        
        rpt = CoverageReportBuilder.build(dst_db)
        
        self.assertEqual(len(rpt.covergroups), 1)
        self.assertEqual(rpt.covergroups[0].name, "cvg")
        self.assertEqual(len(rpt.covergroups[0].coverpoints), 1)
        self.assertEqual(len(rpt.covergroups[0].coverpoints[0].bins), 2)
        self.assertEqual(rpt.covergroups[0].coverpoints[0].coverage, 50.0)

    def test_null_inst_cg_1_cp(self):
        text = """
        coverage:
          covergroups:
          - type-name: cvg
               
            coverpoints:
            - name: cp1
              bins:
              - name: b0
                count: 1
              - name: b1
                count: 1
            covergroups:
            - type-name: cvg
              inst-name: inst1
                  
              coverpoints:
              - name: cp1
                bins:
                - name: b0
                  count: 0
                - name: b1
                  count: 1
                             
            - type-name: cvg
              inst-name: inst2
                   
              coverpoints:
              - name: cp1
                bins:
                - name: b0
                  count: 1
                - name: b1
                  count: 0
        """
        
        src_db = YamlReader().loads(StringIO(text))
        rpt = CoverageReportBuilder.build(src_db)
        
        self.assertEqual(len(rpt.covergroups), 1)
        self.assertEqual(rpt.covergroups[0].name, "cvg")
        self.assertEqual(len(rpt.covergroups[0].coverpoints), 1)
        self.assertEqual(len(rpt.covergroups[0].coverpoints[0].bins), 2)
        self.assertEqual(rpt.covergroups[0].coverpoints[0].coverage, 100.0)
        
        self.assertEqual(len(rpt.covergroups[0].covergroups), 2)
#        self.assertEqual(rpt.covergroups[0].name, "cvg")
        self.assertEqual(len(rpt.covergroups[0].covergroups[0].coverpoints), 1)
        self.assertEqual(len(rpt.covergroups[0].covergroups[0].coverpoints[0].bins), 2)
        self.assertEqual(rpt.covergroups[0].covergroups[0].coverpoints[0].coverage, 50.0)
        
#        self.assertEqual(rpt.covergroups[0].name, "cvg")
        self.assertEqual(len(rpt.covergroups[0].covergroups[1].coverpoints), 1)
        self.assertEqual(len(rpt.covergroups[0].covergroups[1].coverpoints[0].bins), 2)
        self.assertEqual(rpt.covergroups[0].covergroups[1].coverpoints[0].coverage, 50.0)
        
        dst_db = MemFactory.create()

        merger = DbMerger(dst_db)
        merger.merge(src_db)
        
        rpt = CoverageReportBuilder.build(dst_db)
        
        self.assertEqual(len(rpt.covergroups), 1)
        self.assertEqual(rpt.covergroups[0].name, "cvg")
        self.assertEqual(len(rpt.covergroups[0].coverpoints), 1)
        self.assertEqual(len(rpt.covergroups[0].coverpoints[0].bins), 2)
        self.assertEqual(rpt.covergroups[0].coverpoints[0].coverage, 100.0)
        self.assertEqual(len(rpt.covergroups[0].covergroups), 2)
#        self.assertEqual(rpt.covergroups[0].name, "cvg")
        self.assertEqual(len(rpt.covergroups[0].covergroups[0].coverpoints), 1)
        self.assertEqual(len(rpt.covergroups[0].covergroups[0].coverpoints[0].bins), 2)
        self.assertEqual(rpt.covergroups[0].covergroups[0].coverpoints[0].coverage, 50.0)
        
        self.assertEqual(len(rpt.covergroups[0].covergroups[1].coverpoints), 1)
        self.assertEqual(len(rpt.covergroups[0].covergroups[1].coverpoints[0].bins), 2)
        self.assertEqual(rpt.covergroups[0].covergroups[1].coverpoints[0].coverage, 50.0)




    