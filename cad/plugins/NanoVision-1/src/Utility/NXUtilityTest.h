// Copyright 2008 Nanorex, Inc.  See LICENSE file for details.

#ifndef NX_UTILITYTEST_H
#define NX_UTILITYTEST_H

#pragma warning(disable:4786)
#include <iostream>
#include <fstream>
#include <string>

#include <cppunit/extensions/HelperMacros.h>

#include <Nanorex/Utility/NXUtility.h>


/* CLASS: NXUtilityTest */
class NXUtilityTest : public CPPUNIT_NS::TestFixture {

	CPPUNIT_TEST_SUITE(NXUtilityTest);
	CPPUNIT_TEST_SUITE_END();

	public:
		void setUp();
		void tearDown();
};

#endif
