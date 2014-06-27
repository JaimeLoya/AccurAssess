import numpy as np
import csv, itertools,sys
from accassess import *

# This was copied from the AccAssess plugin by Jared Kibele
   
def error_matrix( reference, comparison, categories=None, unclassified=0 ):
    """
    Take a reference array and a comparison array and return an error matrix.
    
    >>> error_matrix(ref_array(),comp_array())
    Example: ErrorMatrix([[15,  0,  0,  0],
           [ 2,  9,  0,  0],
           [ 3,  0, 13,  0],
           [ 7,  0,  0, 20]])
    """
    idx = np.where( reference<>unclassified )
    all_classes = np.unique( np.vstack( (reference[idx],comparison[idx]) ) )
    
    n = len( all_classes )
    em = np.array([z.count(x) for z in [zip(comparison.flatten(),reference.flatten())] for x in itertools.product(all_classes,repeat=2)]).reshape(n,n).view( ErrorMatrix )
    if categories:
        em.categories = categories
    else:
        # need vstacked values so we can check both arrays
        em.categories = all_classes.tolist()
    return em
    

class ErrorMatrix( np.ndarray ):


    def save_csv( self, filepath,  rounding=None):
        
        with open(filepath, 'wb') as f:
            
            writer = csv.writer(f)
            # copy the array so we can annotate it without screwing it up
            arr = self.copy()
            # round if needed
            if rounding:
                arr = arr.round( rounding )
            # write the annotated error matrix
            writer.writerows( arr )
           

if __name__ == "__main__":
    import doctest
    doctest.testmod()
