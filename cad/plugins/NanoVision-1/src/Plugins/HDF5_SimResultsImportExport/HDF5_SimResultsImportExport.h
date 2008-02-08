// Copyright 2008 Nanorex, Inc.  See LICENSE file for details.

#ifndef NX_HDF5_SIMRESULTSIMPORTEXPORT_H
#define NX_HDF5_SIMRESULTSIMPORTEXPORT_H

#ifdef WIN32
#	ifdef _MSC_VER
#		pragma warning(disable:4786)
#	endif
#endif

#include <QDir>
#include <QFile>
#include <QObject>
#include <QString>
#include <QFileInfo>

#include "Nanorex/HDF5_SimResults.h"
#include "Nanorex/Utility/NXLogger.h"
#include "Nanorex/Utility/NXCommandResult.h"
#include "Nanorex/Interface/NXNumbers.h"
#include "Nanorex/Interface/NXNanoVisionResultCodes.h"
#include "Nanorex/Interface/NXDataImportExportPlugin.h"
using namespace Nanorex;

#include <vector>
using namespace std;


/* CLASS: HDF5_SimResultsImportExport */
class HDF5_SimResultsImportExport
		: public QObject, public NXDataImportExportPlugin {
	Q_OBJECT
	Q_INTERFACES(Nanorex::NXDataImportExportPlugin)
		
public:
    HDF5_SimResultsImportExport();
    ~HDF5_SimResultsImportExport();
    
                // NXDataImportExportPlugin implementation
    NXCommandResult* importFromFile(NXMoleculeSet* moleculeSet,
                                    NXDataStoreInfo* dataStoreInfo,
                                    const std::string& filename,
                                    int frameSetId, int frameIndex);
    NXCommandResult* exportToFile(NXMoleculeSet* moleculeSet,
                                NXDataStoreInfo* dataStoreInfo,
                                const std::string& filename,
                                int frameSetId, int frameIndex);
    
private:
    void populateDataStoreInfo(NXDataStoreInfo* dataStoreInfo,
                            HDF5_SimResults* simResults,
                            int frameSetId);
    void exportToFileHelper(NXMoleculeSet* moleculeSet,
                            unsigned int atomIndex, unsigned int bondIndex,
                            unsigned int* atomIds,
                            unsigned int* atomicNumbers,
                            float* positions, void* bonds,
                            NXCommandResult* result);
    void populateCommandResult(NXCommandResult* result,
                            const string& message);
	string parseSuffix(const string& filename);
};

#endif
