import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics
import base64

def main():
    st.title("Estimating EPU for Canada")
    uploaded_file = st.file_uploader("Upload your csv file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df['scaled_count_fin'] = df['count_fin'] / df['total_fin'] # calculate scaled counts
        df['scaled_count_leader'] = df['count_leader'] / df['total_leader']
        df['scaled_count_mg'] = df['count_mg'] / df['total_mg']
        df['scaled_count_np'] = df['count_np'] / df['total_np']
        df['scaled_count_oc'] = df['count_oc'] / df['total_oc']
        df['scaled_count_va'] = df['count_va'] / df['total_va']
    
        df['normed_count_fin'] = df['scaled_count_fin'] / statistics.stdev(df['scaled_count_fin']) # calculate normalized counts for each newspaper
        df['normed_count_leader'] = df['scaled_count_leader'] / statistics.stdev(df['scaled_count_leader'])
        df['normed_count_mg'] = df['scaled_count_mg'] / statistics.stdev(df['scaled_count_mg'])
        df['normed_count_np'] = df['scaled_count_np'] / statistics.stdev(df['scaled_count_np'])
        df['normed_count_oc'] = df['scaled_count_oc'] / statistics.stdev(df['scaled_count_oc'])
        df['normed_count_va'] = df['scaled_count_va'] / statistics.stdev(df['scaled_count_va'])
    
        df['epu'] = np.mean(df.loc[: , 'normed_count_fin':'normed_count_va'], axis = 1) # calculate the row-wise means of the columns in this range
        df['normed_epu'] = 100 * df['epu'] / statistics.mean(df['epu'])
    
        fig = plt.figure(figsize = (9, 5))
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(df['date'], df['normed_epu'], color='r', linestyle='-')
        ax.set_xlabel('Date')
        ax.set_xticks(df['date'][::4])
        ax.set_xticklabels(df['date'][::4], rotation=60)
        ax.set_ylabel('EPU')
        ax.grid(False)
        st.pyplot(fig)
          
    
        if st.button("Download csv"): 
            csv = df.to_csv(index= False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="merged_df.csv">Download csv file</a>'
            st.markdown(href, unsafe_allow_html=True)
             
if __name__ == '__main__':
    main()


