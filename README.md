# captcha-solve
Scripts to solve simple captchas. 

## Contents
* Some test images (`captcha.png`, `captcha-0.png`, ...)
* `captcha_solver.py` - a finalized module for solving captchas
* "Intermediate"-stage scripts:
  1. `color-chanel.py` splits images up into common color chanels
  1. `rescale-threshold.py` forces images to (at least) 300 DPI and applies a thresholding algorithm
  1. `filter.py` applies "expand" and "contract" filter (MinFilter / MaxFilter) to eliminate gaps
  1. `solve-captcha.py` solves a captcha from a hardcoded file path.
