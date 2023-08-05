#datasetdivisiontest.py

TestTif = ep.Dataset('Test', imagetype='stack', path='C:\\Users\\conor\\Desktop\\TestStack\\BLA\\E00010\\1' )

TestTif.divide(TestTif.data[10])