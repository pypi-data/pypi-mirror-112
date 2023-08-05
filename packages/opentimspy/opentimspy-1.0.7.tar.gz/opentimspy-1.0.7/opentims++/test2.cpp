/*
 *   OpenTIMS: a fully open-source library for opening Bruker's TimsTOF data files.
 *   Copyright (C) 2020-2021 Michał Startek and Mateusz Łącki
 *
 *   This program is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License, version 3 only,
 *   as published by the Free Software Foundation.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#include <cassert>
#include "opentims.cpp"
#include "tof2mz_converter.cpp"
#include "scan2inv_ion_mobility_converter.cpp"

int main(int argc, char** argv)
{
    assert(argc == 2);
    //DefaultTof2MzConverterFactory::setAsDefault<BrukerTof2MzConverterFactory, const char*>("/home/mist/svn/git/timsdata_scratchpad/tims2hdf5/libtimsdata.so");
    //DefaultScan2InvIonMobilityConverterFactory::setAsDefault<BrukerScan2InvIonMobilityConverterFactory, const char*>("/home/mist/svn/git/timsdata_scratchpad/tims2hdf5/libtimsdata.so");
    TimsDataHandle TDH(argv[1]);
//    for(size_t ii = TDH.min_frame_id(); ii <= TDH.max_frame_id(); ii++)
    size_t ii = 2;
    {
        auto frame_size = TDH.expose_frame(ii);

        //TDH.get_frame(2).print();

        for(size_t jj = 0; jj < frame_size; jj++)
            
            std::cout << ii << "\t" << TDH.scan_ids_buffer()[jj] << "\t" << TDH.tofs_buffer()[jj] << "\t" << TDH.intensities_buffer()[jj] << std::endl;
//            std::cout << frames[ii] << "\t" << scans[ii] << "\t" << tofs[ii] << "\t" << intensities[ii] << std::endl;
    }
}
