import json, random
from fractions import Fraction

def hu(num, den):
    return Fraction((2*num + den) - ((2*num + den) % (2*den)), 2*den)

def dec(v, places=2):
    if v < 0: return "-" + dec(-v, places)
    base = 10**places
    n = v.numerator // v.denominator
    s = str(n // base); f = str(n % base).zfill(places).rstrip("0")
    return s + "." + f if f else s

def sdec(v, places=2):
    return ("-" if v < 0 else "") + dec(abs(v), places)

def leg(vs, top, bottom): return hu(1000*vs*bottom, top+bottom)

def bridge(v, a, b, c, d):
    va = leg(v,a,b); vb = leg(v,c,d); out = vb - va
    return (f"With a {dec(Fraction(v))} V excitation, the left leg sits at {dec(va)} mV and the right leg at {dec(vb)} mV, "
            f"so the bridge reads {sdec(out)} mV.")
def unknown(a, b, c):
    rx = hu(100*b*c, a)
    return f"With {a} Ω and {b} Ω on one side and a {c} Ω known arm in balance, the unknown works out to {dec(rx)} Ω."
def shift(v, a, x):
    def m2(w): return leg(v,a,w) - leg(v,a,a)
    s = m2(x+1) - m2(x)
    return f"With a {dec(Fraction(v))} V excitation and {a} Ω arms, a 1 Ω shift around {x} Ω moves the reading by {sdec(s)} mV."

def s100(n):
    w, f = divmod(n, 100)
    return f"{w}.{f:02d}".rstrip("0").rstrip(".")

random.seed(730)
cases = [
  dict(fn="bridge", args=["5","1000","1000","1000","1001"], expect=bridge(500,1000,1000,1000,1001)),
  dict(fn="unknown", args=["1000","1000","1010"], expect=unknown(1000,1000,1010)),
  dict(fn="shift", args=["5","1000","1000"], expect=shift(500,1000,1000)),
]
for _ in range(30):
    v = random.randint(1,10000)
    rs = [random.randint(1,1000000) for _ in range(4)]
    cases.append(dict(fn="bridge", args=[s100(v)]+[str(r) for r in rs], expect=bridge(v,*rs)))
    a,b,c = [random.randint(1,1000000) for _ in range(3)]
    cases.append(dict(fn="unknown", args=[str(a),str(b),str(c)], expect=unknown(a,b,c)))
    r,x = random.randint(1,1000000), random.randint(1,1000000)
    cases.append(dict(fn="shift", args=[s100(v),str(r),str(x)], expect=shift(v,r,x)))
errcases = [
  ("bridge", ["0","1000","1000","1000","1000"]), ("bridge", ["5","0","1000","1000","1000"]),
  ("bridge", ["5","1000001","1000","1000","1000"]), ("bridge", ["5","1.5","1000","1000","1000"]),
  ("unknown", ["0","1000","1010"]), ("unknown", ["1000","1000","0"]),
  ("shift", ["0","1000","1000"]), ("shift", ["5","0","1000"]), ("shift", ["5","1000","0"]),
  ("bridge", ["100.001","1000","1000","1000","1000"]),
]
json.dump({"cases": cases, "errors": errcases}, open("expected.json","w"), ensure_ascii=False, indent=1)
open("expected.json","a").write("\n")
print("expected.json written:", len(cases), "cases")
