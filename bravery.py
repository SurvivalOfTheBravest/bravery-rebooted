# A *rule* is a function that takes as input the comment that we're looking at,
# and returns one of the following:
# * Nothing (i.e., no return statement, or simply "return") - do nothing
# * A string - reply to the comment with that string
# * A Post object - make a top-level post somewhere
# * A tuple (string, otherComment) - reply to the otherComment with that string
#   (this is used to reply to a comment other than the one we're looking at)

def rules(): # Define rules here.


  def sarahJessicaParker(comment):
    if "sarah jessica parker" in comment.body.lower() and len(comment.body) < 40:
      return "http://i.imgur.com/0KZK3.gif"


  def breadsticks(comment):
    lc = comment.body.lower()
    if ("olive garden" in lc or "breadsticks" in lc) and "r/unlimitedbreadsticks" not in lc:
      return "/r/unlimitedbreadsticks"


  def igtmsft(comment):
    if "r/imgoingtohellforthis" in comment.body.lower():
      return "[/r/imgoingtomiddleschoolforthis](/r/igtmsft)"

  
  # If someone makes a one-word reply saying "religion" to an askreddit post,
  # commend them for their bravery, or post it to /r/magicskyfairy.
  def religion(comment):
    if str(comment.subreddit) in ["AskReddit","test"] and "religion" in comment.body.lower() and len(comment.body) < 10 and comment.parent_id[:2]=="t3":
      if True: # random.randint(0,1): #wait till the bot gets going before doing this
        return random.choice([
          "I tip my fedora to you, good sir",
          "In this moment, I am euphoric. Not because of any phony god's blessing, but because, I am enlightened by /u/"+str(comment.author)+"'s intelligence.",
          "Literally so brave",
          "My fedora is literally throbbing with euphoria.",
          ">Religion\n\n~Neil deGrasse Tyson",
          ">Religion\n\n~Carl Sagan",
          "+/u/fedoratips 1 TIPS verify"
        ])
      else:
        msfTitle = random.choice([
          "/u/"+str(comment.submission.author)+"asks \""+comment.submission.title+"\" I think we all know the answer",
          "The fedoras are out in full force tonight",
          comment.submission.title + " - Is that even a question?",
          "Keeping the default bravery alive",
          "Someone get this brave gentlesir a Mountain Dew",
          "Quotemaker of the year: /u/"+str(comment.author),
          "Bravery sighting in /r/askreddit"
        ])
        msfUrl = string.replace(comment.permalink, "www.reddit.com", "np.reddit.com")
        return Post(
          title = msfTitle,
          isSelf = False,
          content = msfUrl,
          subreddit = "magicskyfairy"
        )


  def instructionsUnclear(comment):
    lc = comment.body.lower()
    if "step 1" in lc and "step 2" in lc:
      longestWord = max(re.findall(r"[\w']+|[.,!?;]", comment.body),key=len)
      return "Instructions unclear, dick stuck in "+longestWord


  def alot(comment):
    #Posts an alot if someone misuses "a lot"
    lowercaseComment = comment.body.lower()
    if " alot " in lowercaseComment:
      alot_List = [
        "http://4.bp.blogspot.com/_D_Z-D2tzi14/S8TRIo4br3I/AAAAAAAACv4/Zh7_GcMlRKo/s400/ALOT.png" ,
        "http://4.bp.blogspot.com/_D_Z-D2tzi14/S8TfVzrqKDI/AAAAAAAACw4/AaBFBmKK3SA/s320/ALOT5.png" ,
        "http://www.mentalfloss.com/sites/default/legacy/blogs/wp-content/uploads/2011/02/550_alotAlix.jpg" ,
        "http://cdn0.dailydot.com/cache/51/95/51950010b596348543008ad9019a2ae6.jpg",
        "http://i.imgur.com/azxmg.png",
        "http://i.imgur.com/3uwHa.jpg"
      ]
      return "[alot](" + random.choice(alot_List) + ")"


  def hodor(comment):
    #if str(comment.subreddit) == "books": return None
    lc = comment.body.lower()
    #We don't need this, because we don't track those subreddits.
    #subreddit = str(comment.subreddit)
    #if subreddit == "gameofthrones" or subreddit == "asoiaf": return None
    triggerList = ["joffrey","lannister","game of thrones","a song of ice and fire","jon snow" ]
    hodorList = ["Hodor?", "hodor.", "HODOR!!!" ,"hodor?!"]
    for trigger in triggerList:
      if trigger in lc:
        return(random.choice(hodorList),comment)


  def riskyClickVideo(comment):
    if "://www.liveleak.com/" in comment.body:
      responses = [
        "risky click of the day",
        "Risky click.",
        "That link's staying blue, mate."
      ]
      return random.choice(responses)

  def trollhunter(comment):
    lc = comment.body.lower()
    if random.randint(0,4) == 1 and " troll " in lc:
      return "[i was only pretending](http://i.imgur.com/aaODnol.jpg)"


  def bjCopyPaste(comment):
    if str(comment.subreddit) == "Braveryjerk":
      global bjClipboard
      if random.randint(0,5)==1:
        if bjClipboard == "":
          #Get a new copypaste.
          bjClipboard = comment.body
          print "Copied Braveryjerk comment for later use"
          return
        else:
          #Release the copypaste.
          response = bjClipboard
          bjClipboard = ""
          return response

  # Detect if someone appears to be losing an argument,
  # and get ourselves on the winning side.
  def winningArgument(comment):
    lc = comment.body.lower()
    if len(lc)>50 and ("ad hominem" in lc or "i never said" in lc or "what makes you think" in lc or "personal attack" in lc):
      try: #Get the parent comment.
        threadID = comment.submission.id
        parent = r.get_submission("http://www.reddit.com/r/all/comments/"+threadID+"/_/"+comment.parent_id[3:]).comments[0]
      except Exception, ex:
        print "winningArgument could not get parent:", ex
        return
      if parent.score > 2: #If the parent is upvoted,
        try: #Get the grandparent comment.
          grandparent = r.get_submission("http://www.reddit.com/r/all/comments/"+threadID+"/_/"+parent.parent_id[3:]).comments[0]
        except Exception, ex:
          print "winningArgument could not get grandparent:", ex
          return
        #If the grandparent has been downvoted and is by the same person,
        if grandparent.score < 0 and comment.author == grandparent.author:
          if random.randint(0,2) == 0: #Reply to the comment with disagreement
            if "ad hominem" in lc:
              responses = [
                ">ad hominem\n\nI don't think that means what you think it means.",
                "A simple expression of disagreement doesn't count as *ad hominem*.",
                "I think that /u/"+str(parent.author)+" makes a valid point. Why do you think it's an *ad hominem*?",
              ]
            else:
              responses = [
                "someone sounds butthurt",
                "the butthurt store called, they're running out of /u/"+str(comment.author),
                "Why are you even arguing about this?",
                "http://xkcd.com/386/",
                "The fact that people still think like this makes me sad.",
                "Dude, seriously. Give it a rest."
              ]
            return random.choice(responses)
          else: #Or, reply to the parent with agreement.
            responses = [
              "I can't believe that anyone would be so naive as to disagree with this.",
              "Haters gonna hate. Don't waste your time arguing with trolls.",
              "Yours is a much needed voice of reason.",
              "I wish more people were as reasonable as you.",
              "Thank you for bringing some sanity to this discussion."
            ]
            return (random.choice(responses), parent)

  # /u/wsgy111
  def circumcision(comment):
    if random.randint(0,1) and "circumcis" in comment.body.lower():
      return "Circumcision is genital mutilation, pure and simple. My penis was mangled when I was young because of some stupid fucking religious custom, and the entire practice should be outlawed."
  

  # /u/hansjens47
  def edgy(comment):
    if "2edgy4me" in comment.body.lower():
      return "69edgy420me"


  # /u/Coman_Dante
  def braveryTrain(comment):
    if "karma train" in comment.body.lower():
      return "[Did somebody say karma train?](http://i.imgur.com/hlMv1.jpg)"


  # /u/xvvhiteboy
  def bullshitCopypasta(comment):
    if "This is bullshit - you're oversimplifying a complex situation to the point of no longer adding anything to the discussion." in comment.body:
      return """I am aware this is "copypasta", but I'm going to explain why it isn't relevant in this case. You people seem to think "copypastas" are funny by definition if they're relevant, and you post them even if they're not, hoping others upvote them on sight.

Let me tell you that's not how it works. For instance, the fact that you decided to use that copypasta in this situation indicates that you think:

a) the situation was complex

b) it has been oversimplified

c) it adds nothing to the conversation.

Well, you see, complexity is subjective, that's the nature of emergence. What's complex for a child like you is often trivial or routine for a scientist like me. Reddit's userbase is quite diverse, although there seems to be evidence of an over-representation of individuals exhibiting childish behaviors.

Secondly, do you really think this situation has been has been oversimplified? It's through using "copypastas" and other hasty generalizations you try to cram each individual scenario with its particularities into a formulaic mold. I hypothesize you require this simplification because of the state of your mental faculties and reasoning skills.

And lastly, most of the time your simplifications do not aid in understanding new facets of the subject matter. Characterizations that might not be 100% accurate can act as useful models for understanding overarching facets of complex inter-dependent systems, but your "copypastas" do not facilitate in that endeavor.

If even one of these criticisms is valid, your point is moot as it depends unilaterally on all the three premises I've highlighted. The social commentary you wish "copypastas" to exhibit might seem sensible, maybe even profound to you, but they're just as bad, if not worse than the additions reactiongifs, pun chains or novelty accounts bring to the table. Please consider this seriously, and don't immediately fall back on your preconceived notions without reexamining their validity, at least in a cursory manner after I've presented you with this new evidence you really should take seriously."""


  # /u/xvvhiteboy
  def bitcoinMagic(comment):
    if not random.randint(0,3) and "bitcoin" in comment.body.lower():
      return random.choice([
        "I don't feel comfortable investing in a currency where the price drops when a Magic The Gathering website has technical issues",
        "Anything that has dropped 650 dollars in 1 second is not an investment I am willing to risk making."
      ])

  # /u/xvvhiteboy
  def ragingClue(comment):
    if "raging clue" in comment.body.lower():
      return "I'm about to spray clue glue everywhere, let's follow your clue."

  # /u/xvvhiteboy
  def shivakamini(comment):
    if "shiva" in comment.body.lower():
      return "SHIVAKAMINI SOMAKANDARKRAM!!!"

  # /u/xvvhiteboy
  def maggianos(comment):
    if "Maggiano's" in comment.body:
      return "Recently I went on a date with my GF to Maggianos for lunch. We sat down and a couple minutes later a waiter noticed we hadnt had our drink orders taken. He alerted our waiter and our waiter gave him the table and he took our drink orders. The manager came over to us after we ordered drinks and apologized profusely. I explained we hadnt even noticed any wait and that there was no problem. We finished our meal and must have racked up a 40-60 bill and at the end the waiter said that our entire meal was on the house. Needless to say I didn't think that was necessary but they insisted. So I left all the money I had in my wallet as a tip which was around $25(I had planned to pay with a card) I honestly wish I could have tipped more and plan to go back and do so this week."


  # Return all the rules we've just defined
  return locals()



######### MAGIC STARTS HERE #########


# Configuration variables:


# Which subreddits should we check?
SUBREDDITS = [
  "test",
  #"bjbs",
  "Braveryjerk",
  "circlejerk",
  "pics",
  "funny",
  "gaming",
  "AskReddit",
  "videos",
  "IAmA",
  "todayilearned",
  "aww",
  "AdviceAnimals",
  "gifs",
  "wtf"
]

# How many seconds should we wait between cycles?
CYCLE_TIME = 90

# The following karma score is considered neutral.
# Comments that score less than this will lead to throttling. 
NEUTRAL_KARMA = 1

# How much will we react to upvotes/downvotes?
# Multiply the throttling factor by this if we get upvotes, or divide if we get downvotes.
THROTTLING_SENSITIVITY = 1.1

# Time (in seconds) to wait before checking the karma of a comment.
MATURITY_AGE = 86400

# These users may be harassed more than once by the bot.
HARASSMENT_EXEMPTIONS = [
  "SOTB-human"
]

# These rules are exempt from the no-harassment metarule.
HARASSMENT_EXEMPT_RULES = [
  "bjCopyPaste"
]



import time, random, string, re, praw
from collections import deque
bjClipboard = ""

# Set up reddit connection
from secrets import USERNAME, PASSWORD
r = praw.Reddit(user_agent="Bravery bot 4.0 by /u/"+USERNAME)
r.login(username=USERNAME, password=PASSWORD)

# Class for making top-level posts
class Post:
  def __init__(self, title, isSelf, content, subreddit):
    self.title = title
    self.isSelf = isSelf
    self.content = content
    self.subreddit = subreddit
  def submit(self):
    return r.submit(subreddit, title, text = (content if isSelf else None), url = (None if isSelf else content))

# "Compile" the rules
rulesList = rules()

# Set up database
import sqlite3
dbConnection = sqlite3.connect("database.db")
dbCursor = dbConnection.cursor()
dbCursor.execute("""CREATE TABLE IF NOT EXISTS history (
  id INTEGER PRIMARY KEY,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  submission_id VARCHAR(12) NOT NULL,
  comment_id VARCHAR(12) DEFAULT NULL,
  rule_name VARCHAR(100) NOT NULL,
  replyee VARCHAR(24) NOT NULL,
  upvotes INTEGER DEFAULT NULL,
  downvotes INTEGER DEFAULT NULL,
  karma INTEGER DEFAULT NULL
);""")
dbCursor.execute("""CREATE TABLE IF NOT EXISTS rules (
  name VARCHAR(100) NOT NULL PRIMARY KEY,
  throttling_factor DECIMAL(10,9) DEFAULT 1.0
);""")
dbConnection.commit()
dbCursor.execute("""CREATE TABLE IF NOT EXISTS placeholder (
  ph VARCHAR(12) DEFAULT NULL
);""")
dbConnection.commit()
dbCursor.execute("SELECT COUNT(1) FROM placeholder;")
result = dbCursor.fetchone()[0]
if result == 0:
  dbCursor.execute("INSERT INTO placeholder VALUES (NULL)")
  dbConnection.commit()

for ruleName in rulesList:
  dbCursor.execute("SELECT COUNT(1) FROM rules WHERE name='"+ruleName+"';")
  result = dbCursor.fetchone()[0]
  if result == 0:
    print "Adding rule to database:", ruleName
    dbCursor.execute("INSERT INTO rules VALUES ('"+ruleName+"', 1.0);")
    dbConnection.commit()


# Helper functions

def haveWeRepliedTo(username):
  dbCursor.execute("SELECT COUNT(1) FROM history WHERE replyee='"+username+"';")
  result = dbCursor.fetchone()[0]
  if result == 0:
    return False
  else:
    return True

def writeToHistory(thing, ruleName, replyee):
  thingType = type(thing).__name__
  if thingType == "Comment":
    dbCursor.execute("INSERT INTO history (     submission_id,      comment_id,rule_name,replyee) VALUES ('"+
                                   string.join([thing.submission.id,thing.id,  ruleName, replyee],"','") + "');")
  elif thingType == "Submission":
    dbCursor.execute("INSERT INTO history (     submission_id,rule_name,replyee) VALUES ('"+
                                   string.join([thing.id,     ruleName, replyee],"','") + "');")
  else:
    print "Unknown thing type:", thingType
    return
  dbConnection.commit()

def recordKarma(id, upvotes, downvotes, karma):
  strupvotes = str(upvotes) if upvotes is not None else "NULL"
  strdownvotes = str(downvotes) if downvotes is not None else "NULL"
  dbCursor.execute("UPDATE history SET upvotes="+strupvotes+",downvotes="+strdownvotes+",karma="+str(karma)+" WHERE id="+str(id)+";")
  dbConnection.commit()

def throttlingFactorFor(ruleName):
  dbCursor.execute("SELECT throttling_factor FROM rules WHERE name='"+ruleName+"';")
  results = dbCursor.fetchall()
  if results:
    return results[0][0]
  else:
    return 1.0

def ruleAlreadyInvokedInThread(ruleName, submissionID):
  dbCursor.execute("SELECT COUNT(1) FROM history WHERE rule_name='"+ruleName+"' AND submission_id='"+submissionID+"';")
  result = dbCursor.fetchone()[0]
  if result > 0:
    return True
  else:
    return False



responseQueue = deque([])
sr = r.get_subreddit(string.join(SUBREDDITS,"+"))
while True:
  print "...starting loop"

  # Stage 1: Get new comments from reddit

  dbCursor.execute("SELECT ph FROM placeholder;")
  dbfo = dbCursor.fetchone()
  placeholder = dbfo[0] if dbfo else None

  try:
    commentsGen = sr.get_comments(place_holder=placeholder, limit = (1000 if placeholder else 0))
    comments = [x for x in commentsGen]
  except Exception, ex:
    print "Exception in getting comments:", ex
    time.sleep(CYCLE_TIME)
    continue

  if not comments:
    print "No comments. Waiting..."
    time.sleep(CYCLE_TIME)
    continue

  dbCursor.execute("UPDATE placeholder SET ph='"+comments[0].id+"';")
  dbConnection.commit()

  if not placeholder:
    print "No placeholder. Waiting..."
    time.sleep(CYCLE_TIME)
    continue

  comments = comments[:-1]
  print "got", len(comments), "comments."


  # Stage 2: Go through the rules, enqueuing responses if applicable
  for comment in comments:
    for ruleName in rulesList:
      if random.random() < throttlingFactorFor(ruleName):
        ruleFunction = rulesList[ruleName]
        result = ruleFunction(comment)
        if result:
          print "Hit!", ruleName
          if type(result).__name__ in ["str", "unicode"]:
            result = (result, comment)
          responseQueue.append((result, ruleName))

  nextResponseQueue = deque([])


  # Stage 3: Go through the queue, attempting to submit the responses.
  # Skip any entry that replies to ourself or to someone we've already replied to,
  # or where the rule has already been invoked in the same thread before.
  # If there's a temporary failure, defer to the next round.
  while len(responseQueue):
    queueEntry = responseQueue.popleft()
    response = queueEntry[0]
    ruleName = queueEntry[1]
    responseType = type(response).__name__
    if responseType == "tuple": #If we're submitting a comment
      replyee = str(response[1].author)
      if replyee == USERNAME or (replyee not in HARASSMENT_EXEMPTIONS and ruleName not in HARASSMENT_EXEMPT_RULES and haveWeRepliedTo(replyee)):
        print "not allowed to reply to", replyee
        continue
      elif ruleAlreadyInvokedInThread(ruleName, response[1].submission.id):
        print "rule already invoked in thread", response[1].permalink
        continue
      else:
        try:
          tron = type(response[1]).__name__
          if tron == "Comment":
            reply = response[1].reply(response[0])
          elif tron == "Submission":
            reply = response[1].add_comment(response[0])
          else:
            raise ("Unknown responsee type:"+tron)
          print "Successfully commented!", reply.permalink
          writeToHistory(reply, ruleName, replyee)
        except Exception, ex:
          print "Exception in replying:", ex
          # If the exception is non-fatal, add it to the nextResponseQueue.
          strex = str(ex)
          if "you are doing that too much" in strex:
            nextResponseQueue.append(queueEntry)
    elif responseType == "Post": #If we're submitting a post:
      try:
        post = response.submit()
        writeToHistory(post, ruleName, replyee)
      except Exception, ex:
        #TODO: refactor to avoid repetition
        # If the exception is non-fatal, add it to the nextResponseQueue.
        strex = str(ex)
        if "you are doing that too much" in strex:
          nextResponseQueue.append(queueEntry)
    else:
      print "Unknown response type:", responseType
  responseQueue = nextResponseQueue #Carry over deferred comments to the next round
  if len(responseQueue): print "Deferred comments:", len(responseQueue)


  # Stage 4: Find the karma value of things more than a certain age old,
  # write them into the database, and adjust the throttling factors accordingly.
  dbCursor.execute("SELECT id, submission_id, comment_id, rule_name FROM history WHERE karma IS NULL AND strftime('%s','now') - strftime('%s',timestamp) > "+str(MATURITY_AGE)+";")
  maturedThings = dbCursor.fetchall()
  for (id, submissionID, commentID, ruleName) in maturedThings:
    if commentID:
      url = "http://www.reddit.com/r/all/comments/"+submissionID+"/_/"+commentID
      try:
        commentTree = r.get_submission(url).comments
        if commentTree:
          comment = commentTree[0]
          karma = int(comment.score)
          upvotes = int(comment.ups)
          downvotes = int(comment.downs)
        else:
          print "Comment has been deleted:", url
          karma = 0
          upvotes = 0
          downvotes = 0
      except Exception, ex:
        print "Exception in getting comment. Assume neutral.", ex
        karma = NEUTRAL_KARMA
        upvotes = None
        downvotes = None
    else:
      url = "http://www.reddit.com/r/all/comments/"+submissionID+"/_/"
      try:
        submission = r.get_submission(url)
        karma = submission.score
        upvotes = submission.ups
        downvotes = submission.downs
      except Exception, ex:
        print "Exception in getting post. Assume neutral.", ex
        karma = NEUTRAL_KARMA
        upvotes = None
        downvotes = None
    print "Assessing karma:", karma, url
    recordKarma(id, upvotes, downvotes, karma)
    if karma > NEUTRAL_KARMA:
      dbCursor.execute("UPDATE rules SET throttling_factor = MIN(1.0, throttling_factor*"+str(THROTTLING_SENSITIVITY)+") WHERE name = '"+ruleName+"';")
      dbConnection.commit()
    elif karma < NEUTRAL_KARMA:
      dbCursor.execute("UPDATE rules SET throttling_factor = throttling_factor/"+str(THROTTLING_SENSITIVITY)+" WHERE name = '"+ruleName+"';")
      dbConnection.commit()
    else:
      pass # No adjustment


  # Stage 5: Wait.
  print "sleeping..."
  time.sleep(CYCLE_TIME)
