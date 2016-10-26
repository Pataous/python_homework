class IntSet(object):
    """An IntSet is a set of integers
    The value is represented by a list of integers stored in self.vals
    Each integer in the list must occur in self.vals exactly once."""

    def __init__(self, list_of_ints):
        """Create a set of integers. A particular value can appear only once."""
        #self.vals = list(list_of_ints)

        self.vals=[]

        for i in range(len(list_of_ints)):
            if list_of_ints[i] not in self.vals:
                self.vals.append(list_of_ints[i])       
        

    def insert(self, x):
        """Inserts x into the list if it is an integer that is not already present in the list"""
        
        if type(x) != int:
            raise TypeError("The element is not an integer")

        if x not in self.vals:
            self.vals.append(x)

        else:
            print "Element not added because it was already present in the list"
        

    def member(self, x):
        """Assumes x is an integer
           Returns True if x is in self.vals, and False otherwise"""
        return x in self.vals

    def __str__(self):
        """Returns a string representation of self"""
        self.vals.sort()
        return '{' + ','.join([str(x) for x in self.vals]) + '}'

    def intersect(self,other_IntSec):
        '''Returns the overlap bewteen self and "other_IntSec". If there is no overlap, returns an empty list.'''
        overlap = IntSet([])
        overlap.vals = [x for x in self.vals if x in other_IntSec.vals]
        return overlap

    def __len__(self):
        '''Modifies the len method so that it returns the number of elements in self.vals'''
        return len(self.vals)



#Test_IntSet = IntSet([1,3,3,3,4,5,6,4,2])
#Test_IntSet2 = IntSet([9,9,9])


#print Test_IntSet.intersect(Test_IntSet2).vals
#print len(Test_IntSet2)

#Test_IntSet2.insert(9)