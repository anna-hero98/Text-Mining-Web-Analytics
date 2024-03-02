import text_import_text
import access_dataframe
import SentimentAnalyse
from dataframe_storage import extracted_df

text_import_text.build_and_process_dataframe()
print('1')
access_dataframe.process_data()
print('2')
SentimentAnalyse.sentiment_analyse(extracted_df=extracted_df)
print('3')
