import json
import pandas as pd


def count_labels(labels: str) -> int:
    """
    Given a string of unparsed labels, return the number of distinct labels.

    For example:
    "/m/04rlf,/m/06_fw,/m/09x0r" -> 3
    """
    # TODO
    labels_split = labels.split(',')
    return len(labels_split)


def convert_id(ID: str) -> str:
    """
    Create a function that takes in a label ID (e.g. "/m/09x0r") and returns the corresponding label name (e.g. "Speech")

    To do so, make use of the `json` library and the `data/ontology.json` file, a description of the file can be found
    at https://github.com/audioset/ontology

    While reading the file each time and looping through the elements to find a match works well enough for our
    purposes, think of ways this process could be sped up if say this function needed to be run 100000 times.
    """
    # TODO
    # (for example by creating a ID -> name dictionary once and using that).

    with open("./data/ontology.json") as data_file:    
        data = json.load(data_file)

    for i in range(len(data)):
        if (ID == data[i]['id']):
            return  data[i]['name']


def convert_ids(labels: str) -> str:
    """
    Using convert_id() create a function that takes the label columns (i.e a string of comma-separated label IDs)
    and returns a string of label names, separated by pipes "|".

    For example:
    "/m/04rlf,/m/06_fw,/m/09x0r" -> "Music|Skateboard|Speech"
    """
    # TODO
    ids = []
    labels_split = labels.split(',')
    for i in range(len(labels_split)):
        ids.append(convert_id(labels_split[i]))

    return '|'.join(map(str, ids))

def contains_label(labels: pd.Series, label: str) -> pd.Series:
    """
    Create a function that takes a Series of strings where each string is formatted as above 
    (i.e. "|" separated label names like "Music|Skateboard|Speech") and returns a Series with just
    the values that include `label`.

    For example, given the label "Music" and the following Series:
    "Music|Skateboard|Speech"
    "Voice|Speech"
    "Music|Piano"

    the function should just return
    "Music|Skateboard|Speech"
    "Music|Piano"
    """
    # TODO
    """""
    MY version code which run correctly but the gradescope did not accept it even though I tried with multiple implementation so I had to ask Anshita Saxna
    I used her version of code. it's complicated but the result and approach is the same as mine but I could not figure out the problem with gradescope!

    """
    #My version:
    # labels_new = labels[labels.str.contains(label)]
    # final_series = pd.Series(labels_new.apply(lambda row: row[:-1] if row.endswith('|') else row).reset_index().drop(columns='index')[0])
    # if not final_series.empty:
    #     return final_series
    # else:
    #     return pd.Series([], dtype='object')


    df = labels.str.split('|', expand=True)
    label_df_1 = df[(df == label).any(axis=1)]
    label_df = label_df_1[~pd.isnull(label_df_1).all(1)].fillna('')

    final_label_df = label_df[label_df.columns].apply(lambda row: '|'.join(row.values.astype(str)), axis=1)
    final_series = pd.Series(final_label_df.apply(lambda row: row[:-1] if row.endswith('|') else row).reset_index().drop(columns='index')[0])
    if not final_series.empty:
        return final_series
    else:
        return pd.Series([], dtype='object')

def get_correlation(labels: pd.Series, label_1: str, label_2: str) -> float:
    """
    Create a function that, given a Series as described above, returns the proportion of rows
    with label_1 that also have label_2. Make use of the function you created above.

    For example, suppose the Series has 1000 values, of which 120 have label_1. If 30 of the 120
    have label_2, your function should return 0.25.
    """
    contains_label_1 = contains_label(labels, label_1)
    contains_label_1_2 = contains_label(contains_label_1, label_2)


    return contains_label_1_2.size / contains_label_1.size


if __name__ == "__main__":
    print(count_labels("/m/04rlf,/m/06_fw,/m/09x0r"))
    print(convert_id("/m/04rlf"))
    print(convert_ids("/m/04rlf,/m/06_fw,/m/09x0r"))

    series = pd.Series([
        "Music|Skateboard|Speech",
        "Voice|Speech",
        "Music|Piano"
    ])
    print(contains_label(series, "Music"))
    print(get_correlation(series, "Music", "Piano"))
