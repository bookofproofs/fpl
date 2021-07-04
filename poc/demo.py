from fplinterpreter import FplInterpreter
from util import fplutil

u = fplutil.Utils()
fpl_parser = u.get_parser("../grammar/fpl_tatsu_format.ebnf")
u.add_distinct_duration("creating tatsu parser")

theoryCommon = u.get_file_content("theories/Commons.fpl")
interpreterCommon = FplInterpreter("common", theoryCommon, fpl_parser, True)
u.add_distinct_duration("interpreting common")
if not interpreterCommon.has_errors():
    print(interpreterCommon.minified())
    # interpreterCommon.print_semantics()
else:
    interpreterCommon.print_errors()

theoryNat = u.get_file_content("theories/ArithmeticsNat.fpl")
interpreterNat = FplInterpreter("nat", theoryNat, fpl_parser, True)
u.add_distinct_duration("interpreting nat")
if not interpreterNat.has_errors():
    print(interpreterNat.minified())
    # interpreterNat.print_semantics()
else:
    interpreterNat.print_errors()

theorySet = u.get_file_content("theories/Set.fpl")
interpreterSet = FplInterpreter("settheory", theorySet, fpl_parser, True)
u.add_distinct_duration("interpreting set")
if not interpreterSet.has_errors():
    print(interpreterSet.minified())
    # interpreterSet.print_semantics()
else:
    interpreterSet.print_errors()

theoryAlgebra = u.get_file_content("theories/Algebra.fpl")
interpreterAlgebra = FplInterpreter("algebra", theoryAlgebra, fpl_parser, True)
u.add_distinct_duration("interpreting algebra")
if not interpreterAlgebra.has_errors():
    print(interpreterAlgebra.minified())
    # interpreterAlgebra.print_semantics()
else:
    interpreterAlgebra.print_errors()

theoryGeometry = u.get_file_content("theories/Geometry.fpl")
interpreterGeometry = FplInterpreter("geometry", theoryGeometry, fpl_parser, True)
u.add_distinct_duration("interpreting geometry")
if not interpreterGeometry.has_errors():
    print(interpreterGeometry.minified())
    # interpreterGeometry.print_semantics()
else:
    interpreterGeometry.print_errors()

theoryLinalg = u.get_file_content("theories/Linalg.fpl")
interpreterLinalg = FplInterpreter("linalg", theoryLinalg, fpl_parser, True)
u.add_distinct_duration("interpreting linalg")
if not interpreterLinalg.has_errors():
    print(interpreterLinalg.minified())
    # interpreterLinalg.print_semantics()
else:
    interpreterLinalg.print_errors()

theoryComStruct = u.get_file_content("theories/CommonsStructures.fpl")
interpreterComStruct = FplInterpreter("comstruct", theoryComStruct, fpl_parser, True)
u.add_distinct_duration("interpreting comstruct")
if not interpreterComStruct.has_errors():
    print(interpreterComStruct.minified())
    # interpreterComStruct.print_semantics()
else:
    interpreterComStruct.print_errors()

theoryExample25 = u.get_file_content("theories/Example4-7.fpl")
interpreterExample25 = FplInterpreter("example25", theoryExample25, fpl_parser, True)
u.add_distinct_duration("interpreting example25")
if not interpreterExample25.has_errors():
    print(interpreterExample25.minified())
    # interpreterExample25.print_semantics()
else:
    interpreterExample25.print_errors()

u.print_durations()


