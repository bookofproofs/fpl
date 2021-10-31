from fplinterpreter import FplInterpreter
from util import fplutil

u = fplutil.Utils()
fpl_parser = u.get_parser("../grammar/fpl_tatsu_format.ebnf")
u.add_distinct_duration("creating tatsu parser")

theoryCommon = fplutil.Utils.get_file_content("theories/Commons.fpl")
interpreterCommon = FplInterpreter(fpl_parser)
interpreterCommon.syntax_transform("common", theoryCommon)
u.add_distinct_duration("interpreting common")
print(interpreterCommon.minified())
if interpreterCommon.has_errors():
    interpreterCommon.print_errors()

theoryNat = fplutil.Utils.get_file_content("theories/ArithmeticsNat.fpl")
interpreterNat = FplInterpreter(fpl_parser)
interpreterNat.syntax_transform("nat", theoryCommon)
u.add_distinct_duration("interpreting nat")
print(interpreterNat.minified())
if interpreterNat.has_errors():
    interpreterNat.print_errors()

theorySet = fplutil.Utils.get_file_content("theories/Set.fpl")
interpreterSet = FplInterpreter(fpl_parser)
interpreterSet.syntax_transform("settheory", theorySet)
u.add_distinct_duration("interpreting set")
print(interpreterSet.minified())
if interpreterSet.has_errors():
    interpreterSet.print_errors()

theoryAlgebra = fplutil.Utils.get_file_content("theories/Algebra.fpl")
interpreterAlgebra = FplInterpreter(fpl_parser)
interpreterAlgebra.syntax_transform("algebra", theoryAlgebra)
u.add_distinct_duration("interpreting algebra")
print(interpreterAlgebra.minified())
if interpreterAlgebra.has_errors():
    interpreterAlgebra.print_errors()

theoryGeometry = fplutil.Utils.get_file_content("theories/Geometry.fpl")
interpreterGeometry = FplInterpreter(fpl_parser)
interpreterGeometry.syntax_transform("geometry", theoryGeometry)
u.add_distinct_duration("interpreting geometry")
print(interpreterGeometry.minified())
if interpreterGeometry.has_errors():
    interpreterGeometry.print_errors()

theoryExample25 = fplutil.Utils.get_file_content("theories/Example4-7.fpl")
interpreterExample25 = FplInterpreter(fpl_parser)
interpreterExample25.syntax_transform("example25", theoryExample25)
u.add_distinct_duration("interpreting example25")
print(interpreterExample25.minified())
if interpreterExample25.has_errors():
    interpreterExample25.print_errors()

theoryLinalg = fplutil.Utils.get_file_content("theories/Linalg.fpl")
interpreterLinalg = FplInterpreter(fpl_parser)
interpreterLinalg.syntax_transform("linalg", theoryLinalg)
u.add_distinct_duration("interpreting linalg")
print(interpreterLinalg.minified())
if interpreterLinalg.has_errors():
    interpreterLinalg.print_errors()

theoryComStruct = fplutil.Utils.get_file_content("theories/CommonsStructures.fpl")
interpreterComStruct = FplInterpreter(fpl_parser)
interpreterComStruct.syntax_transform("comstruct", theoryComStruct)
u.add_distinct_duration("interpreting comstruct")
print(interpreterComStruct.minified())
if interpreterComStruct.has_errors():
    interpreterComStruct.print_errors()


u.print_durations()


