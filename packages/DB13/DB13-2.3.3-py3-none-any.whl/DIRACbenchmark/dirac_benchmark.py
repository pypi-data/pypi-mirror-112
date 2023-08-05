
""" DIRAC Benchmark 2012 by Ricardo Graciani, and wrapper functions to
    run multiple copies in parallel by Andrew McNab.
    This file (dirac_benchmark.py) is intended to be the ultimate upstream
    shared by different users of the DIRAC Benchmark 2012 (DB12). The
    canonical version can be found at https://github.com/DIRACGrid/DB12
    This script can either be imported or run from the command line:
    ./dirac_benchmark.py NUMBER
    where NUMBER gives the number of benchmark processes to run in parallel.
    Run  ./dirac_benchmark.py help  to see more options.
"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os
import sys
import random
import multiprocessing

VERSION = "1.0.0 DB12"

if sys.version_info[0] >= 3:
    #pylint: disable = E, W, R, C
    long = int 
    xrange = range
    import urllib.request
    urllib = urllib.request

else:
    import urllib


def single_dirac_benchmark(iterations_num=1, measured_copies=None):
    """Get Normalized Power of one CPU in DIRAC Benchmark 2012 units (DB12)"""

    # This number of iterations corresponds to 1kHS2k.seconds, i.e. 250 HS06 seconds

    iters = int(1000 * 1000 * 12.5)
    calib = 250.0

    m_1 = long(0)
    m_2 = long(0)
    p_1 = 0
    p_2 = 0
    # Do one iteration extra to allow CPUs with variable speed (we ignore zeroth iteration)
    # Do one or more extra iterations to avoid tail effects when copies run in parallel
    it_1 = 0
    while (it_1 <= iterations_num) or (
            measured_copies is not None and measured_copies.value > 0
    ):
        if it_1 == 1:
            start = os.times()

        # Now the iterations
        for _j in xrange(iters):
            t_1 = random.normalvariate(10, 1)
            m_1 += t_1
            m_2 += t_1 * t_1
            p_1 += t_1
            p_2 += t_1 * t_1

        if it_1 == iterations_num:
            end = os.times()
            if measured_copies is not None:
                # Reduce the total of running copies by one
                measured_copies.value -= 1

        it_1 += 1

    cput = sum(end[:4]) - sum(start[:4])
    wall = end[4] - start[4]

    if not cput:
        return None

    # Return DIRAC-compatible values
    return {
        "CPU": cput,
        "WALL": wall,
        "NORM": calib * iterations_num / cput,
        "UNIT": "DB12",
    }


def single_dirac_benchmark_process(result_object, iterations_num=1, measured_copies=None):

    """Run single_dirac_benchmark() in a multiprocessing friendly way"""

    benchmark_result = single_dirac_benchmark(
        iterations_num=iterations_num, measured_copies=measured_copies
    )

    if not benchmark_result or "NORM" not in benchmark_result:
        return

    # This makes it easy to use with multiprocessing.Process
    result_object.value = benchmark_result["NORM"]


def multiple_dirac_benchmark(copies=1, iterations_num=1, extra_iter=False):

    """Run multiple copies of the DIRAC Benchmark in parallel"""

    processes = []
    results = []

    if extra_iter:
        # If true, then we run one or more extra iterations in each
        # copy until the number still being meausured is zero.
        measured_copies = multiprocessing.Value("i", copies)
    else:
        measured_copies = None

    # Set up all the subprocesses
    for i in xrange(copies):
        results.append(multiprocessing.Value("d", 0.0))
        processes.append(
            multiprocessing.Process(
                target=single_dirac_benchmark_process,
                args=(results[i], iterations_num, measured_copies),
            )
        )

    # Start them all off at the same time
    for process in processes:
        process.start()

    # Wait for them all to finish
    for process in processes:
        process.join()

    raw = []
    product = 1.0

    for res in results:
        raw.append(res.value)
        product *= res.value

    raw.sort()

    # Return the list of raw results and various averages
    return {
        "raw": raw,
        "copies": copies,
        "sum": sum(raw),
        "arithmetic_mean": sum(raw) / copies,
        "geometric_mean": product ** (1.0 / copies),
        "median": raw[(copies - 1) // 2],
    }


def wholenode_dirac_benchmark(copies=None, iterations_num=1, extra_iter=False):

    """Run as many copies as needed to occupy the whole machine"""

    # If not given by caller then just count CPUs
    if copies is None:
        try:
            copies = multiprocessing.cpu_count()
        except: # pylint: disable=bare-except
            copies = 1

    return multiple_dirac_benchmark(
        copies=copies, iterations_num=iterations_num, extra_iter=extra_iter
    )


def jobslot_dirac_benchmark(copies=None, iterations_num=1, extra_iter=False):

    """Run as many copies as needed to occupy the job slot"""

    # If not given by caller then just run one copy
    if copies is None:
        copies = 1

    return multiple_dirac_benchmark(
        copies=copies, iterations_num=iterations_num, extra_iter=extra_iter
    )

def main():
    "Main function"
    help_string = """dirac_benchmark.py [--iterations ITERATIONS] [--extra-iteration]
                  [COPIES|single|wholenode|jobslot|version|help] 
Uses the functions within dirac_benchmark.py to run the DB12 benchmark from the 
command line.
By default one benchmarking iteration is run, in addition to the initial 
iteration which DB12 runs and ignores to avoid ramp-up effects at the start.
The number of benchmarking iterations can be increased using the --iterations
option. Additional iterations which are also ignored can be added with the 
--extra-iteration option  to avoid tail effects. In this case copies which
finish early run additional iterations until all the measurements finish.
The COPIES (ie an integer) argument causes multiple copies of the benchmark to
be run in parallel. The tokens "wholenode", "jobslot" and "single" can be 
given instead to use $MACHINEFEATURES/total_cpu, $JOBFEATURES/allocated_cpu, 
or 1 as the number of copies respectively. If $MACHINEFEATURES/total_cpu is
not available, then the number of (logical) processors visible to the 
operating system is used.
Unless the token "single" is used, the script prints the following results to
two lines on stdout:
COPIES SUM ARITHMETIC-MEAN GEOMETRIC-MEAN MEDIAN
RAW-RESULTS
The tokens "version" and "help" print information about the script.
The source code of dirac_benchmark.py provides examples of how the functions
within dirac_benchmark.py can be used by other Python programs.
dirac_benchmark.py is distributed from  https://github.com/DIRACGrid/DB12
"""

    copies = None
    iterations = 1
    extra_iteration = False

    for arg in sys.argv[1:]:
        if arg.startswith("--iterations="):
            iterations = int(arg[13:])
        elif arg == "--extra-iteration":
            extra_iteration = True
        elif arg in ("--help", "help"):
            print(help_string)
            sys.exit(0)
        elif not arg.startswith("--"):
            copies = arg

    if copies == "version":
        print(VERSION)
        sys.exit(0)

    if copies is None or copies == "single":
        print(single_dirac_benchmark()["NORM"])
        sys.exit(0)

    if copies == "wholenode":
        result = wholenode_dirac_benchmark(
            iterations_num=iterations, extra_iter=extra_iteration
        )
        print(
            result["copies"],
            result["sum"],
            result["arithmetic_mean"],
            result["geometric_mean"],
            result["median"],
        )
        print(" ".join([str(j) for j in result["raw"]]))
        sys.exit(0)

    if copies == "jobslot":
        result = jobslot_dirac_benchmark(
            iterations_num=iterations, extra_iter=extra_iteration
        )
        print(
            result["copies"],
            result["sum"],
            result["arithmetic_mean"],
            result["geometric_mean"],
            result["median"],
        )
        print(" ".join([str(j) for j in result["raw"]]))
        sys.exit(0)

    result = multiple_dirac_benchmark(
        copies=int(copies), iterations_num=iterations, extra_iter=extra_iteration
    )
    print(
        result["copies"],
        result["sum"],
        result["arithmetic_mean"],
        result["geometric_mean"],
        result["median"],
    )
    print(" ".join([str(k) for k in result["raw"]]))
    sys.exit(0)

#
# If we run as a command
#
if __name__ == "__main__":
    main()
