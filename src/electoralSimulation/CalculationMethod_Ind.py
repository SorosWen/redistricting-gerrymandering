# Created this file as a seperate package for a difference project. 

'''
Input: 
    votes: a list of strings, where each element is a name. 
Output: 
    the winner name. 
Exception: 
    If there is a tie. 
'''
def FPTP(votes=[]):
    if votes == None or len(votes) == 0:
        raise Exception("Votes cannot be empty.")
    result = {}
    for candidate in votes:
        if candidate in result.keys():
            result[candidate] += 1
        else:
            result[candidate] = 1
    
    winner = max(result, key=result.get)
    # if there is a tie then raise exception. 
    winnerVotes = votes 


# votes: a list of lists. 
# example: [[Red, Blue, Green], [Green, Red], [Red, Green, Brown], [Brown, Red]]
def RCV(votes=None):
    if votes == None or len(votes) == 0:
        raise Exception("Input votes are empty.")
    eliminatedCandidate = set()

    while(True):
        result = {}
        for ballot in votes:
            if ballot != None and len(ballot) != 0 :
                for candidate in ballot:
                    if candidate in eliminatedCandidate:
                        continue
                    else:
                        if candidate not in result:
                            result[candidate] = 1
                        else:
                            result[candidate] += 1
                        break
        # return if only one candidate standing. 
        if len(result.keys()) == 1:
            return list(result.keys())[0]
        # return if a candidate exceed majority. 
        for candidate in result.keys():
            if 1.0 * result[candidate] / sum(result.values()) > 0.5:
                return candidate

        partyWithLeastVote = min(result, key=result.get)
        eliminatedCandidate.add(partyWithLeastVote)

print(FPTP(['red', 'brown', 'yellow', 'blue', 'red']))