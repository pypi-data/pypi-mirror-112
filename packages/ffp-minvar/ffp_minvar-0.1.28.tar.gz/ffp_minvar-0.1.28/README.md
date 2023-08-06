FFP_MINVAR
===
# Table of Contents
- [Installation](Installation)
- [Documentation](Documentation)
- [Github Description](#Github-Description)
- [GSL Download](#GSL-Download)
  - [OSX](#osx)
  - [Ubuntu](#ubuntu)
- [Compilation and Test](#Compilation)
  - [Compile .so file](#Shared)
  - [Test in python](#PythonTest)
  - [Test in c](#CTest)


# Installation
To install ***ffp_minvar***, use this command in terminal:
```bash
pip3 install ffp_minvar
```
We assume you are using python >= 3.6

# Documentation
To use the library, import the module like following:
```bash
from ffp_minvar import ffp_minvar_lib
```

Function Description
- <dt id="ffp_minvar_lib.ffp">
  <code class="sig-prename descclassname">ffp_minvar_lib.</code><code class="sig-name descname">ffp</code><span class="sig-paren">(</span><em class="sig-param">theta</em>, <em class="sig-param">B</em>, <em class="sig-param">V</em>, <em class="sig-param">Delta</em>)</span>
  </dt>

  - <span style="background-color:grey">theta</span>: A K-1 array of [np.zeros(K)](https://numpy.org/doc/stable/reference/generated/numpy.zeros.html) 
  - <span style="background-color:grey">B</span>: An N-K [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html)
  - <span style="background-color:grey">V</span>: A K-K diagonal matrix as [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html). Note that V must be passed in as a diagonal matrix otherwise a *ValueError* will be raised. 
  - <span style="background-color:grey">Delta</span>: An N-1 [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html). Contains the diagonal entries of the actual N-N matrix D.

- <dt id="ffp_minvar_lib.lo_minvar">
  <code class="sig-prename descclassname">ffp_minvar_lib.</code><code class="sig-name descname">lo_minvar</code><span class="sig-paren">(<em class="sig-param">B</em>, <em class="sig-param">V</em>, <em class="sig-param">Delta</em>)</span>
  </dt>

  - <span style="background-color:grey">B</span>: An N-K [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html)
  - <span style="background-color:grey">V</span>: A K-K diagonal matrix as [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html). Note that V must be passed in as a diagonal matrix otherwise a *ValueError* will be raised. 
  - <span style="background-color:grey">Delta</span>: An N-1 [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html). Contains the diagonal entries of the actual N-N matrix D.

- <dt id="ffp_minvar_lib.psi">
  <code class="sig-prename descclassname">ffp_minvar_lib.</code><code class="sig-name descname">psi</code><span class="sig-paren">(<em class="sig-param">B</em>, <em class="sig-param">V</em>, <em class="sig-param">Delta</em>)</span>
  </dt>

  - <span style="background-color:grey">B</span>: An N-K [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html)
  - <span style="background-color:grey">V</span>: A K-K diagonal matrix as [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html). Note that V must be passed in as a diagonal matrix otherwise a *ValueError* will be raised. 
  - <span style="background-color:grey">Delta</span>: An N-1 [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html). Contains the diagonal entries of the actual N-N matrix D.

Examples:
```bash
#------------ ffp Test --------------#
print("------------ ffp Test ------------")
ffp_res = ffp_minvar_lib.ffp(theta, B, V, D)  
print(ffp_res)

#------------ Psi Test --------------#
print("------------ Psi Test ------------")
psi_res = ffp_minvar_lib.psi(B, V, D)  
print(psi_res)

#---------- lo_minvar Test ----------#
print("------------ lo_minvar Test ------------")
lo_minvar_res = ffp_minvar_lib.lo_minvar(B, V, D)
print(lo_minvar_res)
```
  

# Github Description
`lib` folder stores the source python library. 

`lib/shared` folder stores the .so file used by the python library.

`include` folder contains the header file of the algorithm.

`src` folder contains the C file of the algorithm, which uses the GSL library from GNU. 

`obj` folder stores the object file of the compiled C file of the algorithm.

`test` folder contains tests in C of the functions of the algorithm.

`ffp_minvar.py` is the original version of the algorithm.

`test_lib.py` is the test file of the python package.



# GSL Download
Note that this part is irrelevant to the installation of ***ffp_minvar*** package and is only for the download of GSL library. 
## OSX

Apparently GSL can be installed through [Homebrew](https://brew.sh/) via 
```bash
brew install gsl
```
though installing it manually is just as simple, which we now describe.

- Download [gsl-latest.tar.gz](ftp://ftp.gnu.org/gnu/gsl/gsl-latest.tar.gz) from the [GSL ftp site](ftp://ftp.gnu.org/gnu/gsl/) and unzip it anywhere (e.g. /Downloads)
- Open the unzipped `gsl` folder in Terminal (e.g. `cd ~/Downloads/gsl-2.4`
- Run `sudo ./configure && make && make install`

If the above gives a "permission denied" error, instead try
```bash
sudo make clean
sudo chown -R $USER .
./configure && make
make install
```

## Ubuntu

```bash
sudo apt-get install libgsl-dev
```
You'll now be able to include GSL into your code from anywhere.


# Compilation

## Shared
To compile the .so file of the algorithm used by the python package, use this command under root folder. 
```bash
make alg_lomv.so
```
## PythonTest
To run the test of the python package:
1. Compile the .so file
2. Make sure that your current python interpreter has installed `numpy`, `ctypes`, `pdb`, and `pathlib`.
3. Use this command under root folder:
    ```bash
    python test_lib.py
    ```

## CTest
To compile the test of the algorithm in c, use this command under root folder:
```bash
make test_alg
./test_alg
```