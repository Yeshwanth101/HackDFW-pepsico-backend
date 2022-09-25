from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
import uuid
import json
from random import randint
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/influencerCatalog'
app.debug = True
db = SQLAlchemy(app)

class influencers(db.Model):
    __tablename__ = 'influencers'
    uniqueName = db.Column(db.String(100), primary_key=True)
    media = db.Column(db.String(), nullable=False)
    engagementScore = db.Column(db.Float(), nullable=False, default=0)
    entryDate = db.Column(db.String(), nullable=False)
    budgetIdentifier = db.Column(db.String(), nullable=False)
    projectEarnings = db.Column(db.String(), nullable=False)
    likeCount = db.Column(db.Integer(), nullable=False, default=0)
    viewCount = db.Column(db.Integer(), nullable=False, default=0)
    shareCount = db.Column(db.Integer(), nullable=False, default=0)

    def __init__(self, uniqueName, media, engagementScore, entryDate, budgetIdentifier, projectEarnings,viewCount, likeCount, shareCount):
        self.uniqueName = uniqueName
        self.media = media
        self.engagementScore = engagementScore
        self.entryDate = entryDate
        self.budgetIdentifier = budgetIdentifier
        self.projectEarnings = projectEarnings
        self.viewCount = viewCount
        self.shareCount = shareCount
        self.likeCount = likeCount

    def get_projected_earnings(influencer_unique_identifier):
        return randint(200, 10000) / 10

    def get_engagement_score(influencer_unique_identifier):
        return randint(40, 50)/10

    def get_views(influencer_unique_identifier):
        return randint(500, 10000)

    def get_likes(influencer_unique_identifier):
        return randint(500, 5000)

    def get_shares(influencer_unique_identifier):
        return randint(100, 2500)


@app.route('/viewInfluencersPerBudget', methods=['GET'])
@cross_origin()
def getInfluencers():
    args = request.args
    requestedBudgetID = args.get("budgetID", type=str)
    allBudget = budget.query.all()
    requestedBudgetName = ""
    requestedBudgetAmount = ""
    for budgetInfo in allBudget:
        if budgetInfo.budgetIdentifier == requestedBudgetID:
            requestedBudgetName = budgetInfo.budgetName
            requestedBudgetAmount = budgetInfo.budgetAmount
            break
    allInfluencers = influencers.query.all()
    result = []
    i = 0
    for influencer in allInfluencers:
        if influencer.budgetIdentifier == requestedBudgetID:
            currInfluencer = {
                "budgetIdentifier": requestedBudgetID,
                "budgetName": requestedBudgetName,
                "budgetAmount": requestedBudgetAmount,
                "uniqueName" : influencer.uniqueName,
                "media" : influencer.media,
                "engagementScore" : influencer.engagementScore,
                "likeCount": influencer.likeCount,
                "shareCount": influencer.shareCount,
                "viewCount": influencer.viewCount,
                "entryDate" : influencer.entryDate
            }
            result.append(json.dumps(currInfluencer))
    return jsonify(result)

@app.route('/enrollInfluencers', methods = ['post'])
@cross_origin()
def putInfluencers():
    influencerData = request.get_json()
    start_date = datetime.datetime.now()
    influencer = influencers(
        uniqueName=influencerData['uniqueName'],
        media=influencerData['media'],
        engagementScore=influencers.get_engagement_score(influencerData['uniqueName']),
        entryDate=str(start_date),
        budgetIdentifier=influencerData['budgetIdentifier'],
        projectEarnings = influencers.get_projected_earnings(influencerData['uniqueName']),
        viewCount=influencers.get_views(influencerData['uniqueName']),
        likeCount=influencers.get_likes(influencerData['uniqueName']),
        shareCount=influencers.get_shares(influencerData['uniqueName'])
    )
    db.session.add(influencer)
    db.session.commit()
    return jsonify(influencerData)

@app.route("/deleteInfluencer", methods=['DELETE'])
@cross_origin()
def removeInfluencer():
    args = request.args
    uniqueName = args.get("uniqueName", type=str)
    removedName = influencers.query.get(uniqueName)
    db.session.delete(removedName)
    db.session.commit()
    result = {
        "Message": "Successfully deleted."
    }
    return json.dumps(result)

# @app.route("/deleteInfluencer", methods=['DELETE'])
# def removeInfluencer():
#     args = request.args
#     influencerID = args.get("influencerID", type=str)
#     influencer = influencers.query.get(influencerID)
#     db.session.delete(influencer)
#     db.session.commit()
#
#     return influencer

###########################################################################################################################################

class budget(db.Model):
    __tablename__ = 'budget'
    budgetIdentifier = db.Column(db.String(100), primary_key=True)
    budgetName = db.Column(db.String(), nullable=False)
    budgetAmount = db.Column(db.Integer(), nullable=False)
    budgetStart = db.Column(db.String(), nullable=False)
    budgetExpiry = db.Column(db.String(), nullable=False)
    targetLocation = db.Column(db.String(), nullable=False)
    state = db.Column(db.String(), nullable=False)

    def __init__(self, budgetIdentifier, budgetName, budgetAmount ,budgetStart, budgetExpiry, targetLocation, state):
        self.budgetIdentifier = budgetIdentifier
        self.budgetName = budgetName
        self.budgetAmount = budgetAmount
        self.budgetStart = budgetStart
        self.budgetExpiry = budgetExpiry
        self.targetLocation = targetLocation
        self.state = state

@app.route('/addBudget', methods = ['post'])
@cross_origin()
def putBudget():
    budgetData = request.get_json()
    start_date = datetime.datetime.now()
    end_date = start_date + datetime.timedelta(days=30)
    budgetObj = budget(budgetIdentifier=str(uuid.uuid4().hex), budgetName=budgetData['budgetName'], budgetAmount = budgetData['budgetAmount'],budgetStart=str(start_date), budgetExpiry=str(end_date), targetLocation=budgetData['targetLocation'], state=budgetData['state'])
    db.session.add(budgetObj)
    db.session.commit()
    return jsonify(budgetData)

@app.route('/getActiveBudgets', methods = ['GET'])
@cross_origin()
def getBudget():
    allBudget = budget.query.all()
    output = []
    for budgetInfo in allBudget:
        currbudget = {}
        if datetime.datetime.strptime(budgetInfo.budgetExpiry[:19], '%Y-%m-%d %H:%M:%S') > datetime.datetime.now():
            currbudget['budgetIdentifier'] = budgetInfo.budgetIdentifier
            currbudget['budgetName'] = budgetInfo.budgetName
            currbudget['budgetAmount'] = budgetInfo.budgetAmount
            currbudget['budgetStart'] = budgetInfo.budgetStart
            currbudget['budgetExpiry'] = budgetInfo.budgetExpiry
            currbudget['targetLocation'] = budgetInfo.targetLocation
            currbudget['state'] = budgetInfo.state
            output.append(currbudget)
    return jsonify(output)

@app.route("/deleteBudget", methods=['DELETE'])
@cross_origin()
def removeBudget():
    args = request.args
    requestedBudgetID = args.get("budgetID", type=str)
    removedBudget = budget.query.get(requestedBudgetID)
    print(removedBudget)
    db.session.delete(removedBudget)
    db.session.commit()
    result = {
        "Message" : "Successfully deleted."
    }
    return json.dumps(result)

if __name__ == '__main__':
    app.run(debug=True)


