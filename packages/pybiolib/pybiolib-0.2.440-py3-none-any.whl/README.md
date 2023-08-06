# PyBioLib

PyBioLib is a Python package for running BioLib applications from Python scripts, and the command line.

### Python Example
```python
# pip3 install pybiolib
import biolib
samtools = biolib.load('samtools/samtools')
print(samtools(args=['--help']))
```

### Command Line Example
```bash
pip3 install pybiolib
biolib run samtools/samtools --help
```
