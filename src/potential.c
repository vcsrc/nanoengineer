/* Copyright (c) 2006 Nanorex, Inc. All rights reserved. */

#include "simulator.h"

#define ALMOST_ZERO 0.0001

static char const rcsid[] = "$Id$";

#if 0
/* Be able to turn off CHECK* when we need performance */
#undef CHECKNAN
#undef CHECKNANR
#undef CHECKVEC
#define CHECKNAN(x)
#define CHECKNANR(x,y)
#define CHECKVEC(x)
#endif

// incremented each time either the potential or gradient is
// calculated.  Used to match values in bond->valid to determine the
// need to recalculate bond->inverseLength and bond->rUnit.
//
// This is the same as setting bond->valid to 0 for each bond,
// checking for non-zero, and setting to non-zero when calculated.  It
// doesn't require the reset loop at the start of each calculation,
// though.
//
// Probably should allow the use of the same serial number for back to
// back calls to potential and gradient using the same positions.  But
// then we'd have to save r and rSquared as well.
static int validSerial = 0;

// presumes that updateVanDerWaals() has been called already.
static void
setRUnit(struct xyz *position, struct bond *b, double *pr)
{
  struct xyz rv;
  double r;
  double rSquared;

  // rv points from a1 to a2
  vsub2(rv, position[b->a2->index], position[b->a1->index]);
  rSquared = vdot(rv, rv);
  r = sqrt(rSquared);
  if (r < 0.001) {
    // atoms are on top of each other
    b->inverseLength = 1000;
    vsetc(b->rUnit, 1.0);
  } else {
    b->inverseLength = 1.0 / r;
    vmul2c(b->rUnit, rv, b->inverseLength); /* unit vector along r from a1 to a2 */
  }
  CHECKVEC(b->rUnit);
  if (pr) {
    *pr = r;
  }
  b->valid = validSerial;
}


// note: the first two parameters are only used for error processing...
// result in aJ (1e-18 J)
double
stretchPotential(struct part *p, struct stretch *stretch, struct bondStretch *stretchType, double r)
{
  int k;
  double potential;

  /* interpolation */
  double *a;
  double *b;
  double *c;
  double *d;
  double start;
  double scale;

  struct interpolationTable *iTable;

  // table lookup equivalent to: potential = potentialLippincottMorse(rSquared);
  iTable = &stretchType->LippincottMorse;
  start = iTable->start;
  scale = iTable->scale;
  a = iTable->a;
  b = iTable->b;
  c = iTable->c;
  d = iTable->d;
  k = (int)((r - start) / scale);
  if (k < 0) {
    if (!ToMinimize && DEBUG(D_TABLE_BOUNDS) && stretch) { //linear
      fprintf(stderr, "stretch: low --");
      printStretch(stderr, p, stretch);
    }
    potential = ((a[0] * r + b[0]) * r + c[0]) * r + d[0];
  } else if (k >= TABLEN) {
    if (ToMinimize) { // extend past end of table using a polynomial
      potential =
        ((stretchType->potentialExtensionD * r +
          stretchType->potentialExtensionC) * r +
         stretchType->potentialExtensionB) * r +
        stretchType->potentialExtensionA;
    } else {
      potential=0.0;
      if (DEBUG(D_TABLE_BOUNDS) && stretch) {
        fprintf(stderr, "stretch: high --");
        printStretch(stderr, p, stretch);
      }
    }
  } else if (DirectEvaluate) {
    potential = potentialLippincottMorse(r, stretchType);
  } else {
    potential = ((a[k] * r + b[k]) * r + c[k]) * r + d[k];
  }
  return potential;
}

static double
stretchPotentialPart(struct part *p, struct xyz *position)
{
  int j;
  struct stretch *stretch;
  struct bond *bond;
  double r;
  double potential = 0.0;

  for (j=0; j<p->num_stretches; j++) {
    stretch = &p->stretches[j];
    bond = stretch->b;

    // we presume here that rUnit is invalid, and we need r
    // anyway.
    setRUnit(position, bond, &r);
    BAILR(0.0);
    potential += stretchPotential(p, stretch, stretch->stretchType, r);
    CHECKNANR(potential, 0.0);
  }
  return potential;
}

// result in pN (1e-12 J/m)
double
stretchGradient(struct part *p, struct stretch *stretch, struct bondStretch *stretchType, double r)
{
  int k;
  double gradient; // in uN, converted to pN on return

  /* interpolation */
  double *a;
  double *b;
  double *c;
  double start;
  double scale;

  struct interpolationTable *iTable;

  // table lookup equivalent to: gradient = gradientLippincottMorse(r);
  // Note:  this points uphill, toward higher potential values.
  iTable = &stretchType->LippincottMorse;
  start = iTable->start;
  scale = iTable->scale;
  a = iTable->a;
  b = iTable->b;
  c = iTable->c;
  k = (int)((r - start) / scale);
  if (!ToMinimize &&
      !ExcessiveEnergyWarning &&
      (k < stretchType->minPhysicalTableIndex ||
       k > stretchType->maxPhysicalTableIndex))
    {
      WARNING2("excessive energy on %s bond at iteration %d -- further warnings suppressed", stretchType->bondName, Iteration);
      ExcessiveEnergyWarningThisFrame++;
    }
  if (k < 0) {
    if (!ToMinimize && DEBUG(D_TABLE_BOUNDS) && stretch) { //linear
      fprintf(stderr, "stretch: low --");
      printStretch(stderr, p, stretch);
    }
    gradient = (3.0 * a[0] * r + 2.0 * b[0]) * r + c[0];
  } else if (k >= TABLEN) {
    if (ToMinimize) { // extend past end of table using a polynomial
      gradient =
        (stretchType->potentialExtensionD * r * 3.0 +
         stretchType->potentialExtensionC * 2.0) * r +
        stretchType->potentialExtensionB;
    } else {
      gradient=0.0;
      if (DEBUG(D_TABLE_BOUNDS) && stretch) {
        fprintf(stderr, "stretch: high --");
        printStretch(stderr, p, stretch);
      }
    }
  } else if (DirectEvaluate) {
    gradient = gradientLippincottMorse(r, stretchType);
  } else {
    gradient = (3.0 * a[k] * r + 2.0 * b[k]) * r + c[k];
  }
  return gradient * 1e6;
}

static void
stretchGradientPart(struct part *p, struct xyz *position, struct xyz *force)
{
  int j;
  double gradient;
  struct stretch *stretch;
  struct bond *bond;
  struct xyz f;
  double r;
    
  for (j=0; j<p->num_stretches; j++) {
    stretch = &p->stretches[j];
    bond = stretch->b;

    // we presume here that rUnit is invalid, and we need r anyway
    setRUnit(position, bond, &r);
    BAIL();

    gradient = stretchGradient(p, stretch, stretch->stretchType, r);
    CHECKNAN(gradient);
    // rUnit points from a1 to a2; F = -gradient
    vmul2c(f, bond->rUnit, gradient);
    vadd(force[bond->a1->index], f);
    vsub(force[bond->a2->index], f);
    if (DEBUG(D_STRESS_MOVIE)) { // -D12
      writeSimpleStressVector(position, bond->a1->index, bond->a2->index, -1, gradient, 1000.0, 10000.0);
    }
    if (0 && DEBUG(D_MINIMIZE_GRADIENT_MOVIE_DETAIL)) { // -D5
      writeSimpleForceVector(position, bond->a1->index, &f, 1, 1.0); // red
      vmulc(f, -1.0);
      writeSimpleForceVector(position, bond->a2->index, &f, 1, 1.0); // red
    }
  }
}

static double
bendPotentialPart(struct part *p, struct xyz *position)
{
  int j;
  struct bend *bend;
  struct bond *bond1;
  struct bond *bond2;
  struct xyz v1;
  struct xyz v2;
  double theta;
  double dTheta;
  struct bendData *bType;
  double ff;
  double potential = 0.0;

  for (j=0; j<p->num_bends; j++) {
    bend = &p->bends[j];

    bond1 = bend->b1;
    bond2 = bend->b2;

    // Update rUnit for both bonds, if necessary.  Note that we
    // don't need r or rSquared here.
    if (bond1->valid != validSerial) {
      setRUnit(position, bond1, NULL);
      BAILR(0.0);
    }
    if (bond2->valid != validSerial) {
      setRUnit(position, bond2, NULL);
      BAILR(0.0);
    }
      
    // v1, v2 are the unit vectors FROM the central atom TO the
    // neighbors.  Reverse them if we have to.
    if (bend->dir1) {
      vsetn(v1, bond1->rUnit);
    } else {
      vset(v1, bond1->rUnit);
    }
    if (bend->dir2) {
      vsetn(v2, bond2->rUnit);
    } else {
      vset(v2, bond2->rUnit);
    }

    theta = (Pi / 180.0) * angleBetween(v1, v2);
    BAILR(0.0);

#if 0
#define ACOS_POLY_A -0.0820599
#define ACOS_POLY_B  0.142376
#define ACOS_POLY_C -0.137239
#define ACOS_POLY_D -0.969476

    z = vlen(vsum(v1, v2));
    // this is the equivalent of theta=arccos(z);
    theta = Pi + z * (ACOS_POLY_D +
                      z * (ACOS_POLY_C +
                           z * (ACOS_POLY_B +
                                z *  ACOS_POLY_A   )));
#endif
      
    // bType->kb in yJ/rad^2 (1e-24 J/rad^2)
    bType = bend->bendType;
    dTheta = (theta - bType->theta0);
    ff = 0.5 * dTheta * dTheta * bType->kb;
    // ff is in yJ (1e-24 J), potential in aJ (1e-18 J)
    potential += ff * 1e-6;
    CHECKNANR(potential, 0.0);
  }
  return potential;
}

static void
bendGradientPart(struct part *p, struct xyz *position, struct xyz *force)
{
  int j;
  struct xyz v1;
  struct xyz v2;
  double theta;
  double ff;
  struct bond *bond1;
  struct bond *bond2;
  struct bend *bend;
  struct bendData *bType;
  double torque;
  struct xyz q1;
  struct xyz q2;
  struct xyz foo;
  struct xyz axis;
    
  /* now the forces for each bend */
  for (j=0; j<p->num_bends; j++) {
    bend = &p->bends[j];

    bond1 = bend->b1;
    bond2 = bend->b2;

    // Update rUnit for both bonds, if necessary.  Note that we
    // don't need r or rSquared here.
    if (bond1->valid != validSerial) {
      setRUnit(position, bond1, NULL);
      BAIL();
    }
    if (bond2->valid != validSerial) {
      setRUnit(position, bond2, NULL);
      BAIL();
    }
      
    // v1, v2 are the unit vectors FROM the central atom TO the
    // neighbors.  Reverse them if we have to.
    if (bend->dir1) {
      vsetn(v1, bond1->rUnit);
    } else {
      vset(v1, bond1->rUnit);
    }
    if (bend->dir2) {
      vsetn(v2, bond2->rUnit);
    } else {
      vset(v2, bond2->rUnit);
    }

    // XXX figure out how close we can get / need to get
    // apply no force if v1 and v2 are close to being linear
#define COLINEAR 1e-8

    theta = (Pi / 180.0) * angleBetween(v1, v2);

#if 0
    z = vlen(vsum(v1, v2));
    // this is the equivalent of theta=arccos(z);
    theta = Pi + z * (ACOS_POLY_D +
                      z * (ACOS_POLY_C +
                           z * (ACOS_POLY_B +
                                z *  ACOS_POLY_A   )));
#endif
      
    v2x(foo, v1, v2);       // foo = v1 cross v2
    if (vlen(foo) < COLINEAR) {
      // v1 and v2 are very close to colinear.  We can pick any
      // vector orthogonal to either one.  First we try v1 x (1, 0,
      // 0).  If v1 is colinear with the x axis, then it can't be
      // colinear with the y axis too, so we use v1 x (0, 1, 0) in
      // that case.
      axis.x = 1;
      axis.y = 0;
      axis.z = 0;
      v2x(foo, v1, axis);
      if (vlen(foo) < COLINEAR) {
        axis.x = 0;
        axis.y = 1;
        v2x(foo, v1, axis);
      }
    }
        
    //foo = uvec(foo);        // hmmm... not sure why this has to be a unit vector.
    q1 = uvec(vx(v1, foo)); // unit vector perpendicular to v1 in plane of v1 and v2
    q2 = uvec(vx(foo, v2)); // unit vector perpendicular to v2 in plane of v1 and v2

    // bType->kb in yJ/rad^2 (1e-24 J/rad^2)
    bType = bend->bendType;
    // torque in yJ/rad
    torque = (theta - bType->theta0) * bType->kb;
    // inverseLength is rad/pm
    // ff is yJ/pm (1e-24 J / 1e-12 m) or 1e-12 J/m or pN
    ff = torque * bond1->inverseLength;
    vmulc(q1, ff);
    ff = torque * bond2->inverseLength;
    vmulc(q2, ff);

    vsub(force[bend->ac->index], q1);
    vadd(force[bend->a1->index], q1);
    vsub(force[bend->ac->index], q2);
    vadd(force[bend->a2->index], q2);
    if (DEBUG(D_STRESS_MOVIE)) { // -D12
      writeSimpleStressVector(position, bend->a1->index, bend->a2->index, bend->ac->index, torque, 500000.0, 1000000.0);
    }
    if (0 && DEBUG(D_MINIMIZE_GRADIENT_MOVIE_DETAIL)) { // -D5
      writeSimpleForceVector(position, bend->a1->index, &q1, 3, 1.0); // blue
      vmulc(q1, -1.0);
      writeSimpleForceVector(position, bend->ac->index, &q1, 2, 1.0); // green
      writeSimpleForceVector(position, bend->a2->index, &q2, 3, 1.0); // blue
      vmulc(q2, -1.0);
      writeSimpleForceVector(position, bend->ac->index, &q2, 2, 1.0); // green
    }
  }
}

static double
torsionPotentialPart(struct part *p, struct xyz *position)
{
  int j;
  struct torsion *torsion;
  struct xyz v1;
  struct xyz v2;
  struct xyz v3;
  struct xyz v4;
  struct xyz v5;
  double theta;
  double potential = 0.0;

  for (j=0; j<p->num_torsions; j++) {
    torsion = &p->torsions[j];

    // v3: ab --- aa is central bond that the torsion is around
    // v4 and v5 are are the two end bonds
    vsub2(v3, position[torsion->ab->index], position[torsion->aa->index]);
    vsub2(v4, position[torsion->a1->index], position[torsion->aa->index]);
    vsub2(v5, position[torsion->a2->index], position[torsion->ab->index]);
    v2x(v1, v3, v4); // v3 x v4 is normal to 1-a-b plane
    v2x(v2, v5, v3); // v5 x v3 is normal to a-b-2 plane
    theta = (Pi / 180.0) * angleBetween(v1, v2);
    BAILR(0.0);

    // cos(2 * theta) goes like theta^2 for small theta
    // so A is in aJ/rad^2
    potential += torsion->A * (1 - cos(2 * theta));
    CHECKNANR(potential, 0.0);
  }
  return potential;
}

static void
torsionGradientPart(struct part *p, struct xyz *position, struct xyz *force)
{
  int j;
  struct xyz v1;
  struct xyz v2;
  struct xyz v3;
  struct xyz v4;
  struct xyz v5;
  double theta;
  double ff;
  struct torsion *torsion;
  double torque;
  struct xyz q1;
  struct xyz q2;
    
  for (j=0; j<p->num_torsions; j++) {
    torsion = &p->torsions[j];

    // v3: ab --- aa is central bond that the torsion is around
    // v4 and v5 are are the two end bonds
    vsub2(v3, position[torsion->ab->index], position[torsion->aa->index]);
    vsub2(v4, position[torsion->a1->index], position[torsion->aa->index]);
    vsub2(v5, position[torsion->a2->index], position[torsion->ab->index]);
    v2x(v1, v3, v4); // v3 x v4 is normal to 1-a-b plane
    v2x(v2, v5, v3); // v5 x v3 is normal to a-b-2 plane
    // v1 and v2 point along the direction that a1 and a2 should move
    theta = (Pi / 180.0) * angleBetween(v1, v2);
    if (theta < 1e-10) {
      continue;
    }

    q1 = uvec(v1); // unit vector along which force will be applied to a1
    q2 = uvec(v2); // unit vector along which force will be applied to a2

    // v1 dot v5 tells us the sign of the torque to apply
      
    // A is aJ/rad^2
    // sin(2 * theta) = 2 * theta for small theta, so torque is aJ/rad
    torque = (vdot(v1, v5) > 0.0 ? -torsion->A : torsion->A) * sin(2 * theta);
    // vlen(v4) is pm/rad; ff is yJ/pm or pN
    ff = 1e3 * torque / vlen(v4);
    ff *= 2e3;
    CHECKNAN(ff);
    vmulc(q1, ff);
    ff = 1e3 * torque / vlen(v5);
    ff *= 2e3;
    CHECKNAN(ff);
    vmulc(q2, ff);
      
    vsub(force[torsion->aa->index], q1);
    vadd(force[torsion->a1->index], q1);
    vsub(force[torsion->ab->index], q2);
    vadd(force[torsion->a2->index], q2);
      
    if (DEBUG(D_MINIMIZE_GRADIENT_MOVIE_DETAIL)) { // -D5
      writeSimpleForceVector(position, torsion->a1->index, &q1, 3, 1.0); // blue
      vmulc(q1, -1.0);
      writeSimpleForceVector(position, torsion->aa->index, &q1, 2, 1.0); // green
      writeSimpleForceVector(position, torsion->a2->index, &q2, 3, 1.0); // blue
      vmulc(q2, -1.0);
      writeSimpleForceVector(position, torsion->ab->index, &q2, 2, 1.0); // green
    }
    BAIL();
  }
}

static double
outOfPlanePotentialPart(struct part *p, struct xyz *position)
{
  int j;
  double rSquared;
  double normalLength;
  struct xyz v1_2;
  struct xyz v1_3;
  struct xyz v1_c;
  struct xyz normal;
  struct xyz unitNormal;
  double outOfPlaneDistance;
  struct outOfPlane *outOfPlane;
  double potential = 0.0;
    
  for (j=0; j<p->num_outOfPlanes; j++) {
    outOfPlane = &p->outOfPlanes[j];

    // v1_2 and v1_3 are vectors in the plane of the outer triangle (1-2-3)
    // v1_c is a vector from somewhere on that plane (actually point 1)
    //    to the outOfPlane point.
    vsub2(v1_2, position[outOfPlane->a2->index], position[outOfPlane->a1->index]);
    vsub2(v1_3, position[outOfPlane->a3->index], position[outOfPlane->a1->index]);
    vsub2(v1_c, position[outOfPlane->ac->index], position[outOfPlane->a1->index]);

    v2x(normal, v1_2, v1_3);
    rSquared = vdot(normal, normal);
    if (rSquared < 1e-8) {
      // If normal is very short, then 1-2-3 must be nearly co-linear.
      // We can draw any plane we want which passes through that line,
      // so we choose the one passing through point c.  That means
      // outOfPlaneDistance = 0.
      continue;
    }

    // At this point, we know that 1, 2, and 3 are all distinct points

    // distance = v1_c dot unit(normal)
    normalLength = 1.0 / sqrt(rSquared);
    vmul2c(unitNormal, normal, normalLength);
    outOfPlaneDistance = vdot(unitNormal, v1_c);

    // A is aJ/pm^2
    potential += 0.5 * outOfPlane->A * outOfPlaneDistance * outOfPlaneDistance;
    CHECKNANR(potential, 0.0);
  }
  return potential;
}

#define BALANCED_OOP_GRADIENT

static void
outOfPlaneGradientPart(struct part *p, struct xyz *position, struct xyz *force)
{
  int j;
  double rSquared;
  double normalLength;
  struct xyz v1_2;
  struct xyz v1_3;
  struct xyz v1_c;
  struct xyz normal;
  struct xyz unitNormal;
  struct xyz projection_ac; // point in plane which is closest to ac
  struct xyz f;
  struct xyz f1;
  double ff;
  double outOfPlaneDistance;
  struct outOfPlane *outOfPlane;
  double factor1;
  double factor2;
  double factor3;
#ifdef BALANCED_OOP_GRADIENT
  double parameter;
  struct xyz axis;
  struct xyz axis_mobilePlanePoint;
  struct xyz axis_projectionAc;
#ifdef CHECK_RESIDUAL
  struct xyz v2_3;
  struct xyz v2_1;
  double factor1a;
#endif
#endif
    
  for (j=0; j<p->num_outOfPlanes; j++) {
    outOfPlane = &p->outOfPlanes[j];

    // v1_2 and v1_3 are vectors in the plane of the outer triangle (1-2-3)
    // v1_c is a vector from somewhere on that plane (actually point 1)
    //    to the outOfPlane point.
    vsub2(v1_2, position[outOfPlane->a2->index], position[outOfPlane->a1->index]);
    vsub2(v1_3, position[outOfPlane->a3->index], position[outOfPlane->a1->index]);
    vsub2(v1_c, position[outOfPlane->ac->index], position[outOfPlane->a1->index]);

    v2x(normal, v1_2, v1_3);
    rSquared = vdot(normal, normal);
    if (rSquared < 1e-8) {
      // If normal is very short, then 1-2-3 must be nearly co-linear.
      // We can draw any plane we want which passes through that line,
      // so we choose the one passing through point c.  That means
      // outOfPlaneDistance = 0.
      continue;
    }

    // At this point, we know that 1, 2, and 3 are all distinct points

    // distance = v1_c dot unit(normal)
    normalLength = 1.0 / sqrt(rSquared);
    vmul2c(unitNormal, normal, normalLength);
    outOfPlaneDistance = vdot(unitNormal, v1_c);

    if (fabs(outOfPlaneDistance) < 1e-8) {
      continue;
    }
    // Now, ac must be distinct from 1, 2, 3 as well.

#ifdef BALANCED_OOP_GRADIENT

#define closePointParameter(line, point) (vdot(point, line) / vdot(line, line))

    vmul2c(projection_ac, unitNormal, -outOfPlaneDistance);
    vadd(projection_ac, position[outOfPlane->ac->index]);

    parameter = closePointParameter(v1_2, v1_3);
    vmul2c(axis, v1_2, parameter);
    vadd(axis, position[outOfPlane->a1->index]);
    vsub2(axis_mobilePlanePoint, position[outOfPlane->a3->index], axis);
    vsub2(axis_projectionAc, projection_ac, axis);
    factor3 = -closePointParameter(axis_mobilePlanePoint, axis_projectionAc);

    parameter = closePointParameter(v1_3, v1_2);
    vmul2c(axis, v1_3, parameter);
    vadd(axis, position[outOfPlane->a1->index]);
    vsub2(axis_mobilePlanePoint, position[outOfPlane->a2->index], axis);
    vsub2(axis_projectionAc, projection_ac, axis);
    factor2 = -closePointParameter(axis_mobilePlanePoint, axis_projectionAc);

    factor1 = -1.0 - factor2 - factor3;

#ifdef CHECK_RESIDUAL
    vsub2(v2_3, position[outOfPlane->a3->index], position[outOfPlane->a2->index]);
    vsub2(v2_1, position[outOfPlane->a1->index], position[outOfPlane->a2->index]);
    parameter = closePointParameter(v2_3, v2_1);
    vmul2c(axis, v2_3, parameter);
    vadd(axis, position[outOfPlane->a2->index]);
    vsub2(axis_mobilePlanePoint, position[outOfPlane->a1->index], axis);
    vsub2(axis_projectionAc, projection_ac, axis);
    factor1a = -closePointParameter(axis_mobilePlanePoint, axis_projectionAc);

    if (fabs(factor1 - factor1a) > 1e-12) {
      fprintf(stderr, "residual: %e\n", factor1 - factor1a);
    }
#endif
    
#else
    factor1 = factor2 = factor3 = -1.0 / 3.0 ;
#endif

    // A is aJ/pm^2; ff is yJ/pm or pN
    ff = -1e3 * outOfPlane->A * outOfPlaneDistance;
    ff *= 1e3;
    vmul2c(f, unitNormal, ff);
      
    vadd(force[outOfPlane->ac->index], f);
    vmul2c(f1, f, factor1);
    vadd(force[outOfPlane->a1->index], f1);
    vmul2c(f1, f, factor2);
    vadd(force[outOfPlane->a2->index], f1);
    vmul2c(f1, f, factor3);
    vadd(force[outOfPlane->a3->index], f1);
      
    if (DEBUG(D_MINIMIZE_GRADIENT_MOVIE_DETAIL)) { // -D5
      writeSimpleForceVector(position, outOfPlane->ac->index, &f, 8, 100.0); // blue

      vmul2c(f1, f, factor1);
      writeSimpleForceVector(position, outOfPlane->a1->index, &f1, 7, 100.0); // green
      vmul2c(f1, f, factor2);
      writeSimpleForceVector(position, outOfPlane->a2->index, &f1, 7, 100.0); // green
      vmul2c(f1, f, factor3);
      writeSimpleForceVector(position, outOfPlane->a3->index, &f1, 8, 100.0); // green
    }
  }
}

// result in aJ (1e-18 J)
double
vanDerWaalsPotential(struct part *p, struct vanDerWaals *vdw, struct vanDerWaalsParameters *parameters, double r)
{
  double potential;
  int k;
  double *a;
  double *b;
  double *c;
  double *d;
  double start;
  double scale;
  struct interpolationTable *iTable;
  
  /* table setup  */
  iTable = &parameters->Buckingham;
  start = iTable->start;
  scale = iTable->scale;
  a = iTable->a;
  b = iTable->b;
  c = iTable->c;
  d = iTable->d;

  k=(int)((r - start) / scale);
  if (k < 0) {
    if (!ToMinimize && DEBUG(D_TABLE_BOUNDS)) { //linear
      fprintf(stderr, "vdW: off table low -- r=%.2f \n",  r);
      printVanDerWaals(stderr, p, vdw);
    }
    potential = ((a[0] * r + b[0]) * r + c[0]) * r + d[0];
  } else if (k>=TABLEN) {
    potential = 0.0;
  } else if (DirectEvaluate) {
    potential = potentialBuckingham(r, parameters);
  } else {
    potential = ((a[k] * r + b[k]) * r + c[k]) * r + d[k];
  }
  return potential;
}

static double
vdwPotentialPart(struct part *p, struct xyz *position)
{
  int j;
  struct vanDerWaals *vdw;
  struct xyz rv;
  double rSquared;
  double r;
  double potential = 0.0;
    
  /* do the van der Waals/London forces */
  for (j=0; j<p->num_vanDerWaals; j++) {
    vdw = p->vanDerWaals[j];

    // The vanDerWaals array changes over time, and might have
    // NULL's in it as entries are deleted.
    if (vdw == NULL) {
      continue;
    }
      
    vsub2(rv, position[vdw->a1->index], position[vdw->a2->index]);
    rSquared = vdot(rv, rv);
    r = sqrt(rSquared);
    potential += vanDerWaalsPotential(p, vdw, vdw->parameters, r);
    CHECKNANR(potential, 0.0);
  }
  return potential;
}

// result in pN (1e-12 J/m)
double
vanDerWaalsGradient(struct part *p, struct vanDerWaals *vdw, struct vanDerWaalsParameters *parameters, double r)
{
  double gradient; // in uN, converted to pN at return
  int k;
  double *a;
  double *b;
  double *c;
  double start;
  double scale;
  struct interpolationTable *iTable;
      
  /* table setup  */
  iTable = &parameters->Buckingham;
  start = iTable->start;
  scale = iTable->scale;
  a = iTable->a;
  b = iTable->b;
  c = iTable->c;
					
  k=(int)((r - start) / scale);

  if (!ToMinimize &&
      !ExcessiveEnergyWarning &&
      k < parameters->minPhysicalTableIndex)
  {
    WARNING2("excessive energy in %s vdw at iteration %d -- further warnings suppressed", parameters->vdwName, Iteration);
    ExcessiveEnergyWarningThisFrame++;
  }

  if (k < 0) {
    if (!ToMinimize && DEBUG(D_TABLE_BOUNDS)) { //linear
      fprintf(stderr, "vdW: off table low -- r=%.2f \n",  r);
      printVanDerWaals(stderr, p, vdw);
    }
    gradient = (3.0 * a[0] * r + 2.0 * b[0]) * r + c[0];
  } else if (DirectEvaluate) {
    gradient = gradientBuckingham(r, parameters);
  } else if (k>=TABLEN) {
    gradient = 0.0;
  } else {
    gradient = (3.0 * a[k] * r + 2.0 * b[k]) * r + c[k];
  }
  return gradient * 1e6;
}

static void
vdwGradientPart(struct part *p, struct xyz *position, struct xyz *force)
{
  int j;
  double rSquared;
  double gradient;
  struct vanDerWaals *vdw;
  struct xyz rv;
  struct xyz f;
  double r;
    
  /* do the van der Waals/London forces */
  for (j=0; j<p->num_vanDerWaals; j++) {
    vdw = p->vanDerWaals[j];

    // The vanDerWaals array changes over time, and might have
    // NULL's in it as entries are deleted.
    if (vdw == NULL) {
      continue;
    }
      
    vsub2(rv, position[vdw->a1->index], position[vdw->a2->index]);
    rSquared = vdot(rv, rv);
    r = sqrt(rSquared);

    if (r > ALMOST_ZERO) {
      gradient = vanDerWaalsGradient(p, vdw, vdw->parameters, r) / r;
    
      vmul2c(f, rv, gradient);
      vsub(force[vdw->a1->index], f);
      vadd(force[vdw->a2->index], f);
    } else {
      gradient = 0.0;
    }
    if (DEBUG(D_STRESS_MOVIE)) { // -D12
      writeSimpleStressVector(position, vdw->a1->index, vdw->a2->index, -1, gradient, 10.0, 100.0);
    }
    if (DEBUG(D_MINIMIZE_GRADIENT_MOVIE_DETAIL) && r > ALMOST_ZERO) { // -D5
      writeSimpleForceVector(position, vdw->a2->index, &f, 4, 1.0); // cyan
      vmulc(f, -1.0);
      writeSimpleForceVector(position, vdw->a1->index, &f, 4, 1.0); // cyan
    }
  }
}

// result in aJ (1e-18 J)
double
calculatePotential(struct part *p, struct xyz *position)
{
  double potential = 0.0;

  validSerial++;

  if (!DEBUG(D_SKIP_STRETCH)) { // -D6
    potential += stretchPotentialPart(p, position);
    CHECKNANR(potential, 0.0);
  }

  if (!DEBUG(D_SKIP_BEND)) { // -D7
    potential += bendPotentialPart(p, position);
    CHECKNANR(potential, 0.0);
  }

  if (!DEBUG(D_SKIP_TORSION)) { // -D16
    potential += torsionPotentialPart(p, position);
    CHECKNANR(potential, 0.0);
  }

  if (!DEBUG(D_SKIP_OUT_OF_PLANE)) { // -D17
    potential += outOfPlanePotentialPart(p, position);
    CHECKNANR(potential, 0.0);
  }

  if (!DEBUG(D_SKIP_VDW)) { // -D9
    potential += vdwPotentialPart(p, position);
    CHECKNANR(potential, 0.0);
  }
  
  return potential;
}

// result placed in force is in pN (1e-12 J/m)
void
calculateGradient(struct part *p, struct xyz *position, struct xyz *force)
{
  int j;

  validSerial++;
    
  /* clear force vectors */
  for (j=0; j<p->num_atoms; j++) {
    vsetc(force[j], 0.0);
  }
  
  if (!DEBUG(D_SKIP_STRETCH)) { // -D6
    stretchGradientPart(p, position, force);
    BAIL();
  }

  if (!DEBUG(D_SKIP_BEND)) { // -D7
    bendGradientPart(p, position, force);
    BAIL();
  }

  if (!DEBUG(D_SKIP_TORSION)) { // -D16
    torsionGradientPart(p, position, force);
    BAIL();
  }

  if (!DEBUG(D_SKIP_OUT_OF_PLANE)) { // -D17
    outOfPlaneGradientPart(p, position, force);
    BAIL();
  }

  if (!DEBUG(D_SKIP_VDW)) { // -D9
    vdwGradientPart(p, position, force);
    BAIL();
  }
}
