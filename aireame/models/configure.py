# -*- coding: utf-8 -*- 
# Este fichero forma parte de airea.me
#
# Copyright 2011 Plexxoo Interactiva S.L.
# Copyright Daniel Gonzalez     <demetrio@plexxoo.com>
# Copyright Jon Latorre         <moebius@plexxoo.com>
# Copyright Silvia Martín       <smartin@plexxoo.com>
# Copyright Jesus Martinez      <jamarcer@plexxoo.com>
#
# Este fichero se distribuye bajo la licencia GPL según las
# condiciones que figuran en el fichero 'licence' que se acompaña.
# Si se distribuyera este fichero individualmente, DEBE incluirse aquí
# las condiciones expresadas allí.
#
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os
import yaml

from gluon.storage import Storage

class File:
    """
    This class implements the basic statics methods to handle a file.
    """
    @staticmethod        
    def exists(filename):
        """
       Checks if file exists.

        Keyword arguments:
        filename -- file name (path)
        """
        try:
            return os.path.exists(filename)
        except IOError, (errno, errstr):
            #print("I/O Error (%s): %s <%s>" % (errno, errstr, filename))
            return False
            
    @staticmethod        
    def save(filename, data):
        """
        Saves data in a file.

        Keyword arguments:
        filename -- file name (path)
        data -- data to save in file
        """
        try:
            fh = open(filename, 'w')
            fh.write(data)
            fh.close()
        except IOError, (errno, errstr):
            #print("I/O Error (%s): %s <%s>" % (errno, errstr, filename))
            data = None
     
    @staticmethod   
    def load(filename):
        """
        Returns data from a file.

        Keyword arguments:
        filename -- file name (path)
        """
        try:
            fh = open(filename)
            data = fh.read()
            fh.close()
        except IOError, (errno, errstr):
            #print("I/O Error (%s): %s <%s>" % (errno, errstr, filename))
            data = None
        return data
    
    @staticmethod        
    def touch(filename):
        """
        Touches a file. Creates an empty file.

        Keyword arguments:
        filename -- file name (path)
        """
        open(filename, 'w').close() 
    
    @staticmethod        
    def copy(origin, destiny):
        """
        Copies a file in another file.

        Keyword arguments:
        origin -- file name (path) to copy
        destiny -- file name (path)
        """
        import shutil
        shutil.copy2(origin, destiny)
    
    @staticmethod        
    def remove(filepath):
        """
        Deletes a file.

        Keyword arguments:
        filename -- file name (path)
        """
        os.remove(filepath)
        
class YAMLFile:   
    """
    This class implements the basic statics methods to handle a YAML formated file.
    """     
    @staticmethod          
    def load(filename):  
        """
        Returns data from a YAML formated file.

        Keyword arguments:
        filename -- file name (path)
        """
        return yaml.load(File.load(filename))
        
    @staticmethod          
    def save(filename, data, sort=False):
        """
        Saves data in a YAML formated file.

        Keyword arguments:
        filename -- file name (path)
        data -- data to save in file
        sort -- data must be sorted (default is False)
        """
        if sort:
            data.sort()

        File.save(filename, yaml.dump(data, default_flow_style=False))


class Configure():
    """
    This class implements a configurable set of options
    for use in anything that needs settings that
    are to be stored in a YAML formated file.
    """
    def __init__(self,filename=None,autosave=True):
        """
        Initialize configure class.
        """
        if filename is None:
            filename=CONFIG_PATH
            if File.exists(filename) is False:
                os.mkdir(os.path.dirname(filename))
                File.touch(filename)
        self.filename=filename
        self.autosave=autosave
        self._get_settings()
        
    def _get_settings(self):
        """
        Retrieves the settings from the YAML formated file and
        stores them in a storage dictionary
        """
        data=None
        if self.filename is not None:
            if File.exists(self.filename):
                data=YAMLFile.load(self.filename)
            else:
                data=None

        if data is not None:
            self.settings = Storage(data)
        else:
            self.settings = Storage() 
                  

    def settings(self,data):
        """
        Returns the value of a settings object

        Keyword arguments:
        name -- setting name
        """
        self.settings=Storage(data)

    def get(self,name):
        """
        Returns the value of a settings object. (Returns None if setting not exists)

        Keyword arguments:
        name -- setting name
        """
        try:
            return self.settings[name]
        except:
            return None

    def set(self,name,value):
        """
        Returns the value of a settings object

        Keyword arguments:
        name -- setting name
        value -- value for the setting
        """
        self.settings[name]=value
        if self.autosave:
            self.save()

    def save(self):
        """
        Writes all settings to the YAML formated file
        """
        if self.filename is not None:
            YAMLFile.save(self.filename,dict(self.settings))
            
    def __repr__(self):
        return "<Configure '%s'[%s] %s >" % (self.filename,self.autosave,self.settings)
  