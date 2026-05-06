#!/usr/bin/env python3
"""
Copy `finished-manuscript/` into `finished-manuscript-reorg/original_copy/`.
Usage:
  python copy_finished_manuscript.py [--src PATH] [--dst PATH] [--force]

This script is intentionally simple and non-destructive by default.
"""
import os
import sys
import shutil
import argparse

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    default_src = os.path.abspath(os.path.join(here, '..', '..', 'finished-manuscript'))
    default_dst = os.path.abspath(os.path.join(here, '..', 'original_copy'))

    p = argparse.ArgumentParser(description='Copy finished-manuscript into this reorg folder')
    p.add_argument('--src', default=default_src, help='Source finished-manuscript folder')
    p.add_argument('--dst', default=default_dst, help='Destination copy folder (created)')
    p.add_argument('--force', action='store_true', help='Overwrite destination if exists')
    args = p.parse_args()

    if not os.path.isdir(args.src):
        print('Source not found:', args.src)
        sys.exit(1)

    if os.path.exists(args.dst):
        if args.force:
            print('Removing existing destination:', args.dst)
            shutil.rmtree(args.dst)
        else:
            print('Destination already exists:', args.dst)
            print('Run with --force to overwrite')
            sys.exit(1)

    print('Copying', args.src, '→', args.dst)
    shutil.copytree(args.src, args.dst)
    print('Copy finished.')

if __name__ == '__main__':
    main()
