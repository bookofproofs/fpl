from poc.fplsourcetransformer import FPLSourceTransformer
from poc.util import fplutil

u = fplutil.Utils()
fpl_parser = u.get_parser("../grammar/fpl_tatsu_format.ebnf")
u.add_distinct_duration("creating tatsu parser")

transform = FPLSourceTransformer(fpl_parser)
transform.syntax_transform("theories/Commons.fpl")
u.add_distinct_duration("parsing and minifying common")
print(transform.get_minified())

transform.clear()
transform.syntax_transform("theories/ArithmeticsNat.fpl")
u.add_distinct_duration("parsing and minifying nat")
print(transform.get_minified())

transform.clear()
transform.syntax_transform("theories/Set.fpl")
u.add_distinct_duration("parsing and minifying set")
print(transform.get_minified())

transform.clear()
transform.syntax_transform("theories/Algebra.fpl")
u.add_distinct_duration("parsing and minifying algebra")
print(transform.get_minified())

transform.clear()
transform.syntax_transform("theories/Geometry.fpl")
u.add_distinct_duration("parsing and minifying geometry")
print(transform.get_minified())

transform.clear()
transform.syntax_transform("theories/Example4-7.fpl")
u.add_distinct_duration("parsing and minifying example25")
print(transform.get_minified())

transform.clear()
transform.syntax_transform("theories/Linalg.fpl")
u.add_distinct_duration("parsing and minifying linalg")
print(transform.get_minified())

transform.clear()
transform.syntax_transform("theories/CommonsStructures.fpl")
u.add_distinct_duration("parsing and minifying comstruct")
print(transform.get_minified())

u.print_durations()


