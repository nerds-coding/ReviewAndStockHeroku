import pandas as pd
from sklearn.preprocessing import MinMaxScaler

data = pd.read_csv('ProductsDatasetFile/Butterfly_Cooker.csv')


def graph_analysis(data):
    # ------------------------------ Processing Share Market Dataset ----------------------------------------------------------
    bseData = pd.read_csv("ProductsDatasetFile/BSE Data - Sheet1.csv")
    nseData = pd.read_csv("ProductsDatasetFile/NSE Data - Sheet1.csv")

    bseData.dropna(inplace=True)
    nseData.dropna(inplace=True)

    bseData['ClosePrice'] = MinMaxScaler().fit_transform(bseData['Close'].values.reshape(-1, 1))
    nseData['ClosePrice'] = MinMaxScaler().fit_transform(nseData['Close'].values.reshape(-1, 1))
    minMax = MinMaxScaler()
    bseData['Date'] = pd.to_datetime(bseData['Date'])
    nseData['Date'] = pd.to_datetime(bseData['Date'])

    bseData.sort_values('Date', inplace=True)
    nseData.sort_values('Date', inplace=True)

    bseData.rename(columns={"- SPREAD -": "SpreadHighLow",
                            "Unnamed: 7": 'SpreadOpenClose', 'Date': 'DateOfReview'}, inplace=True)
    nseData.rename(columns={"- SPREAD -": "SpreadHighLow",
                            "Unnamed: 7": 'SpreadOpenClose', 'Date': 'DateOfReview'}, inplace=True)

    # ------------------------------ Processing Product Dataset ----------------------------------------------------------
    EachDayReview = pd.DataFrame(columns=['FinalTextSentimentNegative', 'FinalTextSentimentPositive',
                                          'FinalTextSentimentNeutral', 'FinalTextSentimentCompound',
                                          'UserReviewSentimentNegative', 'UserReviewSentimentNegative',
                                          'UserReviewSentimentPositive', 'UserReviewSentimentNeutral',
                                          'UserReviewSentimentCompound'])

    EachDayReview[['FinalTextSentimentNegative', 'FinalTextSentimentPositive',
                   'FinalTextSentimentNeutral', 'FinalTextSentimentCompound',
                   'UserReviewSentimentNegative', 'UserReviewSentimentNegative',
                   'UserReviewSentimentPositive', 'UserReviewSentimentNeutral',
                   'UserReviewSentimentCompound']] = data[['FinalTextSentimentNegative', 'FinalTextSentimentPositive',
                                                           'FinalTextSentimentNeutral', 'FinalTextSentimentCompound',
                                                           'UserReviewSentimentNegative', 'UserReviewSentimentNegative',
                                                           'UserReviewSentimentPositive', 'UserReviewSentimentNeutral',
                                                           'UserReviewSentimentCompound']].astype(float)

    EachDayReview.index = pd.to_datetime(data['DateOfReview'])
    EachDayReview = EachDayReview.resample('D').mean().ffill()
    EachDayReview['FinalTextSentiment'] = ['pos' if x > 0.5 else 'neu' if ((x < 0.4) & (
        x > 0.1)) else 'neg' for x in EachDayReview['FinalTextSentimentCompound']]
    EachDayReview['UserReviewLabel'] = ['pos' if x > 0.5 else 'neu' if ((x < 0.4) & (
        x > 0.1)) else 'neg' for x in EachDayReview['UserReviewSentimentCompound']]
    EachDayReview['DateOfReview'] = EachDayReview.index
    EachDayReview.reset_index(inplace=True, drop=True)

    # ------------------------------ Merging Bse dataset with Product Dataset and also for NSE ----------------------------------------------------------
    bseDataAndAllReview = pd.merge(bseData, EachDayReview, on='DateOfReview')
    nseDataAndAllReview = pd.merge(nseData, EachDayReview, on='DateOfReview')

    # ------------------------------ Preparing for "Sentiment over time and Donught Chart Dictionary" for Conclusion.html ----------------------------------------------------------
    pos = EachDayReview[EachDayReview['FinalTextSentiment'] == 'pos']
    pos = list(zip(list(pos['FinalTextSentimentCompound'].values),
                   list(pos['DateOfReview'].values)))

    neg = EachDayReview[EachDayReview['FinalTextSentiment'] == 'neg']
    neg = list(zip(list(neg['FinalTextSentimentCompound'].values),
                   list(neg['DateOfReview'].values)))

    neu = EachDayReview[EachDayReview['FinalTextSentiment'] == 'neu']
    neu = list(zip(list(neu['FinalTextSentimentCompound'].values),
                   list(neu['DateOfReview'].values)))

    # ------------------------------ Variable for Conclusion.html----------------------------------------------------------
    values = {'sentiment': {'pos': pos,
                            'neg': neg,
                            'neu': neu},

              'DateOfReview': list(data['DateOfReview'].values[0:]),

              'BseData': list(zip(list(bseData['DateOfReview'].values), list(bseData['High'].values), list(
                  bseData['Low'].values), list(bseData['Open'].values), list(bseData['Close'].values))),

              'NseData': list(zip(list(nseData['DateOfReview'].values), list(nseData['High'].values), list(
                  nseData['Low'].values), list(bseData['Open'].values), list(nseData['Close'].values))),

              'bseAndReview': list(zip(list(bseDataAndAllReview['DateOfReview'].values), list(bseDataAndAllReview['ClosePrice'].values), list(bseDataAndAllReview['FinalTextSentimentCompound'].values))),

              'nseAndReview': list(zip(list(nseDataAndAllReview['DateOfReview'].values), list(nseDataAndAllReview['ClosePrice'].values), list(nseDataAndAllReview['FinalTextSentimentCompound'].values)))
              }

    return values


# graph_analysis(data)
