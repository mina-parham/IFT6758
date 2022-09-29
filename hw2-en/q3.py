import re
import os
import pandas as pd
from tqdm import tqdm
from q2 import download_audio, cut_audio
from typing import List


def filter_df(csv_path: str, label: str) -> List[str]:
    """
    Write a function that takes the path to the processed csv from q1 (in the notebook) and returns a df of only the rows 
    that contain the human readable label passed as argument

    For example:
    get_ids("audio_segments_clean.csv", "Speech")
    """

    """
    again the same problem that happened with q1.py, the gradescope did not accept my solution so Anshita Saxna helped me with this part too!
    """
    # TODO
    df = pd.read_csv(csv_path)
    df['labels'] = df['label_names'].str.split('|')
    df = df[df['labels'].apply(lambda x: label in x)]
    df.drop(df.columns[[-1]], axis=1, inplace=True)
    return df

def data_pipeline(csv_path: str, label: str) -> None:
    """
    Using your previously created functions, write a function that takes a processed csv and for each video with the given label:
    (don't forget to create the associated label folder!). 
    1. Downloads it to <label>_raw/<ID>.mp3
    2. Cuts it to the appropriate segment
    3. Stores it in <label>_cut/<ID>.mp3

    It is recommended to iterate over the rows of filter_df().
    #Use tqdm to track the progress of the download process (https://tqdm.github.io/)

    #Unfortunately, it is possible that some of the videos cannot be downloaded. In such cases, your pipeline should handle the failure by going to the next video with the label.
    """
    # TODO
    df = filter_df(csv_path, label)
    if not os.path.exists(label+"_raw"):
        os.makedirs(label+"_raw")
    if not os.path.exists(label+"_cut"):
        os.makedirs(label+"_cut")
    with tqdm(len(df)) as bar:
        for index, row in df.iterrows():
            try:
                download_audio(row["# YTID"], label+"_raw/"+row['# YTID']+".mp3")
                bar.update(1)
                if os.path.exists(os.path.join(label+'_raw', row['# YTID']+'.mp3')):
                    cut_audio(label+'_raw/'+row['# YTID']+'.mp3',
                              label+'_cut/'+row['# YTID']+'.mp3',
                              row[' start_seconds'],
                              row[' end_seconds'])



            except KeyboardInterrupt:
                pass

    # for filename in os.listdir(label+"_raw"):
    #     prefix = re.findall(r'[^\/]+(?=\.)',filename);
    #     prefix = prefix[0]
    #     sub_df= df[df['# YTID']==prefix]
    #     start, end = sub_df.iloc[0][' start_seconds'], sub_df.iloc[0][' end_seconds']
    #     cut_audio(label+"_raw/"+filename, label+"_cut", start, end)



def rename_files(path_cut: str, csv_path: str) -> None:
    """
    Suppose we now want to rename the files we've downloaded in `path_cut` to include the start and end times as well as length of the segment. While
    this could have been done in the data_pipeline() function, suppose we forgot and don't want to download everything again.

    Write a function that, using regex (i.e. the `re` library), renames the existing files from "<ID>.mp3" -> "<ID>_<start_seconds_int>_<end_seconds_int>_<length_int>.mp3"
    in path_cut. csv_path is the path to the processed csv from q1. `path_cut` is a path to the folder with the cut audio.

    For example
    "--BfvyPmVMo.mp3" -> "--BfvyPmVMo_20_30_10.mp3"

    ## BE WARY: Assume that the YTID can contain special characters such as '.' or even '.mp3' ##
    """
    # TODO
    #mirim to in path
    #doone doone ID harkoodoom ro mikhoonim
    #too audio.csv donbale start o end o length migardim
    df = pd.read_csv(csv_path)
    for filename in os.listdir(path_cut):

        prefix = re.findall(r'[^\/]+(?=\.)',filename);
        prefix = prefix[0]
        sub_df= df[df['# YTID']==prefix]
        start, end = sub_df.iloc[0][' start_seconds'], sub_df.iloc[0][' end_seconds']
        duration = end - start
        os.rename(path_cut+"/"+filename, path_cut+"/"+prefix +"_"+str(int(start))+"_"+str(int(end))+"_"+str(int(duration))+".mp3")



if __name__ == "__main__":
    print(filter_df("audio_segments_clean.csv", "Laughter"))
    data_pipeline("audio_segments_clean.csv", "Laughter")
    rename_files("Laughter_cut", "audio_segments_clean.csv")
