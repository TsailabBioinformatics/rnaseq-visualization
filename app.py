import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import re


def separate_gene_ids(input_string):
    # Define the regular expression pattern to match potential separators
    # any non-alphanumeric characters (except underscore, dot, and hyphen)
    pattern = r"[^\w.-]+"

    # Split the input string based on the pattern
    gene_ids = re.split(pattern, input_string)

    # Remove empty gene IDs if any
    gene_ids = list(filter(None, gene_ids))

    return gene_ids


@st.cache_data
def load_data(csv_file_path, meta_file_path):
    tpm_df = pd.read_csv(csv_file_path, index_col=0)
    meta_df = pd.read_csv(meta_file_path)
    print(tpm_df.shape)
    return tpm_df, meta_df


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


csv_file_path = "data/tpm.csv"
meta_file_path = "data/meta.csv"
tpm_df, meta_df = load_data(csv_file_path, meta_file_path)

st.title("RNA-Seq viz Prototype")

with st.sidebar:
    add_radio = st.radio(
        "Gene selection",
        (
            "Single Gene ID",
            "Multiple Gene IDs",
            #  "Gene Name / keyord"
        ),
    )

    if add_radio == "Single Gene ID":
        gene_id = st.text_input("Gene ID", "PtXaTreH.10G046700")

    elif add_radio == "Multiple Gene IDs":
        gene_id = st.text_input(
            "Gene IDs", "PtXaTreH.10G046700,PtXaTreH.10G046800")
    else:
        gene_id = "PtXaTreH.10G046700"
    # gene_id_list = gene_id.split(",")
    gene_id_list = separate_gene_ids(gene_id)
    # elif add_radio == "Gene Name":
    #     "this function is not available yet" #TODO
    # gene_id = st.text_input("Gene IDs", "PtXaTreH.10G046700,PtXaTreH.10G046800")

    add_selectbox = st.selectbox(
        "Select a study type (not working yet)", ("drought",
                                                  "heat", "salt", "cold")
    )
    # add a free text input to select study type
    add_text = st.text_input("Study type (free text exploration)", "drought")
    selected_samples = meta_df.loc[meta_df["new_short_name"].str.contains(
        add_text)]

    # meta_df.loc[meta_df["new_short_name"].str.contains(add_text), ["new_short_name"]]


st.subheader("Genes selected")
st.write(f"{gene_id_list}")
f"number of genes selected: {len(gene_id_list)}"
# TODO more single gene info
st.divider()
st.subheader("Studies selected")
st.write(f"text input: {add_text}")
"number of samples in each study:"
st.write(selected_samples["study_id"].value_counts())

# TODO this many samples were selected, and user can finetune the samples they want
tab1, tab2 = st.tabs(["view individual study info",
                     "view individual sample info"])
with tab1:
    study_view_option = st.selectbox(
        "Choose a study to view",
        (selected_samples["study_id"].unique()),
    )
    st.write(selected_samples[selected_samples["study_id"]
             == study_view_option].set_index("new_short_name"))
selected_studies_ids = st.multiselect(
    "select studies", selected_samples["study_id"].unique()
)
selected_samples_list = selected_samples.loc[
    selected_samples["study_id"].isin(selected_studies_ids)
]["new_short_name"].tolist()


st.divider()
st.subheader("Expression pattern visualization")

if len(gene_id_list) > 1:
    available_visualizations = ["heatmap", "line chart"]
else:
    available_visualizations = ["line chart", "bar chart"]
visualiztion_options = st.multiselect(
    "available visualizations", available_visualizations, ["line chart"]
)
selected_df = tpm_df.loc[gene_id_list, selected_samples_list]

if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(selected_df)
    csv = convert_df(selected_df)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f"{add_text}_tpm.csv",
        mime="text/csv",
    )

if "line chart" in visualiztion_options:
    st.line_chart(data=selected_df.transpose())
if "bar chart" in visualiztion_options:
    st.bar_chart(selected_df.transpose())
if "heatmap" in visualiztion_options:
    with st.echo():
        import seaborn as sns
        # Generate the clustermap
        clustermap = sns.clustermap(selected_df, cmap='coolwarm', robust=True)

        # Adjust the position of the colorbar
        clustermap.ax_heatmap.collections[0].colorbar.set_label("TPM")

    st.pyplot(clustermap)
