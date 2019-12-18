import unittest

from typepractice import TypePractice

class TestTypePractice(unittest.TestCase):

    def setUp(self):
        self.t1 = TypePractice.startClicked()


    def testStart(self):
        self.assertEqual(self.t1.correctrate, 0)
        self.assertEqual(self.t1.correctLb.text(), '0')
        self.assertEqual(self.t1.remainingTime.text(), '60')
