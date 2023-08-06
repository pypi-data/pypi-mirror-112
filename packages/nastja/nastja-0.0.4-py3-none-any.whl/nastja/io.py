"""
io.py
====================================
Input and output interface to NAStJA simulations.
"""

from glob import glob
import os
import fnmatch
import json
import pandas as pd
import numpy as np
import sqlite3
import warnings

vtisupport = True
try:
    import pyvista as pv
except ImportError:
    import sys
    print("Package 'pyvista' not found. To enable vtk support, please install it. Note: vtk and hence pyvista is not "
          "available on every platform.", file=sys.stderr)
    vtisupport = False


class SimDir():
    """
    This class describes a simulation directory.
    """

    def __init__(self, path):
        """
        Constructs a new instance.

        :param path:  The path of the NAStJA simulation output.
        """
        self.__basename = "output_cells-"
        self.__hasVTI = False
        self.__hasCSV = False
        self.__hasSQL = False
        self.__frames = 0
        self.__configname = "config_save.json"
        self.__con = 0
        self.path = path

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path):
        self.__path = os.path.expanduser(path)
        self.reload()

    @property
    def hasVTI(self):
        return self.__hasVTI

    @property
    def hasCSV(self):
        return self.__hasCSV

    @property
    def hasSQL(self):
        return self.__hasSQL

    @property
    def frames(self):
        return self.__frames

    def __maximumFrame(self, files):
        """
        Determine the maximum available frame from a file list. Checks also if the frames are continues.

        :param files:  The files.

        :returns: The maximum available frames
        """
        if len(files) != int(files[-1][-9:-4]) + 1:
            warnings.warn("Warning: Frame numbers are not complete")

        return int(files[-1][-9:-4]) + 1

    def reload(self):
        """
        Reload vti, csv file from path and determine the largest frames.
        This function is called when the path is set.
        """
        files = os.listdir(self.path)

        vti = fnmatch.filter(files, self.__basename +
                             "[0-9][0-9][0-9][0-9][0-9].vti")
        csv = fnmatch.filter(files, self.__basename +
                             "[0-9][0-9][0-9][0-9][0-9].csv")
        sql = fnmatch.filter(files, "*.sqlite")

        framesvti = 0
        if vti:
            vti.sort()
            self.__hasVTI = True
            framesvti = self.__maximumFrame(vti)

        framescsv = 0
        if csv:
            csv.sort()
            self.__hasCSV = True
            framescsv = self.__maximumFrame(csv)

        framessql = 0
        if sql:
            self.__hasSQL = True
            if len(sql) > 1:
                print("Found more than one database. Loading", sql[0])

            self.__con = sqlite3.connect(self.__path + "/" + sql[0])
            cur = self.__con.cursor()
            row = cur.execute("SELECT MAX(frame) FROM cells").fetchone()
            framessql = row[0] + 1

        self.__frames = max(framesvti, framescsv, framessql)

        if ((self.hasVTI and self.__frames != framesvti) or
            (self.hasCSV and self.__frames != framescsv) or
                (self.hasSQL and self.__frames != framessql)):
            warnings.warn("Warning: Data types vary in frame numbers")

    def __createFilename(self, frame, extension):
        return self.path + "/" + self.__basename + "%05d" % frame + extension

    def readVTI(self, frame):
        """
        Reads a vti file.

        :param frame:  The frame number.

        :returns: A pyVista object.
        """
        if not vtisupport:
            raise NotImplementedError(
                "No vti support due to missing 'pyvista'.")

        if frame not in range(0, self.__frames):
            raise IndexError("Frame {} is not available".format(frame))

        return pv.read(self.__createFilename(frame, ".vti"))

    def readCSV(self, frame):
        """
        Reads a csv file.

        :param frame:  The frame number.

        :returns: A dataframe.
        """
        if frame not in range(0, self.__frames):
            raise IndexError("Frame {} is not available".format(frame))

        data = pd.read_csv(self.__createFilename(frame, ".csv"), delim_whitespace=True, index_col=False)
        return data.rename(columns={"#CellID": "CellID"})

    def readSQL(self, frame):
        """
        Reads a sql file.

        :param frame:  The frame number.

        :returns: A dataframe.
        """
        if not self.__con:
            raise NameError("No database connection found")

        if frame not in range(0, self.__frames):
            raise IndexError("Frame {} is not available".format(frame))

        data = pd.read_sql_query(
            "SELECT CellID, CenterX, CenterY, CenterZ, Volume, Surface, Typ, Signal0, Signal1, Signal2, Age FROM cells "
            "WHERE frame=" + str(frame) + ";", self.__con)
        return data

    def query(self, query):
        """
        Queries a sql file.

        :param query:  The query string.

        :returns: A dataframe.
        """
        if not self.__con:
            raise NameError("No database connection found")

        data = pd.read_sql_query(query, self.__con)
        return data

    def readConfig(self):
        """
        Reads the saved configuration file from the simulation.

        :returns: A Python object of the JSON config.
        """
        with open(self.path + "/" + self.__configname) as json_file:
            return json.load(json_file)

    def mappedArray(self, array, dataframe, column):
        """
        Create a mapped array, replace cellID with the value of the given column.

        :param array:      The numpy array.
        :param dataframe:  The dataframe.
        :param column:     The name of the column.

        :returns: A mapped array.
        """
        ret = np.empty(array.shape)
        for index, row in dataframe.iterrows():
            ret[array == row["CellID"]] = row[column]
        return ret
