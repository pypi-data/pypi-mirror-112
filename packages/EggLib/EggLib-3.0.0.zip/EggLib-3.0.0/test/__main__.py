import sys, getopt,egglib, unittest, importlib, os
from datetime import datetime
import test_modules

HELP = """Copyright 2012-2020 Stephane De Mita, Mathieu Siol, Thomas Coudoux

Test_EggLib module 

EggLib is free software: you can redistribute it and/or modify it under the terms
of the GNU General Public License as published bythe Free Software Foundation, 
either version 3 of the License, or (at your option) any later version.

EggLib is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
PURPOSE. See the GNU General Public License for more details.

usage: python -m test_egglib [options] [-h | -b | -i ...] [-o --output] <file_name>

options and arguments:
-a --all	: Perform all tests (excludes --test-stats)
-b --base	: This option, allow to launch tests on the class: "SampleView", 
   		  "SequenceView", "GroupView", "Database", "Align" and "Container". 
		  Each methods and constructors of this classes are tested
-i --io		: This option, allow to launch tests on the class: "Fasta_iter", 
 		  "GenbankFeatureLocatioin", "GenbankFeature", "Genbank", "GFF3", 
		  "GFF3Feature", "VcfParser" and "Variant". But also on methods of 
		  files: "_legacy.py" and "_export.py".
		  Each methods and constructors of this classes are tested.
-c --coalesce	: This option, allow to launch tests on the class: "ParamDict", 
 		  "ParamList", "ParamMatrix" and "EventList".
		  Each methods and constructors of this classes are tested.
-t --tools	: This option, allow to launch tests on the class: "Translator", 
		  "BackAlignError", "Discretize", "Random", "ReadingFrame". 
		  But also on methods of files: "_code_tools.py", "_concact.py" and
		  "_seq_manip.py".
		  Each methods and constructors of this classes are tested.
-s --stats	: This option, allow to launch tests on the class:"ProbaMisoriented",
		  "CodingDiversity", "ComputeStats", "EHH", "Filter", "Freq", 
		  "ParalogPi", "Site", "Iterator" and "Structure".
		  But also on methods of files: "_freq.py", "_paralog_pi.py",
		  "_haplotypes.py", "_ld.py" and "_structure.py".
-w --wrappers	: This option, allow to launch tests on the wrappers module.
-k --custom	: Custom list of tests (comma-separated).
-o --output	: This option, allows to get the bad results of test (errors and failures) 
		  in a file specified by the user as argument <file_name> of the option
		  "output". If the file name contains the string "{timestamp}", the time
          stamp is inserted.
-h --help	: Show help information on the module test_egglib.
--test-stats	: Print results of comparison of statistics value (no actual tests).

Beware:	Only the option [-o | --output] needs an argument.
	If you pass two or more options at the same time, all tests will be executed.
	If you pass no option, the menu interface of test_egglib will be open [-m ]
"""

tests = {}
tests_dict = {}
n = 0
for pkg, lbl in [(test_modules.test_base, 'base'),
                 (test_modules.test_coalesce, 'coalesce'),
                 (test_modules.test_io, 'io'),
                 (test_modules.test_stats, 'stats'),
                 (test_modules.test_tools, 'tools'),
                 (test_modules.test_wrappers, 'wrappers')]:
    tests[lbl] = []
    for i in dir(pkg):
        if i[:5] == 'test_':
            mod = importlib.import_module(i, 'test_modules.test_' + lbl)
            for j in dir(mod):
                if j[-5:] == '_test':
                    obj = getattr(mod, j)
                    tests[lbl].append(obj)
                    assert j[:-5] not in tests_dict
                    tests_dict[j[:-5]] = obj
                    n += 1
assert sum([len(tests[i]) for i in tests]) == n

def print_test_file(fname, test_name, suite):
    date= datetime.now().strftime('%Y-%m-%d %H:%M')
    counter = 0
    with open(fname, "a") as my_file:
        print('----------------------------------------------------------------------')
        print(test_name)
        runner=unittest.TextTestRunner(verbosity = 0).run(suite)
        err=runner.errors
        fail=runner.failures
        counter += len(err)+len(fail)

        if len(err)+len(fail) > 0:

            my_file.write(">>> "+test_name+": "+date+"\n")
            my_file.write("======================================================================\n")
            my_file.write("---ERROR: ")		
            if(len(err)!=0):
                my_file.write('\n'.join('%s %s' % i for i in err))
            else:
                my_file.write('\tNO ERROR DETECTED\n')

            my_file.write("\n---FAIL: ")
            if(len(fail)!=0):
                my_file.write('\n'.join('%s %s' % i for i in fail))
            else:
                my_file.write('\tNO FAILURE DETECTED\n')
            my_file.write("======================================================================\n\n")

    my_file.close()
    return counter

try:
    opts, args = getopt.getopt(sys.argv[1:], "habictswmk:o:", [ "help", 'all', "base", "io", "coalesce", "tools", "stats", "wrappers", "custom=", "output=", 'test-stats'] )
except getopt.GetoptError as e:
    print(HELP)
    print('error:', str(e))
    sys.exit(2)
if len(args):
    print(HELP)
    print('invalid option(s): ' + ' '.join(args))
    sys.exit(2)

output = ""
has_output = False
test_stats = False
tests_list = []

for opt, arg in opts:
    if opt in ("-h", "--help"):
        print(HELP)
        sys.exit(1)

    elif opt == '--test-stats':
        test_stats = True

    elif opt in ("-o", "--output"):
        now = datetime.now()
        ts = '{0}-{1:0>2}-{2:0>2}_{3:0>2}:{4:0>2}:{5:0>3}.{6:0>6}'.format(now.year, now.month,
                now.day, now.hour, now.minute, now.second, now.microsecond)
        output = arg.format(timestamp=ts)
        with open(output, "w") as my_file: pass                
        has_output=True

    elif opt in ("-a", "--all"):
        for k in sorted(tests):
            tests_list.extend(tests[k])

    elif opt in ("-b", "--base"):
        tests_list.extend(tests['base'])

    elif opt in ("-i", "--io"):
        tests_list.extend(tests['io'])

    elif opt in ("-c", "--coalesce"):
        tests_list.extend(tests['coalesce'])

    elif opt in ("-t", "--tools"):
        tests_list.extend(tests['tools'])

    elif opt in ("-w", "--wrappers"):
        tests_list.extend(tests['wrappers'])

    elif opt in ("-s", "--stats"):
        tests_list.extend(tests['stats'])

    elif opt in ('-k', '--custom'):
        invalid = []
        for i in arg.split(','):
            if i not in tests_dict: invalid.append(i)
            else: tests_list.append(tests_dict[i])
        if len(invalid): sys.exit('invalid component(s): ' + ', '.join(invalid))

total_errors = 0

if test_stats:
    if len(tests_list): sys.exit('error: --test-stats is incompatible with other options')
    if has_output: sys.exit('error: --test-stats is incompatible with other options')
    test = test_modules.test_stats.test_cstats.Statistics_test()
    test.setUp()
    test._run_test(True)
elif has_output:
    for i in tests_list:
        test_name = i.__name__
        suite = unittest.TestLoader().loadTestsFromTestCase(i)
        total_errors += print_test_file(output, test_name, suite)
    print('total errors:', total_errors)
elif len(tests_list) > 0:
    for i in tests_list:
        suite = unittest.TestLoader().loadTestsFromTestCase(i)
        runner = unittest.TextTestRunner(verbosity=2).run(suite)
        total_errors += len(runner.errors) + len(runner.failures)
    print('total errors:', total_errors)
else:
    print(HELP)
