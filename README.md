# Binder_Design_Pipline
 Binder_Design_Pipline for CS286

## Setup
1. Applied licence of pyRosseta
    The environment require PyRosetta which requires a license that
   is free to academics and available [here](https://graylab.jhu.edu/pyrosetta/downloads/documentation/PyRosetta_Install_Tutorial.pdf).
   This license will give you access to the USERNAME and PASSWORD
   referenced below. If you do not provide this USERNAME and PASSWORD,
   you will get a CondaHTTPError when you attempt to run the installation.

After getting license, modify your condarc:
 - Ensure that you have the PyRosetta channel included in your ~/.condarc
Your ~/.condarc should look something like this:
```
channels:
  - defaults
  - https://USER:PASSWORD@conda.graylab.jhu.edu
```
    

2. clone this repo and cd to it.
   ```
   git clone https://github.com/Masterchiefm/Binder_Design_CS286.git
   cd Binder_Design_CS286
   ```
3. Setup the enviroment.
   ```
   bash setup.py
   ```
   Just wait for about 30min, and the setup will be done!

## Binder design
   It's very easy to run the pipeline!

   1) Open the file "binder_design_mannually.py" and then modify the
   "Input Cell" according to your design.

   2) Save changes and run the py file in current directory, don't run it in 
      other directory. And you don't need to activate the conda, for
      the script will activate it automatically.
      ```
      python3 binder_design_mannually.py
      ```

   3) Wait for Results
   
### Optional
You can find a conda env created in your home directory, which is
named binder_design.

IF you want to use RFdiffusion and ProteinMPNN independently, you
can first activate the env by typing
```
conda activate binder_design
```
then navigate to the folder "env_config", the two project is already
there, and you can do binder design or something else mentioned in 
RFdiffusion.

Enjoy!