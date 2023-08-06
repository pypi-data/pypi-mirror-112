# -*- coding: UTF-8 -*-
import logging
from argparse import ArgumentParser, RawTextHelpFormatter
from ast import literal_eval
from os.path import exists
from time import perf_counter

from .__info__ import __author__, __credits__, __copyright__, __license__, __reference__, __source__, __version__
from .__init__ import PyPackerDetect


def valid_file(path):
    if not exists(path):
        raise ValueError("input file does not exist")
    return path


class Positive:
    def __init__(self, *types):
        self._types = types
    
    def __call__(self, string):
        try:
            n = literal_eval(string)
        except ValueError:
            raise ValueError(string)
        if not isinstance(n, self._types) or n < 0.:
            raise ValueError(string)
        return self._types[0](n)
    
    def __repr__(self):
        return "positive %s" % "|".join(map(lambda x: x.__name__, self._types))


def main():
    """ Tool's main function """
    descr = "PyPackerDetect {}\n\nAuthor   : {}\nCredits  : {}\nCopyright: {}\nLicense  : {}\nReference: {}\n" \
            "Source   : {}\n\nThis tool applies multiple checks for determining if a PE file is packed or not.\n" \
            "It supports two modes of operation, the first one for reporting findings and the second for deciding if" \
            " a PE file is packed using a scoring heuristic.\n\n"
    descr = descr.format(__version__, __author__, __credits__, __copyright__, __license__, __reference__, __source__)
    examples = "usage examples:\n- " + "\n- ".join([
        "pypackerdetect program.exe",
        "pypackerdetect program.exe -b",
        "pypackerdetect program.exe --low-imports --unknown-sections",
        "pypackerdetect program.exe --imports-threshold 5 --bad-sections-threshold 5",
    ])
    parser = ArgumentParser(description=descr, epilog=examples, formatter_class=RawTextHelpFormatter, add_help=False)
    parser.add_argument("path", type=valid_file, help="path to the portable executable")
    opt = parser.add_argument_group("optional arguments")
    opt.add_argument("-s", "--score", action="store_true",
                     help="if True, apply a scoring heuristic and decide whether the input executable is packed "
                             "using the input threshold ;\notherwise, simply report findings (this is the default)")
    opt.add_argument("--bad-ep-sections", action="store_false",
                     help="check for bad entry point sections (default: True)")
    opt.add_argument("--low-imports", action="store_false",
                     help="check for the number of imports (default: True)")
    opt.add_argument("--packer-sections", action="store_false",
                     help="check for packer sections (default: True)")
    opt.add_argument("--peid", action="store_false", help="detect with PEiD (default: True)")
    opt.add_argument("--peid-large-db", action="store_true", help="use the large database for PEiD (default: False)")
    opt.add_argument("--peid-ep-only", action="store_false", help="check only entry point signatures (default: True)")
    opt.add_argument("--unknown-sections", action="store_false",
                     help="check for unknown sections (default: True)")
    thrs = parser.add_argument_group("threshold arguments")
    thrs.add_argument("--bad-sections-threshold", dest="bst", type=Positive(int), default=2,
                      help="threshold for the number of bad sections (default: 2)")
    thrs.add_argument("--imports-threshold", dest="it", type=Positive(int), default=10,
                      help="threshold for the minimum number of imports (default: 10)")
    thrs.add_argument("--score-threshold", dest="st", type=Positive(float, int), default=1.,
                      help="threshold for the scoring heuristic (default: 1)")
    thrs.add_argument("--unknown-sections-threshold", dest="ust", type=Positive(int), default=3,
                      help="threshold for the number of unknown sections (default: 3)")
    extra = parser.add_argument_group("extra arguments")
    extra.add_argument("-b", "--benchmark", action="store_true",
                       help="enable benchmarking, output in seconds (default: False)")
    extra.add_argument("-h", "--help", action="help", help="show this help message and exit")
    extra.add_argument("-v", "--verbose", action="store_true", help="display debug information (default: False)")
    args = parser.parse_args()
    logging.basicConfig()
    args.logger = logging.getLogger("pypackerdetect")
    args.logger.setLevel([logging.INFO, logging.DEBUG][args.verbose])
    code = 0
    # execute the tool
    if args.benchmark:
        t1 = perf_counter()
    try:
        r = PyPackerDetect(**vars(args)).detect(args.path, args.score)
        if args.score:
            r = [r >= args.st]
        else:
            PyPackerDetect.report(args.path, r)
            r = []
        dt = str(perf_counter() - t1) if args.benchmark else ""
        if not isinstance(r, (tuple, list)):
            r = [r]
        r = list(map(str, r))
        if dt != "":
            r.append(dt)
        print(" ".join(r))
    except Exception as e:
        if str(e) != "no result":
            args.logger.exception(e)
        code = 1
    return code

