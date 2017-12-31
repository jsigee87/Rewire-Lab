import numpy as np
import random as rm
import pandas as pd

#####################################################################
#                        To use this class
#
# 1.) Create a sequence object with desired length. 
#     note-initial state defaults to 0
#
# 2.) Use helper functions to access sequence details:
#       getSequence() prints the sequence
#       getCounts() prints the number of occurences of each state
#       getTransitions() prints the number of transitions from the
#       the different states as follows: a transition from i to j is
#       tallied in the ith row and jth column.
#
####################################################################

class sequence():
    # the constructor will build the entire sequence desired and assign 
    # it to self.sequence. (the constructor does all the work)
    def __init__(self, desired_length, num_states=4, probabilistic=True, initial=0):
                        
        # desired length must (if you want something correct) be of 
        # form 12k + 1, where k is an int
        self.desired_length = desired_length
        
        # this is the number of 'blocks' that need to be made
        valid_transitions = int((desired_length - 1)/12)
        
        # the number of states to be used. if != 4, the rest of the class
        # should be checked for functionality
        self.num_states = num_states
        
        # defines the main sequence to be built, will be of length
        # 'desired_length'
        self.sequence = []        
                
        # initialize the adj matrix. the ijth entry is the number of possible
        # transitions from i to j
        self.adj_matrix = np.zeros((self.num_states,self.num_states))
                
        assert(probabilistic == True),"Attempting to use deprecated functionality.\nAborting program.\n"
        
        # for loop builds a block on each iteration, and adds it to seq
        for i in range(valid_transitions):
            # define a new block for the block builder
            block = []
            
            # build another sequence of length 12 and add it to the total seq
            self.sequence.extend(self.__makeBlockProbabilistic(initial, block))
            
            # reset the adj matrix for the next block
            self.adj_matrix = np.zeros((self.num_states,self.num_states))   

            
    # this function finds the next state by attempting to greedily choose
    # in order to keep the number of transitions 'even'.
    def __findNextProbabilistic(self, current):  
        #max is updated as we search for the next state with the max number
        # of zero entries in its AM row
        maximum = -1
        for j in range(self.num_states):
            if current != j:
                # if this transition has not yet occured this cycle
                if self.adj_matrix[current][j] == 0:
                    # see how many null transitions the candidate next state has
                    count = np.sum(1-self.adj_matrix[j][:])
                    if  count > maximum:
                        #reset the next_candidate list
                        next_candidate = []
                        next_candidate.append(j)
                        maximum = count
                        next = j
                    elif count == maximum:
                        next_candidate.append(j)
        
        # this randomly chooses an entry of the next_candidate array
        if len(next_candidate) == 1:
            return int(next_candidate[0])
        else:
            pick = rm.randint(0,len(next_candidate) - 1)
            next = next_candidate[pick]
            return int(next)
    '''
    # note to self--- check total string length, and accounting of previous states for transition matrix
    '''
    def __makeBlockProbabilistic(self, state, block):
        block.append(state)
    
        # if not first element in sequence, mark the transition, 
        # and track sum of each row (transitions)
        if len(self.sequence) != 1:
            prev = block[len(block)-2]
            self.adj_matrix[prev][state] += 1
            #prev = self.sequence[len(self.sequence) - 2]    #this should be the value of prev state
            #self.adj_matrix[prev][state] += 1       #we increment to mark that this transition has occured
       
        next_state = self.__findNextProbabilistic(state)
    
        # if we reached our desired length, append the next state and return
        if(len(block) == 12):
            #prev = self.sequence[len(self.sequence) - 1]
            #self.adj_matrix[prev][next_state] += 1
            #return self.sequence.append(next_state)
            return block
    
        #else keep building
        return self.__makeBlockProbabilistic(next_state, block)
    
    ####################################################################
    # Use these to print sequence, counts, transitions
    ####################################################################
     
    def getSequence(self):
        print('The generated sequence for this instance is: /n{}'
              .format(self.sequence))
        
    def getCounts(self):
        unique, counts = np.unique(self.sequence, return_counts=True)
        print('The occurences for each state are as follows: \n{}'.
              format(dict(zip(unique, counts))))
        print('Making the total sequence length {}'
              .format(len(self.sequence)))
           
    def getTransitions(self):
        transitions = np.zeros((4,4))
        
        for i in range(self.desired_length -2):
            transitions[self.sequence[i]][self.sequence[i+1]] +=1
    
        df = pd.DataFrame(transitions)
        print('The number of transitions are in this matrix A, where ')
        print('A(i,j) denotes transitions from i to j: \n\n{}'.format(df))
