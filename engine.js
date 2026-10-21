// Bridge Math engine: Wheatstone bridge leg voltages and signed reading, the unknown arm from balance, and the reading shift per ohm. Exact integers (ohms, hundredths of a V, hundredths of a mV), half-up on display only.
function _p(t, err, intDigits, places, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  var m = new RegExp("^([0-9]{1," + intDigits + "})(?:\\.([0-9]{1," + places + "}))?$").exec(t);
  if (!m) throw new Error(err);
  var v = parseInt(m[1], 10) * Math.pow(10, places) + (m[2] ? parseInt(m[2].padEnd(places, "0"), 10) : 0);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
function _pi(t, err, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,7}$/.test(t)) throw new Error(err);
  var v = parseInt(t, 10);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _V = "the excitation must be from 0.01 to 100 V with at most two decimal places";
var _R = "each resistance must be a whole number from 1 to 1000000 Ω";
function _hu(n, d) { return Math.floor((2 * n + d) / (2 * d)); }
function _dec(v, places) {
  if (v < 0) return "-" + _dec(-v, places);
  var base = Math.pow(10, places);
  var s = String(Math.floor(v / base)), f = String(v % base).padStart(places, "0").replace(/0+$/, "");
  return f ? s + "." + f : s;
}
function _sdec(v, places) { return v < 0 ? "-" + _dec(-v, places) : _dec(v, places); }
function _volt(t) { return _p(t, _V, 3, 2, 1, 10000); }
function _r(t) { return _pi(t, _R, 1, 1000000); }
function _mv(v) { return _dec(v, 2) + " mV"; }
function _leg(vs, top, bottom) { return _hu(1000 * vs * bottom, top + bottom); }

function bridgeTruth(vs, r1, r2, r3, r4) {
  var v = _volt(vs), a = _r(r1), b = _r(r2), c = _r(r3), d = _r(r4);
  var va = _leg(v, a, b), vb = _leg(v, c, d);
  var out = vb - va;
  return "With a " + _dec(v, 2) + " V excitation, the left leg sits at " + _mv(va) + " and the right leg at " + _mv(vb) + ", so the bridge reads " + _sdec(out, 2) + " mV.";
}
function unknownTruth(r1, r2, r3) {
  var a = _r(r1), b = _r(r2), c = _r(r3);
  var rx = _hu(100 * b * c, a);
  return "With " + a + " Ω and " + b + " Ω on one side and a " + c + " Ω known arm in balance, the unknown works out to " + _dec(rx, 2) + " Ω.";
}
function shiftTruth(vs, r, rx) {
  var v = _volt(vs), a = _r(r), x = _r(rx);
  function m2(w) { return _leg(v, a, w) - _leg(v, a, a); }
  var shift = m2(x + 1) - m2(x);
  return "With a " + _dec(v, 2) + " V excitation and " + a + " Ω arms, a 1 Ω shift around " + x + " Ω moves the reading by " + _sdec(shift, 2) + " mV.";
}
