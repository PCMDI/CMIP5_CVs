#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 22:10:37 2022

Paul J. Durack 10th February 2022

This script generates all controlled vocabulary (CV) json files residing this this subdirectory
"""
"""
PJD 10 Feb 2022     - Started
PJD 10 Feb 2022     - Updated following details at https://pcmdi.llnl.gov/mips/cmip5/docs/cmip5_data_reference_syntax.pdf?id=37

@author: durack1
"""

# %% imports

# %% Set commit message and author info
import datetime
import calendar
import gc
import json
import time
import os
import platform
commitMessage = '\"initialize CMIP5_CVs\"'
author = 'Paul J. Durack <durack1@llnl.gov>'
author_institution_id = 'PCMDI'

# %% List target controlled vocabularies (CVs)
masterTargets = [
    'activity_id',
    'experiment_id',
    'frequency',
    'grid_label',
    'institution_id',
    'license',
    'mip_era',
    'nominal_resolution',
    'realm',
    'required_global_attributes',
    'source_id',
    'source_type',
    'table_id'
]

# %% Activities
activity_id = {
    # Needs updating - should we map experiment-id values to CMIP6 equivalent activity_id values?
    'CMIP': 'CMIP DECK: 1pctCO2, abrupt4xCO2, amip, historical, and piControl experiments',
}

# %% Experiments
experiment_id = {
    'piControl': 'DECK: pre-industrial control',  # Needs checking
    'historical': 'CMIP5 historical',
    'midHolocene': '',
    'lgm': '',
    'past1000': '',
    'rcp45': 'future scenario with medium radiative forcing by the end of century. Following approximately 4.5 Wm-2 global forcing pathway. Concentration-driven',
    'rcp85': 'future scenario with high radiative forcing by the end of century. Following approximately 8.5 Wm-2 global forcing pathway. Concentration-driven',
    'rcp26': 'future scenario with low radiative forcing by the end of century. Following approximately 2.6 Wm-2 global forcing pathway. Concentration-driven',
    'rcp60': 'future scenario with medium radiative forcing by the end of century. Following approximately 6.0 Wm-2 global forcing pathway. Concentration-driven',
    'esmControl': 'DECK: pre-industrial control. Emissions-forced (atmospheric CO2 concentration determined by a model)',
    'esmHistorical': 'CMIP5 esmHistorical. Emissions-forced (atmospheric CO2 concentration determined by a model)',
    'esmrcp85': 'future scenario with high radiative forcing by the end of century. Following approximately 8.5 Wm-2 global forcing pathway. Emissions-forced (atmospheric CO2 concentration determined by a model)',
    'esmFixClim1': '',
    'esmFixClim2': '',
    'esmFdbk1': '',
    'esmFdbk2': '',
    '1pctCO2': 'DECK: 1pctCO2 to quadrupling',
    'abrupt4xCO2': 'DECK: abrupt-4xCO2 equilibrium experiment',
    'historicalNat': '',
    'historicalGHG': '',
    'historicalMisc': '',
    'historicalExt': '',
    'amip': 'DECK: AMIP (atmosphere-only model intercomparison project)',
    'sst2030': '',
    'sstClim': '',
    'sstClim4xCO2': '',
    'sstClimAerosol': '',
    'sstClimSulfate': '',
    'amip4xCO2': '',
    'amipFuture': '',
    'aquaControl': '',
    'aqua4xCO2': '',
    'aqua4K': '',
    'amip4K': '',
}

# %% Frequencies
frequency = {
    '1hr': 'sampled hourly',  # Needs updating
    '3hr': '3 hourly mean samples',
    '6hr': '6 hourly mean samples',
    'day': 'daily mean samples',
    'fx': 'fixed (time invariant) field',
    'mon': 'monthly mean samples',
    'monC': 'monthly climatology computed from monthly mean samples',
    'yr': 'annual mean samples',
}

# %% Grid labels
grid_label = {
    'gm': 'global mean data',  # Needs updating
    'gn': 'data reported on a model\'s native grid',
    'gnz': 'zonal mean data reported on a model\'s native latitude grid',
    'gr': 'regridded data reported on the data provider\'s preferred target grid',
    'gr1': 'regridded data reported on a grid other than the native grid and other than the preferred target grid',
    'gr1z': 'regridded zonal mean data reported on a grid other than the native latitude grid and other than the preferred latitude target grid',
    'grz': 'regridded zonal mean data reported on the data provider\'s preferred latitude target grid'
}

# %% Institutions
institution_id = {
    'AER': 'Research and Climate Group, Atmospheric and Environmental Research, 131 Hartwell Avenue, Lexington, MA 02421, USA',  # Needs updating
    'AS-RCEC': 'Research Center for Environmental Changes, Academia Sinica, Nankang, Taipei 11529, Taiwan',
    'AWI': 'Alfred Wegener Institute, Helmholtz Centre for Polar and Marine Research, Am Handelshafen 12, 27570 Bremerhaven, Germany',
    'BCC': 'Beijing Climate Center, Beijing 100081, China',
    'BNU': 'Beijing Normal University, Beijing 100875, China',
    'CAMS': 'Chinese Academy of Meteorological Sciences, Beijing 100081, China',
    'CAS': 'Chinese Academy of Sciences, Beijing 100029, China',
    'CCCR-IITM': 'Centre for Climate Change Research, Indian Institute of Tropical Meteorology Pune, Maharashtra 411 008, India',
    'CCCma': 'Canadian Centre for Climate Modelling and Analysis, Environment and Climate Change Canada, Victoria, BC V8P 5C2, Canada',
    'CMCC': 'Fondazione Centro Euro-Mediterraneo sui Cambiamenti Climatici, Lecce 73100, Italy',
    'CNRM-CERFACS': ''.join(['CNRM (Centre National de Recherches Meteorologiques, Toulouse 31057, France), CERFACS (Centre Europeen de Recherche ',
                             'et de Formation Avancee en Calcul Scientifique, Toulouse 31057, France)']),
    'CSIR-Wits-CSIRO': ''.join(['CSIR (Council for Scientific and Industrial Research - Natural Resources and the Environment, Pretoria, 0001, South Africa), ',
                                'Wits (University of the Witwatersrand - Global Change Institute, Johannesburg 2050, South Africa), ',
                                'CSIRO (Commonwealth Scientific and Industrial Research Organisation, Aspendale, Victoria 3195, Australia)',
                                'Mailing address: Wits, Global Change Institute, Johannesburg 2050, South Africa']),
    'CSIRO': 'Commonwealth Scientific and Industrial Research Organisation, Aspendale, Victoria 3195, Australia',
    'CSIRO-ARCCSS': ' '.join(['CSIRO (Commonwealth Scientific and Industrial Research Organisation, Aspendale, Victoria 3195, Australia),',
                              'ARCCSS (Australian Research Council Centre of Excellence for Climate System Science).',
                              'Mailing address: CSIRO, c/o Simon J. Marsland,',
                              '107-121 Station Street, Aspendale, Victoria 3195, Australia']),
    'CSIRO-COSIMA': ' '.join(['CSIRO (Commonwealth Scientific and Industrial Research Organisation, Australia),',
                              'COSIMA (Consortium for Ocean-Sea Ice Modelling in Australia).',
                              'Mailing address: CSIRO, c/o Simon J. Marsland,',
                              '107-121 Station Street, Aspendale, Victoria 3195, Australia']),
    'DKRZ': 'Deutsches Klimarechenzentrum, Hamburg 20146, Germany',
    'DWD': 'Deutscher Wetterdienst, Offenbach am Main 63067, Germany',
    'E3SM-Project': ''.join(['LLNL (Lawrence Livermore National Laboratory, Livermore, CA 94550, USA); ',
                             'ANL (Argonne National Laboratory, Argonne, IL 60439, USA); ',
                             'BNL (Brookhaven National Laboratory, Upton, NY 11973, USA); ',
                             'LANL (Los Alamos National Laboratory, Los Alamos, NM 87545, USA); ',
                             'LBNL (Lawrence Berkeley National Laboratory, Berkeley, CA 94720, USA); ',
                             'ORNL (Oak Ridge National Laboratory, Oak Ridge, TN 37831, USA); ',
                             'PNNL (Pacific Northwest National Laboratory, Richland, WA 99352, USA); ',
                             'SNL (Sandia National Laboratories, Albuquerque, NM 87185, USA). ',
                             'Mailing address: LLNL Climate Program, c/o David C. Bader, ',
                             'Principal Investigator, L-103, 7000 East Avenue, Livermore, CA 94550, USA']),
    'EC-Earth-Consortium': ''.join(['AEMET, Spain; BSC, Spain; CNR-ISAC, Italy; DMI, Denmark; ENEA, Italy; FMI, Finland; Geomar, Germany; ICHEC, ',
                                    'Ireland; ICTP, Italy; IDL, Portugal; IMAU, The Netherlands; IPMA, Portugal; KIT, Karlsruhe, Germany; KNMI, ',
                                    'The Netherlands; Lund University, Sweden; Met Eireann, Ireland; NLeSC, The Netherlands; NTNU, Norway; Oxford ',
                                    'University, UK; surfSARA, The Netherlands; SMHI, Sweden; Stockholm University, Sweden; Unite ASTR, Belgium; ',
                                    'University College Dublin, Ireland; University of Bergen, Norway; University of Copenhagen, Denmark; ',
                                    'University of Helsinki, Finland; University of Santiago de Compostela, Spain; Uppsala University, Sweden; ',
                                    'Utrecht University, The Netherlands; Vrije Universiteit Amsterdam, the Netherlands; Wageningen University, ',
                                    'The Netherlands. Mailing address: EC-Earth consortium, Rossby Center, Swedish Meteorological and Hydrological ',
                                    'Institute/SMHI, SE-601 76 Norrkoping, Sweden']),
    'ECMWF': 'European Centre for Medium-Range Weather Forecasts, Reading RG2 9AX, UK',
    'FIO-QLNM': ''.join(['FIO (First Institute of Oceanography, Ministry of Natural Resources, Qingdao 266061, China), ',
                         'QNLM (Qingdao National Laboratory for Marine Science and Technology, Qingdao 266237, China)']),
    'HAMMOZ-Consortium': ''.join(['ETH Zurich, Switzerland; Max Planck Institut fur Meteorologie, Germany; Forschungszentrum Julich, ',
                                  'Germany; University of Oxford, UK; Finnish Meteorological Institute, Finland; Leibniz Institute for Tropospheric ',
                                  'Research, Germany; Center for Climate Systems Modeling (C2SM) at ETH Zurich, Switzerland']),
    'INM': 'Institute for Numerical Mathematics, Russian Academy of Science, Moscow 119991, Russia',
    'INPE': 'National Institute for Space Research, Cachoeira Paulista, SP 12630-000, Brazil',
    'IPSL': 'Institut Pierre Simon Laplace, Paris 75252, France',
    'KIOST': 'Korea Institute of Ocean Science and Technology, Busan 49111, Republic of Korea',
    'LLNL': ' '.join(['Lawrence Livermore National Laboratory, Livermore,',
                      'CA 94550, USA. Mailing address: LLNL Climate Program,',
                      'c/o Stephen A. Klein, Principal Investigator, L-103,',
                      '7000 East Avenue, Livermore, CA 94550, USA']),
    'MESSy-Consortium': ''.join(['The Modular Earth Submodel System (MESSy) Consortium, represented by the Institute for Physics of the Atmosphere, ',
                                 'Deutsches Zentrum fur Luft- und Raumfahrt (DLR), Wessling, Bavaria 82234, Germany']),
    'MIROC': ''.join(['JAMSTEC (Japan Agency for Marine-Earth Science and Technology, Kanagawa 236-0001, Japan), ',
                      'AORI (Atmosphere and Ocean Research Institute, The University of Tokyo, Chiba 277-8564, Japan), ',
                      'NIES (National Institute for Environmental Studies, Ibaraki 305-8506, Japan), ',
                      'and R-CCS (RIKEN Center for Computational Science, Hyogo 650-0047, Japan)']),
    'MOHC': 'Met Office Hadley Centre, Fitzroy Road, Exeter, Devon, EX1 3PB, UK',
    'MPI-M': 'Max Planck Institute for Meteorology, Hamburg 20146, Germany',
    'MRI': 'Meteorological Research Institute, Tsukuba, Ibaraki 305-0052, Japan',
    'NASA-GISS': 'Goddard Institute for Space Studies, New York, NY 10025, USA',
    'NASA-GSFC': 'NASA Goddard Space Flight Center, Greenbelt, MD 20771, USA',
    'NCAR': 'National Center for Atmospheric Research, Climate and Global Dynamics Laboratory, 1850 Table Mesa Drive, Boulder, CO 80305, USA',
    'NCC': ''.join(['NorESM Climate modeling Consortium consisting of ',
                    'CICERO (Center for International Climate and Environmental Research, Oslo 0349), ',
                    'MET-Norway (Norwegian Meteorological Institute, Oslo 0313), ',
                    'NERSC (Nansen Environmental and Remote Sensing Center, Bergen 5006), ',
                    'NILU (Norwegian Institute for Air Research, Kjeller 2027), ',
                    'UiB (University of Bergen, Bergen 5007), ',
                    'UiO (University of Oslo, Oslo 0313) ',
                    'and UNI (Uni Research, Bergen 5008), Norway. Mailing address: NCC, c/o MET-Norway, ',
                    'Henrik Mohns plass 1, Oslo 0313, Norway']),
    'NERC': 'Natural Environment Research Council, STFC-RAL, Harwell, Oxford, OX11 0QX, UK',
    'NIMS-KMA': ' '.join(['National Institute of Meteorological Sciences/Korea',
                          'Meteorological Administration, Climate Research',
                          'Division, Seoho-bukro 33, Seogwipo-si, Jejudo 63568,',
                          'Republic of Korea']),
    'NIWA': 'National Institute of Water and Atmospheric Research, Hataitai, Wellington 6021, New Zealand',
    'NOAA-GFDL': 'National Oceanic and Atmospheric Administration, Geophysical Fluid Dynamics Laboratory, Princeton, NJ 08540, USA',
    'NTU': 'National Taiwan University, Taipei 10650, Taiwan',
    'NUIST': 'Nanjing University of Information Science and Technology, Nanjing, 210044, China',
    'PCMDI': 'Program for Climate Model Diagnosis and Intercomparison, Lawrence Livermore National Laboratory, Livermore, CA 94550, USA',
    'PNNL-WACCEM': 'PNNL (Pacific Northwest National Laboratory), Richland, WA 99352, USA',
    'RTE-RRTMGP-Consortium': ''.join(['AER (Atmospheric and Environmental Research, Lexington, MA 02421, USA); UColorado (University of Colorado, ',
                                      'Boulder, CO 80309, USA). Mailing address: AER c/o Eli Mlawer, 131 Hartwell Avenue, Lexington, MA 02421, USA']),
    'RUBISCO': ''.join(['ORNL (Oak Ridge National Laboratory, Oak Ridge, TN 37831, USA); ANL (Argonne National Laboratory, Argonne, IL 60439, USA); ',
                        'BNL (Brookhaven National Laboratory, Upton, NY 11973, USA); LANL (Los Alamos National Laboratory, Los Alamos, NM 87545); ',
                        'LBNL (Lawrence Berkeley National Laboratory, Berkeley, CA 94720, USA); NAU (Northern Arizona University, Flagstaff, AZ 86011, USA); ',
                        'NCAR (National Center for Atmospheric Research, Boulder, CO 80305, USA); UCI (University of California Irvine, Irvine, CA 92697, USA); ',
                        'UM (University of Michigan, Ann Arbor, MI 48109, USA). Mailing address: ORNL Climate Change Science Institute, c/o Forrest M. Hoffman, ',
                        'Laboratory Research Manager, Building 4500N Room F106, 1 Bethel Valley Road, Oak Ridge, TN 37831-6301, USA']),
    'SNU': 'Seoul National University, Seoul 08826, Republic of Korea',
    'THU': 'Department of Earth System Science, Tsinghua University, Beijing 100084, China',
    'UA': 'Department of Geosciences, University of Arizona, Tucson, AZ 85721, USA',
    'UCI': 'Department of Earth System Science, University of California Irvine, Irvine, CA 92697, USA',
    'UHH': 'Universitat Hamburg, Hamburg 20148, Germany',
    'UTAS': 'Institute for Marine and Antarctic Studies, University of Tasmania, Hobart, Tasmania 7001, Australia',
    'UofT': 'Department of Physics, University of Toronto, 60 St George Street, Toronto, ON M5S1A7, Canada'
}

# %% CMIP6 License
license = [
    ''.join(['CMIP6 model data produced by <Your Centre Name> is licensed under a Creative Commons ',  # Needs updating
             'Attribution-[NonCommercial-]ShareAlike 4.0 International License ',
             '(https://creativecommons.org/licenses). Consult https://pcmdi.llnl.gov/CMIP6/TermsOfUse ',
             'for terms of use governing CMIP6 output, including citation requirements and proper ',
             'acknowledgment. Further information about this data, including some limitations, can be ',
             'found via the further_info_url (recorded as a global attribute in this file)[ and at ',
             '<some URL maintained by modeling group>]. The data producers and data providers make ',
             'no warranty, either express or implied, including, but not limited to, warranties of ',
             'merchantability and fitness for a particular purpose. All liabilities arising from the ',
             'supply of the information (including any liability arising in negligence) are excluded ',
             'to the fullest extent permitted by law.'])
]

# %% MIP eras
mip_era = ['AMIP1', 'AMIP2', 'CMIP1', 'CMIP2', 'CMIP3']

# %% Nominal resolutions
nominal_resolution = [
    '0.5 km',
    '1 km',
    '10 km',
    '100 km',
    '1000 km',
    '10000 km',
    '1x1 degree',
    '2.5 km',
    '25 km',
    '250 km',
    '2500 km',
    '5 km',
    '50 km',
    '500 km',
    '5000 km'
]

# %% Realms
realm = {
    'aerosol': 'Aerosol',
    'atmos': 'Atmosphere',
    'atmosChem': 'Atmospheric Chemistry',
    'land': 'Land Surface',
    'landIce': 'Land Ice',
    'ocean': 'Ocean',
    'ocnBgchem': 'Ocean Biogeochemistry',
    'seaIce': 'Sea Ice'
}

# %% Required global attributes
required_global_attributes = [
    'Conventions',
    'comment',
    'contact',
    'experiment_id',
    'history',
    'institution',
    'project_id',
    'realization',
    'references',
    'source',
    'table_id',
    'title',
]

# %% Source identifiers

# %% Source types
source_type = {
    # Needs update
    'AER': 'aerosol treatment in an atmospheric model where concentrations are calculated based on emissions, transformation, and removal processes (rather than being prescribed or omitted entirely)',
    'AGCM': 'atmospheric general circulation model run with prescribed ocean surface conditions and usually a model of the land surface',
    'AOGCM': 'coupled atmosphere-ocean global climate model, additionally including explicit representation of at least the land and sea ice',
    'BGC': 'biogeochemistry model component that at the very least accounts for carbon reservoirs and fluxes in the atmosphere, terrestrial biosphere, and ocean',
    'CHEM': 'chemistry treatment in an atmospheric model that calculates atmospheric oxidant concentrations (including at least ozone), rather than prescribing them',
    'ISM': 'ice-sheet model that includes ice-flow',
    'LAND': 'land model run uncoupled from the atmosphere',
    'OGCM': 'ocean general circulation model run uncoupled from an AGCM but, usually including a sea-ice model',
    'RAD': 'radiation component of an atmospheric model run \'offline\'',
    'SLAB': 'slab-ocean used with an AGCM in representing the atmosphere-ocean coupled system'
}

# %% Sub experiment ids

# %% Table ids
table_id = [
    '3hr',  # Needs update
    '6hrLev',
    '6hrPlev',
    '6hrPlevPt',
    'AERday',
    'AERhr',
    'AERmon',
    'AERmonZ',
    'Amon',
    'CF3hr',
    'CFday',
    'CFmon',
    'CFsubhr',
    'E1hr',
    'E1hrClimMon',
    'E3hr',
    'E3hrPt',
    'E6hrZ',
    'Eday',
    'EdayZ',
    'Efx',
    'Emon',
    'EmonZ',
    'Esubhr',
    'Eyr',
    'IfxAnt',
    'IfxGre',
    'ImonAnt',
    'ImonGre',
    'IyrAnt',
    'IyrGre',
    'LImon',
    'Lmon',
    'Oclim',
    'Oday',
    'Odec',
    'Ofx',
    'Omon',
    'Oyr',
    'SIday',
    'SImon',
    'day',
    'fx'
]

# %% Write variables to files
timeNow = datetime.datetime.now().strftime('%c')
offset = (calendar.timegm(time.localtime()) -
          calendar.timegm(time.gmtime()))/60/60  # Convert seconds to hrs
# offset = ''.join(['{:03d}'.format(offset),'00']) # Pad with 00 minutes # Py2
offset = ''.join(['{:03d}'.format(int(offset)), '00']
                 )  # Pad with 00 minutes # Py3
timeStamp = ''.join([timeNow, ' ', offset])
del(timeNow, offset)

for jsonName in masterTargets:
    # Write file
    if jsonName == 'mip_era':
        outFile = ''.join(['../', jsonName, '.json'])
    else:
        outFile = ''.join(['../CMIP6_', jsonName, '.json'])
    # Get repo version/metadata - from src/writeJson.py

    # Extract last recorded commit for src/writeJson.py
    # print(os.path.realpath(__file__))
    versionInfo1 = getFileHistory(os.path.realpath(__file__))
    versionInfo = {}
    versionInfo['author'] = author
    versionInfo['institution_id'] = author_institution_id
    versionInfo['CV_collection_modified'] = timeStamp
    versionInfo['CV_collection_version'] = versionId
    versionInfo['_'.join([jsonName, 'CV_modified'])
                ] = versionHistory[jsonName]['timeStamp']
    versionInfo['_'.join([jsonName, 'CV_note'])
                ] = versionHistory[jsonName]['commitMessage']
    versionInfo['previous_commit'] = versionInfo1.get('previous_commit')
    versionInfo['specs_doc'] = 'v6.2.7 (10th September 2018; https://goo.gl/v1drZl)'
    del(versionInfo1)

    # Check file exists
    if os.path.exists(outFile):
        print('File existing, purging:', outFile)
        os.remove(outFile)
    # Create host dictionary
    jsonDict = {}
    jsonDict[jsonName] = eval(jsonName)
    # Append repo version/metadata
    jsonDict['version_metadata'] = versionInfo
    fH = open(outFile, 'w')
    if platform.python_version().split('.')[0] == '2':
        json.dump(
            jsonDict,
            fH,
            ensure_ascii=True,
            sort_keys=True,
            indent=4,
            separators=(
                ',',
                ':'),
            encoding="utf-8")
    elif platform.python_version().split('.')[0] == '3':
        json.dump(
            jsonDict,
            fH,
            ensure_ascii=True,
            sort_keys=True,
            indent=4,
            separators=(
                ',',
                ':'))
    fH.close()

# Cleanup
del(jsonName, jsonDict, outFile)
del(activity_id, experiment_id, frequency, grid_label, institution_id, license,
    masterTargets, mip_era, nominal_resolution, realm, required_global_attributes,
    source_id, source_type, sub_experiment_id, table_id)
gc.collect()
