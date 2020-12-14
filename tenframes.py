#!/usr/bin/env python3

import os
import subprocess
import tempfile
import random
import math

tex_doc_header = """
\\documentclass[24pt]{article}
\\usepackage{geometry}
\\geometry{a4paper, margin=10mm}
\\usepackage{subcaption}
\\usepackage{tikz}

\\pagestyle{empty}

\\begin{document}
"""

subfigure_template = """
\\begin{{subfigure}}{{.5\\textwidth}}
    \\centering{{
        \\resizebox{{.95\\textwidth}}{{!}}{{\\input{{{TENFRAME_TEX}}}}}
    }}
\\end{{subfigure}}"""

tex_doc_footer = '''
\\end{document}
'''


def generate_ten_frame(count):
    circle = '\\draw[fill=black]({X},{Y}) circle (0.4cm);'
    commands = ['\\begin{tikzpicture}', '\\draw[step=1cm,black,very thick] (0,0) grid (5,2);']
    i = 0
    while i < count:
        x = math.floor(i / 2) + 0.5
        y = i % 2 + 0.5
        commands.append(circle.format(X=x, Y=y))
        i += 1
    commands.append('\\end{tikzpicture}')

    return '\n'.join(commands)


def main():
    with tempfile.TemporaryDirectory() as d:
        tex_main = os.path.join(d, 'tenframe-main.tex')
        with open(tex_main, 'w') as f:
            f.write(tex_doc_header)

            page = 0
            while page < 10:
                frames = list(range(11))
                random.shuffle(frames)
                frames.pop()

                f.write('\section*{\\Huge{Ten} \\Huge\\textbf{Frames}}\n\\begin{figure*}[h!]\n')

                count = 0
                for frame in frames:
                    frame_name = 'tenframe%02d-%02d.tex' % (page, count)
                    frame_path = os.path.join(d, frame_name)
                    with open(frame_path, 'w') as g:
                        g.write(generate_ten_frame(frame))
                    if count % 2 == 0:
                        f.write('\\vspace*{10mm}\n')
                    f.write(f'% FRAME: {frame_name}\n')
                    f.write(subfigure_template.format(TENFRAME_TEX=frame_path).strip())
                    if count % 2 == 0:
                        f.write('%\n')
                    else:
                        f.write('\n\n')
                    count += 1

                f.write('\\end{figure*}\n')
                f.write('\\pagebreak\n')
                page += 1
            f.write(tex_doc_footer)
        with open(tex_main) as f:
            print(f.read())

        subprocess.call(['pdflatex', tex_main])


if __name__ == '__main__':
    main()
