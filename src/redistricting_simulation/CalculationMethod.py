# Input: 
#   candidatesResult: a dictionary. Keys = name of candiate, Value = Votes a candidate received. 
# Output: 
#   String: the name of candidate that win using FPTP
def FPTP(candidatesResult):
    memberWithMaxVote = max(candidatesResult, key=candidatesResult.get)
    return memberWithMaxVote

def RankChoiceVoting(agents):
    if agents == None or len(agents) == 0:
        raise Exception("Input agents are empty.")
    eliminatedParties = set()
    while(True):
        result = {}
        for agent in agents:
            if agent != None: 
                preference = agent.getChoices()
                for party in preference:
                    if party in eliminatedParties:
                        continue
                    else:
                        if party not in result:
                            result[party] = 1
                        else:
                            result[party] += 1
                        break
        # return if only one candidate standing. 
        if len(result.keys()) == 1:
            return list(result.keys())[0]
        # return if a candidate exceed majority. 
        for candidate in result.keys():
            if 1.0 * result[candidate] / sum(result.values()) > 0.5:
                return candidate

        partyWithLeastVote = min(result, key=result.get)
        eliminatedParties.add(partyWithLeastVote)

# Input:
#   partyListResult: a dictionarry. Keys = name of parties. Value = Votes a party received. 
#   totalSeats: int. The number of seats that need to be assigned. 
# Output:
#   Dictionary: Keys = party names. Values = seats assigned to that party. 
def LargestRemainder(partyListResult, seatsToBeAssigned):
    assignedSeats = {}
    # division
    normalizedPartyListResult = {}
    quota = 1.0 * sum(partyListResult.values()) / seatsToBeAssigned
    for color in partyListResult.keys():
        normalizedPartyListResult[color] = 1.0 * partyListResult[color] / quota
    # retrieve the integer part and decimal part. 
    intPart = {}
    decimalPart = {}
    for color in partyListResult.keys():
        intPart[color] = int(normalizedPartyListResult[color])
        decimalPart[color] = normalizedPartyListResult[color] - int(normalizedPartyListResult[color])

    # assign the integer component to assignedSeats. 
    for color in intPart.keys():
        if color not in assignedSeats.keys():
            assignedSeats[color] = intPart[color]
        else:
            assignedSeats[color] += intPart[color]
    # assign the decimal components. 
    remainingSeats = seatsToBeAssigned - sum(assignedSeats.values())
    for i in range(remainingSeats):
        colorWithMaxDecimal = max(decimalPart, key=decimalPart.get)
        if colorWithMaxDecimal not in assignedSeats.keys():
            assignedSeats[colorWithMaxDecimal] = 1
        else: 
            assignedSeats[colorWithMaxDecimal] += 1
        decimalPart.pop(colorWithMaxDecimal)
    return assignedSeats

# Input:
#   partyListResult: a dictionarry. Keys = name of parties. Value = Votes a party received. 
#   totalSeats: int. The total number of seats that sum(assignedSeats.values()) should become. 
#   assignedSeatsOrigin: dictionary. Keys = name of parties. Value = Seats a party already received. 
# Output:
#   Dictionary: Keys = party names. Values = seats assigned to that party in the end, including pre-assigned seats and seats post assignment. 
def HighestAverage(partyListResultOrigin, totalSeats, 
                    assignedSeatsOrigin = None, divisor = "D'Hondt", 
                    quota = "None", threshold = 1, allowOverhang=False, 
                    includeSeatsThatWereAssigned = False):

    partyListResult = partyListResultOrigin.copy()
    
    assignedSeats = {}
    if assignedSeatsOrigin != None:
        assignedSeats = assignedSeatsOrigin.copy()
    
    # initialize the dictionary
    for party in partyListResultOrigin.keys():
        if party not in assignedSeats.keys():
            assignedSeats[party] = 0
            
    # in several divisor methods, we need to assign party a seat base on the quota. 
    if divisor == 'Huntington–Hill' or divisor == "Adams":
        for party in partyListResultOrigin.keys():
            if assignedSeats[party] == 0:
                if quota == "None":
                    assignedSeats[party] += 1
                elif quota == "Hare":
                    if 1.0*sum(partyListResultOrigin.values())/totalSeats < partyListResult[party]:
                        assignedSeats[party] += 1
                    else:
                        partyListResult.pop(party)
                elif quota == "Droop":
                    if int(sum(partyListResultOrigin.values())/(totalSeats+1)) + 1 < partyListResult[party]:
                        assignedSeats[party] += 1
                    else:
                        partyListResult.pop(party)
                elif quota == "Imperiali":
                    if 1.0*sum(partyListResultOrigin.values())/(totalSeats+2) < partyListResult[party]:
                        assignedSeats[party] += 1
                    else:
                        partyListResult.pop(party)
                elif quota == "Threshold":
                    if partyListResultOrigin[party] > threshold:
                        assignedSeats[party] += 1
                    else:
                        partyListResult.pop(party)
                else:
                    raise Exception("Quota method " + quota + " is not implemented.")

    # throw error if overhang not allowed and sum of assigned seats exceeding parliament seat limit. 
    if not allowOverhang and sum(assignedSeats.values()) > totalSeats:
        raise Exception("Not enough seats in parliament for the given methods. To resolve this issue, change methods, increase seats in parliament, or allow overhang.")
    
    # assigning seats
    while sum(assignedSeats.values()) < totalSeats:
        divDict = {}
        for party in partyListResult.keys():
            if divisor == "D'Hondt":
                divDict[party] = 1.0 * partyListResult[party]/(1.0 + assignedSeats[party])
            elif divisor == "Webster":
                divDict[party] = 1.0 * partyListResult[party]/(0.5 + assignedSeats[party])
            elif divisor == "Imperiali":
                divDict[party] = 1.0 * partyListResult[party]/(2 + assignedSeats[party])
            elif divisor == "Huntington–Hill":
                divDict[party] = 1.0 * partyListResult[party]/((assignedSeats[party]*(assignedSeats[party] + 1))**0.5)
            elif divisor == "Danish":
                divDict[party] = 1.0 * partyListResult[party]/(1 + assignedSeats[party]*3)
            elif divisor == "Adams":
                divDict[party] = 1.0 * partyListResult[party]/assignedSeats[party]
            else:
                raise Exception("Divisor method " + divisor + " has not been implemented.")
        partyWithMaxNum = max(divDict, key=divDict.get)
        assignedSeats[partyWithMaxNum] += 1

    if not includeSeatsThatWereAssigned and assignedSeatsOrigin != None:
        for party in assignedSeatsOrigin.keys():
            assignedSeats[party] -= assignedSeatsOrigin[party]

    return assignedSeats