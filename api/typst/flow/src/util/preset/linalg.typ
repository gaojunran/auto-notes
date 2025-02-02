// Utils for typing linear algebra.

// Conjugation.
#let ovl = math.overline

/// Inversion.
#let inv(it) = $it^(-1)$
// Transposition.
#let trp(it) = $it^upright(T)$
// Conjugate transposition.
#let ctrp(it) = $it^upright(H)$

/// Alternate calligraphic handstyle.
/// Not supported by all math fonts.
#let scr(it) = text(
  features: ("ss01",),
  box($cal(it)$)
)
#let dmat(it) = $display(mat(it))$

#let kernel = $scr(N)$
#let image = $scr(R)$

#let null = $arrow(0)$

#let (span, rank, corank, size, Re, Im) = (
  "span", "rank", "corank", "size", "Re", "Im",
).map(math.op)

#let linco(..args) = $sum_(i = 1)^k #args.pos().join()$
#let ipr(..args) = $lr(angle.l #args.pos().join[,] angle.r)$
#let mpr(..args) = $lr([ #args.pos().join[,] ])$

#let matop(entry, rows: $m$, cols: $n$) = {
  $[entry]_(1 <= y <= rows, 1 <= x <= cols)$
}
/// One-line definition of how each entry is named in a matrix.
#let matdef(body, ..args) = matop($body_(y, x)$, ..args)

/// Visual representation of each entry.
#let matvis(entry, rows: $m$, cols: $n$, ..args) = {
  let data = (
      ($entry_(1, 1)$, $dots.c$, $entry_(1, cols)$),
      ($dots.v$, $dots.down$, $dots.v$),
      ($entry_(rows, 1)$, $dots.c$, $entry_(rows, cols)$),
    )

  return math.mat(
    ..data,
    ..args,
  )
}

#let matset = $KK^(m times n)$
#let matset2 = $KK^(n times p)$
#let matset3 = $KK^(p times q)$

#let matsq = $KK^(n times n)$
#let matsq2 = $KK^(m times m)$

#let vecset = $KK^n$
#let vecset2 = $KK^m$

// Over what characters shorthands are defined.
#let charset = "abcdepqrstvwxyz"
#let charset = upper(charset) + charset
/// Maps each common character in equations to the given op.
#let shorthand(op, space: charset) = space.clusters().map(op)

// Absolute value.
#let (
  Aa, Ba, Ca, Da, Ea, Pa, Qa, Ra, Sa, Ta, Va, Wa, Xa, Ya, Za,
  aa, ba, ca, da, ea, pa, qa, ra, sa, ta, va, wa, xa, ya, za,
) = shorthand(math.abs)
// Boldface.
#let (
  Ab, Bb, Cb, Db, Eb, Pb, Qb, Rb, Sb, Tb, Vb, Wb, Xb, Yb, Zb,
  ab, bbo, cb, db, eb, pb, qb, rb, sb, tb, vb, wb, xb, yb, zb,
) = shorthand(math.bold)
// Conjugate.
#let (
  Ac, Bc, Cc, Dc, Ec, Pc, Qc, Rc, Sc, Tc, Vc, Wc, Xc, Yc, Zc,
  ac, bc, cc, dc, ec, pc, qc, rc, sc, tc, vc, wc, xc, yc, zc,
) = shorthand(ovl)
// Norm.
#let (
  An, Bn, Cn, Dn, En, Pn, Qn, Rn, Sn, Tn, Vn, Wn, Xn, Yn, Zn,
  an, bn, cn, dn, en, pn, qn, rn, sn, tn, vn, wn, xn, yn, zn,
) = shorthand(math.norm)
// Vectors.
#let (
  Av, Bv, Cv, Dv, Ev, Pv, Qv, Rv, Sv, Tv, Vv, Wv, Xv, Yv, Zv,
  av, bv, cv, dv, ev, pv, qv, rv, sv, tv, vv, wv, xv, yv, zv,
) = shorthand(math.arrow)
// Tildized.
#let (
  At, Bt, Ct, Dt, Et, Pt, Qt, Rt, St, Tt, Vt, Wt, Xt, Yt, Zt,
  at, bt, ct, dt, et, pt, qt, rt, st, tt, vt, wt, xt, yt, zt,
) = shorthand(math.tilde)
// Inverted.
#let (
  Ainv, Binv, Cinv, Dinv, Einv, Pinv, Qinv, Rinv, Sinv, Tinv, Vinv, Winv, Xinv, Yinv, Zinv,
  ainv, binv, cinv, dinv, einv, pinv, qinv, rinv, sinv, tinv, vinv, winv, xinv, yinv, zinv,
) = shorthand(inv)
// Transposed.
#let (
  AT, BT, CT, DT, ET, PT, QT, RT, ST, TTr, VT, WT, XT, YT, ZT,
  aT, bT, cT, dT, eT, pT, qT, rT, sT, tT, vT, wT, xT, yT, zT,
) = shorthand(trp)
// Conjugate transposed.
#let (
  AH, BH, CH, DH, EH, PH, QH, RH, SH, TH, VH, WH, XH, YH, ZH,
  aH, bH, cH, dH, eH, pH, qH, rH, sH, tH, vH, wH, xH, yH, zH,
) = shorthand(ctrp)

#let vec-shorthand(op, ..args) = shorthand(
  ch => op(math.arrow(ch)),
  ..args,
)
// Vector absolute value.
#let (
  Ava, Bva, Cva, Dva, Eva, Pva, Qva, Rva, Sva, Tva, Vva, Wva, Xva, Yva, Zva,
  ava, bva, cva, dva, eva, pva, qva, rva, sva, tva, vva, wva, xva, yva, zva,
) = vec-shorthand(math.abs)
// Vector boldfaced.
#let (
  Avb, Bvb, Cvb, Dvb, Evb, Pvb, Qvb, Rvb, Svb, Tvb, Vvb, Wvb, Xvb, Yvb, Zvb,
  avb, bvb, cvb, dvb, evb, pvb, qvb, rvb, svb, tvb, vvb, wvb, xvb, yvb, zvb,
) = vec-shorthand(math.bold)
// Vector conjugate.
#let (
  Avc, Bvc, Cvc, Dvc, Evc, Pvc, Qvc, Rvc, Svc, Tvc, Vvc, Wvc, Xvc, Yvc, Zvc,
  avc, bvc, cvc, dvc, evc, pvc, qvc, rvc, svc, tvc, vvc, wvc, xvc, yvc, zvc,
) = vec-shorthand(ovl)
// Vector norm.
#let (
  Avn, Bvn, Cvn, Dvn, Evn, Pvn, Qvn, Rvn, Svn, Tvn, Vvn, Wvn, Xvn, Yvn, Zvn,
  avn, bvn, cvn, dvn, evn, pvn, qvn, rvn, svn, tvn, vvn, wvn, xvn, yvn, zvn,
) = vec-shorthand(math.norm)
// Vector tildized.
#let (
  Avt, Bvt, Cvt, Dvt, Evt, Pvt, Qvt, Rvt, Svt, Tvt, Vvt, Wvt, Xvt, Yvt, Zvt,
  avt, bvt, cvt, dvt, evt, pvt, qvt, rvt, svt, tvt, vvt, wvt, xvt, yvt, zvt,
) = vec-shorthand(math.tilde)
// Vector transposed.
#let (
  AvT, BvT, CvT, DvT, EvT, PvT, QvT, RvT, SvT, TvT, VvT, WvT, XvT, YvT, ZvT,
  avT, bvT, cvT, dvT, evT, pvT, qvT, rvT, svT, tvT, vvT, wvT, xvT, yvT, zvT,
) = vec-shorthand(trp)
// Vector conjugate transposed.
#let (
  AvH, BvH, CvH, DvH, EvH, PvH, QvH, RvH, SvH, TvH, VvH, WvH, XvH, YvH, ZvH,
  avH, bvH, cvH, dvH, evH, pvH, qvH, rvH, svH, tvH, vvH, wvH, xvH, yvH, zvH,
) = vec-shorthand(ctrp)

// Short definition of a matrix' entries.
#let sdef(entry) = $[entry_(y, x)]$
// Short definition of a matrix' entries that is in a general field.
#let sdefk(entry) = $sdef(entry) in matset$
// Short definition of a matrix' entries that is in a complex field.
#let sdefc(entry) = $sdef(entry) in CC^(n times m)$

#let col(name, n: $n$) = $vec(name_1, dots.v, name_#n)$
#let row(name, n: $n$) = $dmat(name_1, ..., name_#n)$

#let vecdef(name, over: $KK$, dim: $n$) = {
  $[name_i]_(i = 1)^dim
  #if over != none { $in over^dim$ }$
}

#let same(value) = $vec(value, dots.v, value)$
