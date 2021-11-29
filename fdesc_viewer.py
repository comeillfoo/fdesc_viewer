#! /usr/bin/python3
import sys
import os
from os import path, replace
import json
from pipe import where

def is_running( pid ):
    try:
        os.kill( pid, 0 )
    except OSError:
        return False
    else:
        return True

_fdesc_modname = 'fdesc'
_fdesc_path = '/proc/fdescs'

def enter_while_in_set( prompt_msg, error_msg, set ):
    while ( True ):
        value = input( prompt_msg )
        if ( value in set ):
            return value
        else:
            if ( value == '-1' ):
                return value
            print( error_msg )

struct_file_fields = [ 'f_path.dentry', 'f_inode', 'f_op', 'f_mode', 'f_flags', 'f_pos', 'f_version', 'f_wb_err', 'f_sb_err' ]

def print_struct_file( fd, file ):
    print( f'{fd}:' )
    for field in struct_file_fields:
        print( f'\t{field}:\t{file[field]}' )


def main( argc, argv ):

    if ( not path.exists( _fdesc_path ) ):
        print( f'error: module {_fdesc_modname} not loaded...' )
    else:
        tasks = os.listdir( _fdesc_path )
        tasks = list( tasks | where( lambda task: is_running( int( task ) ) ) )
        print( 'list of available processes:' )
        print( '\t'.join( tasks ) )
        task = enter_while_in_set( 'enter the pid: ', 'entered unavailable pid, try again...', tasks )

        with open( f'{_fdesc_path}/{task}', 'r' ) as f:
            json_raw = "".join( f.readlines() )
            json_raw = json_raw.replace( '},}', '} }' )
            obj = json.loads( json_raw )
            print( 'list of available descriptors:' )
            print( '\t'.join( obj.keys() ) )
            fd = enter_while_in_set( 'enter the fd or -1 for all: ', 'entered invalid fd, try again...', obj.keys() )
            if ( fd == '-1' ):
                for itr in obj.keys():
                    print_struct_file( itr, obj[ itr ] )
            else:
                print_struct_file( fd, obj[ fd ] )

if ( __name__ == '__main__' ):
    try:
        main( len( sys.argv ), sys.argv )
    except KeyboardInterrupt:
        print( '\nsuccessfully halted...' )