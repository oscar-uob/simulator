#!/usr/bin/env bash

./figure1.py report/figure1.pdf
./figure2.py report/figure2.pdf
./figure3.py report/figure2.pdf

cd report

pdflatex report.tex
