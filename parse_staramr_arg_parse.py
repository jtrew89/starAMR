#!/usr/bin/env python

##Import libraries
import pandas as pd
import os
import argparse

##Create arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', dest='in_filename', help='name of input file, including extension', required=True)
parser.add_argument('-d', '--working_directory', dest='directory', help='directory input file(s) are kept in', required=True)
parser.add_argument('-o', '--output', dest='out_filename', help='name of output file, including extension', required=True)
parser.add_argument('-od', '--output_directory', dest='out_directory', help='specify directory for output file if different')

args = parser.parse_args()
##variables and datasets that will be used in script
os.chdir(args.directory)
raw_df = pd.read_table(args.in_filename)
isolates = list(set(sorted(raw_df['Isolate ID'])))
plasmids = list(set(sorted(raw_df['Plasmid'])))

##create new df
final_df = pd.DataFrame(columns=plasmids,
                        index=isolates)
final_df.columns.name=None
final_df.index.name=None

##format raw_df for next steps
raw_df.set_index("Isolate ID",inplace=True)

##loop through dataset and add a 1 to isolates that had the corrosponding
## plasmid present (isolates that only had one plasmid did not work
##with the dataframe variable, so had to make an empty list variable for those)
for index, row in final_df.iterrows():
    plasmid_df = pd.DataFrame()
    plasmid_lst = []
    if str(type(raw_df.loc[index])) == "<class 'pandas.core.frame.DataFrame'>":
        plasmid_df['plas']=raw_df.loc[index]['Plasmid']
        for a in plasmid_df['plas']:
            final_df.at[index, a] = 1
    else:
        plasmid_lst.append(raw_df.loc[index]['Plasmid'])
        for a in plasmid_lst:
            final_df.at[index, a] = 1

final_df.fillna(0,inplace=True)

if args.out_directory:
	os.chdir(args.out_directory)
	final_df.to_csv(args.out_filename, index=True)
else:
	final_df.to_csv(args.out_filename, index=True)
