import unittest

# Импорты всех тестовых классов
from tests.test_coffman import TestCoffmanGraham
from tests.test_fujii import TestFujiiScheduler
from tests.test_sethi import TestSethiUllman
from tests.test_gabow import TestGabowSCC

def run_all_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Добавляем тесты вручную
    suite.addTests(loader.loadTestsFromTestCase(TestCoffmanGraham))
    suite.addTests(loader.loadTestsFromTestCase(TestFujiiScheduler))
    suite.addTests(loader.loadTestsFromTestCase(TestSethiUllman))
    suite.addTests(loader.loadTestsFromTestCase(TestGabowSCC))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

if __name__ == "__main__":
    run_all_tests()