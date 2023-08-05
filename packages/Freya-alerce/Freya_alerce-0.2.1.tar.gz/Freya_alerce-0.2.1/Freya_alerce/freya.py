#command Freya
from Freya_alerce.core.commands.addcatalog import AddCatalog
from Freya_alerce.core.commands.addcataloglocal import AddCatalogLocal
from Freya_alerce.core.commands.addresource import AddResource
from Freya_alerce.core.commands.newapi import NewAPI
from Freya_alerce.core.commands.renamecatalog import RenameCatalog
from Freya_alerce.core.commands.deletecatalog import DeleteCatalog
#
import Freya_alerce.catalogs # __path__
#
import os
import argparse
import sys

"""
Define the CLI for Freya specific command line. 
"""
class Main(object):

    def main():

        #----------------------------COMMAND LINE----------------------------------------------#
        #parser = argparse.ArgumentParser()
        formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=75)
        parser = argparse.ArgumentParser(formatter_class=formatter)
        #--------------------------------------------------------------------------------------#

        #--------------------------------------------------------------------------------------#
        parser.add_argument('-nc','--newcatalog', action='store', 
                            metavar=('<name>','<source>'),
                            help="add new catalog inside Freya",
                            type=str, nargs=2)
        #--------------------------------------------------------------------------------------#
        parser.add_argument('-ncl','--newcataloglocal', action='store', 
                            metavar=('<name>','<source>'),
                            help="add new catalog who local module",
                            type=str, nargs=2)
        #--------------------------------------------------------------------------------------#
        parser.add_argument('-rc','--renamecatalog', action='store', 
                            metavar=('<old_name>','<new_name'),
                            help="rename catalog inside Freya",
                            type=str, nargs=2)
        #--------------------------------------------------------------------------------------#
        parser.add_argument('-dc','--deletecatalog', action='store', 
                            metavar=('<name>'),
                            help="delete catalog inside Freya",
                            type=str, nargs=1)
        #--------------------------------------------------------------------------------------# 
        parser.add_argument('-na','--newapi', action='store_true', 
                            help="create a new FreyaAPI")
        #--------------------------------------------------------------------------------------#                        
        parser.add_argument('-ar','--addresource', action='store',
                            metavar='<name>',
                            help="add module catalog who resource in FreyaApi",
                            type=str, nargs=1)
        #--------------------------------------------------------------------------------------#
        args = parser.parse_args()

        """
        Check what was the command line called, try call associated method.
        """
        if args.newcatalog :
            print("Created new catalogue...")
            try:
                AddCatalog(name=args.newcatalog[0],source=args.newcatalog[1],path=Freya_alerce.catalogs.__path__[0])
            except:
                raise TypeError (f'Failed to create new catalogue : {args.newcatalog[0]} inside Freya')

        elif args.newcataloglocal : 
            print("Created new local catalogue...")
            try:
                AddCatalogLocal(name=args.newcataloglocal[0],source =args.newcataloglocal[1],path=os.getcwd())
            except:
                raise TypeError ('Fauled to create local module')

        elif args.renamecatalog : 
            print("Rename catalogue...")
            try:
                RenameCatalog(name=args.renamecatalog[0],new_name=args.renamecatalog[1],path=Freya_alerce.catalogs.__path__[0])
            except:
                raise TypeError ('Fauled to raname')
        
        elif args.deletecatalog : 
            print("Delete catalogue...")
            try:
                DeleteCatalog(name=args.deletecatalog[0],path=Freya_alerce.catalogs.__path__[0])
            except:
                raise TypeError ('Fauled to delete')

        elif args.newapi :
            print("Created new FreyaAPI...")
            try:
                NewAPI(path=os.getcwd())
            except:
                raise TypeError ('Failed to create new base to FreaAPI')

        elif args.addresource : 
            print("Add new resource to FreyaAPI...")
            try:
                AddResource(name=args.addresource[0],path=os.getcwd())
            except:
                raise TypeError (f'Failed to create resouce : {args.addresource[0]} inside FreyaAPI')


if __name__ == ' __main__':
          Main().main()