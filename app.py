from flask import Flask, jsonify, request, make_response, render_template
import pandas as pd
import os
import ProcessingDataset as pds

app = Flask(__name__)

picFolder = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = picFolder
productPics = [os.path.join(app.config['UPLOAD_FOLDER'], 'Butterfly_Cooker.jpeg'),
               os.path.join(app.config['UPLOAD_FOLDER'], 'Butterfly_Kettle.jpeg'),
               os.path.join(app.config['UPLOAD_FOLDER'], 'ButterFly_Mixer.jpeg'),
               os.path.join(app.config['UPLOAD_FOLDER'], 'Butterfly_Stove.jpeg'),
               os.path.join(app.config['UPLOAD_FOLDER'], 'RapidJarJuicerMixerGrinderReviews.jpeg'),
               os.path.join(app.config['UPLOAD_FOLDER'], 'TawaReview.jpeg'),
               os.path.join(app.config['UPLOAD_FOLDER'], 'combineProducts.png'),
               os.path.join(app.config['UPLOAD_FOLDER'], 'github.jpg'),
               os.path.join(app.config['UPLOAD_FOLDER'], 'home.png')]


# ----------------------------  Reading CSV Files ----------------------------------
Butterfly_Cooker = pd.read_csv("ProductsDatasetFile/Butterfly_Cooker.csv")
Butterfly_Kettle = pd.read_csv('ProductsDatasetFile/Butterfly_Kettle.csv')
ButterFly_Mixer = pd.read_csv('ProductsDatasetFile/ButterFly_Mixer.csv')
Butterfly_Stove = pd.read_csv('ProductsDatasetFile/Butterfly_Stove.csv')
RapidJarJuicerMixerGrinderReviews = pd.read_csv(
    'ProductsDatasetFile/RapidJarJuicerMixerGrinderReviews.csv')
TawaReview = pd.read_csv('ProductsDatasetFile/TawaReview.csv')

# ----------------------------  Home Page ----------------------------------


def combiningAllProduct():
    allReviews = pd.DataFrame(columns=Butterfly_Cooker.iloc[:, 6:].columns)

    allReviews['DateOfReview'] = Butterfly_Cooker['DateOfReview']
    allReviews.iloc[0:, 0:-1] = Butterfly_Cooker.iloc[:, 6:]

    length = len(allReviews)
    allReviews = allReviews.append(Butterfly_Stove.iloc[:, 6:])
    allReviews.iloc[length:, -1] = Butterfly_Stove['DateOfReview']

    length = len(allReviews)
    allReviews = allReviews.append(RapidJarJuicerMixerGrinderReviews.iloc[:, 6:])
    allReviews.iloc[length:, -1] = RapidJarJuicerMixerGrinderReviews['DateOfReview']

    length = len(allReviews)
    allReviews = allReviews.append(ButterFly_Mixer.iloc[:, 6:])
    allReviews.iloc[length:, -1] = ButterFly_Mixer['DateOfReview']

    length = len(allReviews)
    allReviews = allReviews.append(Butterfly_Kettle.iloc[:, 6:])
    allReviews.iloc[length:, -1] = Butterfly_Kettle['DateOfReview']

    length = len(allReviews)
    allReviews = allReviews.append(TawaReview.iloc[:, 6:])
    allReviews.iloc[length:, -1] = TawaReview['DateOfReview']

    allReviews.set_index('DateOfReview', inplace=True)
    allReviews.index = pd.to_datetime(allReviews.index)
    allReviews[['FinalTextSentimentNegative', 'FinalTextSentimentPositive',
                'FinalTextSentimentNeutral', 'FinalTextSentimentCompound',
                'UserReviewSentimentNegative', 'UserReviewSentimentNegative',
                'UserReviewSentimentPositive', 'UserReviewSentimentNeutral',
                'UserReviewSentimentCompound']] = allReviews[['FinalTextSentimentNegative',
                                                              'FinalTextSentimentPositive',
                                                              'FinalTextSentimentNeutral',
                                                              'FinalTextSentimentCompound',
                                                              'UserReviewSentimentNegative',
                                                              'UserReviewSentimentNegative',
                                                              'UserReviewSentimentPositive',
                                                              'UserReviewSentimentNeutral',
                                                              'UserReviewSentimentCompound']].astype(float)
    allReviews['DateOfReview'] = allReviews.index
    allReviews.reset_index(inplace=True, drop=True)
    return allReviews

# ----------------------------  Home Page ----------------------------------
@app.route("/")
def homePage():
    return render_template('index.html', productPics=productPics)


# ----------------------------  Product conclusion ----------------------------------
@app.route("/conclusion", methods=['GET', 'POST'])
def conclusion():
    selection = int(request.args.get('type'))
    productName = ''

    if(selection == 0):
        productName = 'Butterfly Cooker'
        graphData = pds.graph_analysis(Butterfly_Cooker)
    elif(selection == 1):
        productName = 'Butterfly Kettle'
        graphData = pds.graph_analysis(Butterfly_Kettle)
    elif(selection == 2):
        productName = 'ButterFly Mixer'
        graphData = pds.graph_analysis(ButterFly_Mixer)
    elif(selection == 3):
        productName = 'Butterfly Stove'
        graphData = pds.graph_analysis(Butterfly_Stove)
    elif(selection == 4):
        productName = 'Butterfly RapidJar Juicer Mixer Grinder'
        graphData = pds.graph_analysis(RapidJarJuicerMixerGrinderReviews)
    elif(selection == 5):
        productName = 'Butterfly Tawa'
        graphData = pds.graph_analysis(TawaReview)
    elif(selection == 6):
        productName = 'Combine all product '
        graphData = pds.graph_analysis(combiningAllProduct())
    return render_template('conclusion.html', data=graphData, productPics=productPics, imgVal=selection, productName=productName)


if __name__ == '__main__':
    app.run(debug=True)
