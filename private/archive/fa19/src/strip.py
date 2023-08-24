import json
import os

import re
has_todos = re.compile(r'(\[PP)|([Tt][Oo][Dd][Oo])')

def strip_answers(infile, outfile):
    with open(infile) as fd:
        data = json.load(fd)
    n_strip = 0
    strip_ct = 0
    for k, cell in enumerate(data['cells']):
        if cell['cell_type'] == 'code':
            for i in range(len(cell['source'])):
                if 'your code here' in cell['source'][i].lower():
                    n_strip += len(cell['source']) - i
                    strip_ct += 1
                    cell['source'] = cell['source'][:i+1]
                    break
                if 'your alternate code here' in cell['source'][i].lower():
                    data['cells'][k] = None
                    break
            if 'no_strip' not in cell['metadata']:
                cell['outputs'] = []
        elif cell['cell_type']=='markdown':
            for i in range(len(cell['source'])):
                if '*your answer here*' in cell['source'][i].lower():
                    n_strip += len(cell['source']) - i
                    strip_ct += 1
                    cell['source'] = cell['source'][:i+1]
                    break
                if '*rubric*' in cell['source'][i].lower():
                    data['cells'][k] = None
                    break
        else:
            continue

    data['cells'] = [e for e in data['cells'] if e is not None]

    for k, cell in enumerate(data['cells']):
        if has_todos.search('\n'.join(cell['source'])):
            print(f"Warning: TODO in cell {k}")


    if outfile is None:
        outfile = infile.replace('_solutions.ipynb', '.ipynb')
        if infile == outfile:
            outfile = infile.replace('.ipynb', '_stripped.ipynb')
    assert infile != outfile
    print(f"{infile}: Strip {strip_ct} cells, {n_strip} lines -> {outfile}")
    with open(outfile, 'w') as fd:
        json.dump(data, fd, indent=2)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('infile')
    parser.add_argument('outfile', nargs="?", default=None)
    opts = parser.parse_args()
    strip_answers(opts.infile, opts.outfile)
