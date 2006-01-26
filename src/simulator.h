// Copyright (c) 2004 Nanorex, Inc. All Rights Reserved.

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <signal.h>
#include <time.h>
#include <stdarg.h>
#include <errno.h>
#include <string.h>

#include "debug.h"

#include "lin-alg.h"
#include "allocate.h"
#include "hashtable.h"

#include "minimize.h"
#include "structcompare.h"

#ifdef WWDEBUG
// handy little debug macros
#define SAY(fmt)   { FILE *outf = fopen("/home/wware/FOO", "a"); \
              fprintf(outf, "%s:%d(%s)  ", __FILE__, __LINE__, __FUNCTION__); \
              fprintf(outf, fmt); fclose(outf); }
#define SAY1(fmt,a)   { FILE *outf = fopen("/home/wware/FOO", "a"); \
              fprintf(outf, "%s:%d(%s)  ", __FILE__, __LINE__, __FUNCTION__); \
              fprintf(outf, fmt, a); fclose(outf); }
#define SAY2(fmt,a,b)   { FILE *outf = fopen("/home/wware/FOO", "a"); \
              fprintf(outf, "%s:%d(%s)  ", __FILE__, __LINE__, __FUNCTION__); \
              fprintf(outf, fmt, a, b); fclose(outf); }
#define SAY3(fmt,a,b,c)   { FILE *outf = fopen("/home/wware/FOO", "a"); \
              fprintf(outf, "%s:%d(%s)  ", __FILE__, __LINE__, __FUNCTION__); \
              fprintf(outf, fmt, a, b, c); fclose(outf); }
#define SAY4(fmt,a,b,c,d)   { FILE *outf = fopen("/home/wware/FOO", "a"); \
              fprintf(outf, "%s:%d(%s)  ", __FILE__, __LINE__, __FUNCTION__); \
              fprintf(outf, fmt, a, b, c, d); fclose(outf); }
#else
#define SAY(fmt)
#define SAY1(fmt,a)
#define SAY2(fmt,a,b)
#define SAY3(fmt,a,b,c)
#define SAY4(fmt,a,b,c,d)
#endif

#define MARK()       SAY("\n")
#define SAY_INT(x)   SAY2("%s=%d\n", #x, x)
#define SAY_DBL(x)   SAY2("%s=%lg\n", #x, x)
#define SAY_XYZ(s)   SAY4("%s={%lf,%lf,%lf)\n", #s, (s).x, (s).y, (s).z)
#define SAY_PTR(x)   SAY2("%s=%p\n", #x, x)

#define iabs(x) (x<0 ? -(x) : x)
#ifndef min
#define min(x,y) ((x) < (y) ? (x) : (y))
#endif
#ifndef max
#define max(x,y) ((x) > (y) ? (x) : (y))
#endif

#define PICOSEC (1e-12)

// scaling factor for radius in extension gradient calculations
#define DR 1e6

/* van der Waals forces */

#include "part.h"
#include "newtables.h"
#include "interpolate.h"

#include "readmmp.h"
#include "readxyz.h"
#include "printers.h"
#include "dynamics.h"
#include "jigs.h"
#include "potential.h"
#include "minstructure.h"
#include "writemovie.h"

#include "globals.h"

/*
 * Callbacks for use with Pyrex, do-nothing functions in the stand-alone
 * simulator.  wware 060101
 */

extern void callback_writeFrame(struct part *part, struct xyz *pos);

// wware 060102  callback for trace file
extern void write_traceline(const char *format, ...);

// Python exception stuff, wware 060109
extern char *py_exc_str;
extern void set_py_exc_str(const char *filename, const char *funcname,
			   const char *format, ...);

// define this to test the exception handling in pyrex sim.  Each null
// pointer check will occasionally fail.
//#define RANDOM_FAILURES 0.0001
#ifdef RANDOM_FAILURES
#define RFAIL (((double)random())/((double)RAND_MAX) < RANDOM_FAILURES) ||
#else
#define RFAIL
#endif

#define NULLPTR(p)  \
  if (RFAIL (p) == NULL) { SAY("NULLPTR\n"); \
  set_py_exc_str(__FILE__, __FUNCTION__, "%s is null", #p); return; }
#define NULLPTRR(p,x)  \
  if (RFAIL (p) == NULL) { SAY("NULLPTRR\n"); \
  set_py_exc_str(__FILE__, __FUNCTION__, "%s is null", #p); return (x); }
#define EXCEPTION (py_exc_str != NULL)
#define BAIL()  \
  if (EXCEPTION) { SAY("BAIL\n"); return; }
#define BAILR(x)  \
  if (EXCEPTION) { SAY("BAILR\n"); return x; }

/*
 * Local Variables:
 * c-basic-offset: 4
 * tab-width: 8
 * End:
 */
