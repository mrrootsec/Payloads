#!/usr/bin/env python3

import re
import sys
import os
import argparse

def grep_file(pattern, file_path, show_line_numbers=False, invert=False, color=False):
    matches = []
    regex = re.compile(pattern)
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for lineno, line in enumerate(f, 1):
                match = regex.search(line)
                matched = bool(match)
                if matched != invert:
                    if color and matched:
                        line = regex.sub(lambda m: f'\033[91m{m.group(0)}\033[0m', line.rstrip('\n'))
                    else:
                        line = line.rstrip('\n')
                    if show_line_numbers:
                        matches.append(f'{file_path}:{lineno}:{line}')
                    else:
                        matches.append(f'{file_path}:{line}')
    except FileNotFoundError:
        print(f"File not found: {file_path}", file=sys.stderr)
    return matches

def grep_dir(pattern, dir_path, show_line_numbers, invert, color):
    results = []
    for root, _, files in os.walk(dir_path):
        for name in files:
            file_path = os.path.join(root, name)
            results.extend(grep_file(pattern, file_path, show_line_numbers, invert, color))
    return results

def main():
    parser = argparse.ArgumentParser(description='Enhanced Python grep clone')
    parser.add_argument('pattern', help='Regex pattern')
    parser.add_argument('path', nargs='?', default='-', help='File or directory (use - for stdin)')
    parser.add_argument('-n', action='store_true', help='Show line numbers')
    parser.add_argument('-v', action='store_true', help='Invert match')
    parser.add_argument('-r', '--recursive', action='store_true', help='Recursive search (for directories)')
    parser.add_argument('--color', action='store_true', help='Highlight matches')
    args = parser.parse_args()

    if args.path == '-':
        lines = sys.stdin.readlines()
        regex = re.compile(args.pattern)
        for lineno, line in enumerate(lines, 1):
            match = regex.search(line)
            matched = bool(match)
            if matched != args.v:
                if args.color and matched:
                    line = regex.sub(lambda m: f'\033[91m{m.group(0)}\033[0m', line.rstrip('\n'))
                else:
                    line = line.rstrip('\n')
                if args.n:
                    print(f'{lineno}:{line}')
                else:
                    print(line)
    elif os.path.isdir(args.path):
        if not args.recursive:
            print(f"{args.path} is a directory. Use -r for recursive search.", file=sys.stderr)
            sys.exit(1)
        results = grep_dir(args.pattern, args.path, args.n, args.v, args.color)
        for line in results:
            print(line)
    else:
        results = grep_file(args.pattern, args.path, args.n, args.v, args.color)
        for line in results:
            print(line)

if __name__ == '__main__':
    main()
