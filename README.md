# rnaseq-visualization

Using Streamlit to create a web app for visualizing RNA-seq data.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/TsailabBioinformatics/rnaseq-visualization.git
cd rnaseq-visualization
```

### 2. Create Conda environment and install the dependencies

```bash
conda env create -f environment.yml
conda activate rnaseq-visualization
```

### 3. Prepare the data

You can download the RNA-seq data, e.g. bioPoplar from OneDrive and put it in the `data` folder. Change the name into `tpm.csv` and `meta.csv`.

### 4. Run the app

```bash
streamlit run app.py
```




