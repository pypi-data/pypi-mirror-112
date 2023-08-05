#!/usr/bin/python
# -*- coding: utf-8 -*-

# EnhaaancedLists - Copyright & Contact Notice
##############################################
# Created by Dominik Niedenzu                #      
# Copyright (C) 2021 Dominik Niedenzu        #       
#     All Rights Reserved                    #
#                                            #
#           Contact:                         #
#      pyadaaah@blackward.de                 #         
#      www.blackward.de                      #         
##############################################

# EnhaaancedLists - Version & Modification Notice
#################################################
# Based on EnhaaancedLists Version 0.70         #
# Modified by --- (date: ---)                   #
#################################################

# EnhaaancedLists - License
#######################################################################################################################
# Use and redistribution in source and binary forms, without or with modification,                                    #
# are permitted (free of charge) provided that the following conditions are met (including the disclaimer):           #
#                                                                                                                     #
# 1. Redistributions of source code must retain the above copyright & contact notice and                              #
#    this license text (including the permission notice, this list of conditions and the following disclaimer).       #
#                                                                                                                     #
#    a) If said source code is redistributed unmodified, the belonging file name must be enhaaancedLists.py and       #
#       said file must retain the above version & modification notice too.                                            #
#                                                                                                                     #
#    b) Whereas if said source code is redistributed modified (this includes redistributions of                       #
#       substantial portions of the source code), the belonging file name(s) must be enhaaancedLists_modified*.py     #
#       (where the asterisk stands for an arbitrary intermediate string) and said files                               #
#       must contain the above version & modification notice too - updated with the name(s) of the change             #
#       maker(s) as well as the date(s) of the modification(s).                                                       #
#                                                                                                                     #
# 2. Redistributions in binary form must reproduce the above copyright & contact notice and                           #
#    this license text (including the permission notice, this list of conditions and the following disclaimer).       #
#    They must also reproduce a version & modification notice similar to the one above - in the                       #
#    sense of 1. a) resp. b).                                                                                         #
#                                                                                                                     #
# 3. Neither the name "Dominik Niedenzu", nor the name resp. trademark "Blackward", nor the names of authors resp.    #
#    contributors resp. change makers may be used to endorse or promote products derived from this software without   #
#    specific prior written permission.                                                                               #
#                                                                                                                     #
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO   # 
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.                            #
#                                                                                                                     #
# IN NO EVENT SHALL DOMINIK NIEDENZU OR AUTHORS OR CONTRIBUTORS OR CHANGE MAKERS BE LIABLE FOR ANY CLAIM, ANY         # 
# (DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY OR CONSEQUENTIAL) DAMAGE OR ANY OTHER LIABILITY, WHETHER IN AN    #
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THIS SOFTWARE (OR PARTS OF THIS   #
# SOFTWARE) OR THE USE OR REDISTRIBUTION OR OTHER DEALINGS IN THIS SOFTWARE (OR PARTS OF THIS SOFTWARE).              #
#                                                                                                                     #
# THE USERS RESP. REDISTRIBUTORS OF THIS SOFTWARE (OR PARTS OF THIS SOFTWARE) ARE SOLELY RESPONSIBLE FOR ENSURING     #
# THAT AFOREMENTIONED CONDITIONS ALL ARE MET AND COMPLIANT WITH THE LAW IN THE RESPECTIVE JURISDICTION - BEFORE (!)   #
# THEY USE RESP. REDISTRIBUTE.                                                                                        #
#######################################################################################################################



#import (from) common libraries
from argparse         import ArgumentParser as Argparse_ArgumentParser
from sys              import version_info   as Sys_version_info
from functools        import partial        as Functools_partial
from operator         import attrgetter     as Operator_attrgetter
from operator         import itemgetter     as Operator_itemgetter
from sys              import stderr         as Sys_stderr
from os               import linesep        as Os_linesep


#python version 2 checker
def isPy2():
    """
         Returns True if Python version in use is < 3.0.
    """
    if    Sys_version_info.major < 3.0:
          return True
    else:
          return False
          
          
#python version 3 checker          
def isPy3():
    """
         Returns True if Python version in use is >= 3.0.
    """
    if    Sys_version_info.major >= 3.0:
          return True
    else:
          return False
          
          
### take differences between python2 and python3 into account ###        
if      isPy2() == True:
        ### python version < 3 ###
        #using the types library for checking for built-in types is (just) python 2(.7) style        
        from types            import FunctionType   as Types_FunctionType
        from types            import TupleType      as Types_TupleType
        from types            import NoneType       as Types_NoneType    
        from types            import StringTypes    as Types_StringTypes
        from types            import UnicodeType    as Types_UnicodeType
        
else:
        ### python version >= 3 ###
        def function(): 
            pass
        Types_FunctionType = (type(function), Functools_partial)
        Types_TupleType    = tuple
        Types_NoneType     = None
        Types_StringTypes  = str
        Types_UnicodeType  = str
        xrange = range


#############################
# supported operators tuple #
#############################
#TBD: add unary operators alike 'abs' too resp. check 'operators' library for more
operatorsT = ( 'lt', 'le', 'eq', 'ge', 'gt', 'ne', 'add', 'sub', 'mul', 'truediv', \
               'floordiv', 'mod', 'pow'                                            )
#'div' just exists in Python 2.*
if      isPy2() == True:
        operatorsT += ('div',)

for operatorS in operatorsT:
    exec("from operator import {0} as Operator_{0}".format(operatorS))        
               
           
#####################
# exception handler #  
#####################      
try:
        #if the pyadaaah library is available, use its exceptions / exception handler
        from pyadaaah import *
        
except: 
        #if the pyadaaah library is not available, use a dummy exception handler 
        #(but the 'logExceptions' decorator has a real meaning!)
        #STR - accepting (and translating) unicode characters too
        class STR(str):
            """
                 String class accepting e.g. and in particular unicodes as well; 
                 the result is a pure ascii (0-127) string, which is achieved by 
                 replacing all non-ascii characters by '?'.
            """
            
            #return the pure ascii string
            def __new__(cls, text):
                """ """   
                
                try:
                       #make a str out of text - if not already one (resp. an unicode)
                       if    isinstance(text, Types_StringTypes):
                             textS = text
                       else:
                             textS = str(text)
                      
                       #make a unicode out of textS - if not already one
                       if not isinstance(textS, Types_UnicodeType):
                          textS = textS.decode("ascii", "replace")
                
                       #unicode is str in python 3 - but not in python 2
                       #in python 2: encode back to str
                       if isPy2() == True:
                          #replace non-ascii characters by '?'
                          textS = textS.encode("ascii", "replace")
                          
                       #return
                       return textS
                      
                except BaseException as ee:
                       return "Error in STR: %s!" % str(ee)
                       
               
               
        #dummy exception handler
        class ExceptionHandler(object):
              """ Dummy exception handler doing nothing. """
                             
              @classmethod
              def log(cls, exception):
                  """ Does nothing. """
                  
                  pass
                  
  
    
        #exception logger - decorator for methods (only !)
        def logExceptions(method, logger=ExceptionHandler):
            """ Method wrapper for exception logging (decorator). """
        
            def decorator(self, *params, **paramDict):
                try:   
                        return method(self, *params, **paramDict)              
                        
                except  BaseException as error: 
                        #get class-s name - in a safe manner
                        clsNameS = "no class"
                        if hasattr(self, "__class__"):
                           if hasattr(self.__class__, "__name__"):
                              clsNameS = self.__class__.__name__
                        
                        #get method name - in a safe manner
                        methodNameS = "no method"
                        if hasattr(method, "__name__"):
                           methodNameS = method.__name__
                        
                        #create message - in a safe manner
                        try:
                                errMsgS = "Error in %s.%s: %s" % (clsNameS, methodNameS, STR(error))
                        except:
                                errMsgS = "automatic exception message creation failed"
                                
                        #enhance readability / beauty
                        errMsgS = errMsgS.rstrip() + Os_linesep + Os_linesep
                        
                        #log error message
                        logger.log( type(error)(errMsgS) )
                        
                        #re-raise exception
                        raise type(error)(errMsgS)
                        
            #return new (decorator) method
            return decorator
            
            
        #as the dummy logger does nothing, muting means 'doing nothing' too
        def muteLogging(method, logger=ExceptionHandler):
            """ Decorator - adding nothing to each method decorated. """
            
            def decorator(self, *params, **paramDict):
                """ This wrapper does not add any functionality. """
                
                #call method
                retVal = method(self, *params, **paramDict)
                
                #return return value of method
                return retVal
                
            #return new (decorator) method
            return decorator    



#EnhaaancedLists version
__version__ = 0.7
def getVersion():
    global __version__
    return __version__
    


##################################################
# elem term - condition (partial) function class #
############# ####################################
class ConditionFunction(Functools_partial):
      """
          This is the basic unit of condition terms using the 'elem' term.
          
          It is a function, whose operator methods have been overloaded to
          return another ConditionFunction instance, which has been extended
          by the belonging operations / comparisons.
          
          In particular, the operator methods for getting an attribute ('.') and
          for getting an item ('[]') have been overloaded this way, as well as 
          the comparison operator methods. 
          
          Furthermore the bitwise 'or' and 'and' operator methods are abused 
          to provide a logical 'or' and 'and' too.
          
          Further operators taken into account can be found in operatorsT.
          
          In short: this condition resp. function can be 'extended' by 
          using said operators on it - which then leads to an(other) 
          (extended) condition resp. function resp. ConditionFunction.
          
          Example:
          ex = (elem['a'] > 5) & (elem['b'] < 5)
          #creates a ConditionFunction taking one parameter, namely an element
          
          ex( {'a':6, 'b':4} ) ==> True
          ex( {'a':4, 'b':6} ) ==> False
          
          Note, that the 'elem' term mechanism is very limited yet; it just is
          a short convenience notation, which can be used to enhance the 
          readability of SIMPLE conditions for element selection - TBD.
          
          Some methods of EnhList accept ConditionFunction-s as parameter. For
          those, you either can use the ConditionFunction resp. 'term'
          mechanism, or a function, alike a lambda, returning a truth value.
      """
      
      
      #generate comparison methods __lt__ ... __ne__, 
      #called if "<" ... "!=" are used on a ConditionFunction instance
      for operatorS in operatorsT:
          exec( """@logExceptions
def __{0}__(self, ohs):
    ' overloaded comparison method '
    if    isinstance(ohs, Functools_partial):
          return ConditionFunction( lambda x: Operator_{0}(self(x), ohs(x)) )
    else:
          return ConditionFunction( lambda x: Operator_{0}(self(x), ohs) )
                """.format(operatorS))   
                
                
      #called if the 'bitwise and' operator '&' is used on a ConditionFunction instance
      @logExceptions
      def __and__(self, ohs):
          """ As there is no hook for the 'logical and' operator, 
              the 'bitwise and' is 'abused' instead.               """
      
          if    isinstance(ohs, Functools_partial):
                return ConditionFunction( lambda x: (self(x) and ohs(x)) )    
          else:
                return ConditionFunction( lambda x: (self(x) and ohs) )
          
          
      #called if the 'bitwise or' operator '|' is used on self
      @logExceptions
      def __or__(self, ohs):
          """ As there is no hook for the 'logical or' operator, 
              the 'bitwise or' is 'abused' instead.                """
       
          if    isinstance(ohs, Functools_partial):
                return ConditionFunction( lambda x: (self(x) or ohs(x)) ) 
          else:
                return ConditionFunction( lambda x: (self(x) or ohs) )
                
                
      #method called by ".nameS"
      @logExceptions
      def __getattribute__(self, nameS):
          """ overloaded get attribute method """
          
          #do not meddle with resp change the classes standard attributes (accesses)
          if    not nameS.startswith("__"): 
                return ConditionFunction( Operator_attrgetter(nameS) )
          else:
                return Functools_partial.__getattribute__(self, nameS)
          
          
      #method called by "[nameS]"
      @logExceptions
      def __getitem__(self, keyO):
          """ overloaded get item method """
          
          return ConditionFunction( Operator_itemgetter(keyO) )                
      
      
### short elem alias ###
elem = ConditionFunction(lambda x: x)


#self test method
def _testElem():
    """ Does some tests using the 'elem' notation. """
    
    print ( "Testing 'elem'..." )
    
    #lower than comparison operator
    fct = elem < 5
    assert fct(4) == True
    assert fct(6) == False  
    
    #lower or equal comparison operator
    fct = elem <= 5
    assert fct(5) == True
    assert fct(6) == False
    
    #equal comparison operator
    fct = elem == 5
    assert fct(5) == True
    assert fct(6) == False
    
    #greater or equal comparison operator
    fct = elem >= 5
    assert fct(6) == True
    assert fct(4) == False
    
    #greater comparison operator
    fct = elem > 5
    assert fct(6) == True
    assert fct(5) == False
    
    #not equal comparison operator
    fct = elem != 5
    assert fct(4) == True
    assert fct(5) == False
    
    #add operator
    fct = 1 < elem + 1
    assert fct(1) == True
    assert fct(0) == False
    
    #subtract operator
    fct = 1 < elem - 1
    assert fct(3) == True
    assert fct(2) == False
    
    #multiply operator
    fct = 1 < elem * 2
    assert fct(1) == True
    assert fct(0) == False
    
    #divide operator
    fct = 1 < elem / 2
    assert fct(4.0) == True
    assert fct(2.0) == False
    
    #int divide operator
    fct = elem // 2 >= 1
    assert fct(4) == True
    assert fct(1) == False
    
    #modulo operator
    fct = elem % 2 == elem % 4
    assert fct(4) == True
    assert fct(2) == False
    
    #power operator
    fct = elem ** 2 != 16
    assert fct(3) == True
    assert fct(4) == False

    print ("...'elem' tested successfully!")   



#single
class Single(object):
      """ 
          Just a helper class for EnhList.
          Some methods of EnhList accept that as a parameter.
      """
      pass
single = Single()

#several
class Several(object):
      """ 
          Just a helper class for EnhList.
          Some methods of EnhList accept that as a parameter.
      """
      pass
several = Several() 
      
      
    
#######################
# Enhanced List Class #
#######################
class EnhList(list):
      """ 
          List with extended / enhanced IN-PLACE capabilities.
          
          Together with the 'elem' term, some of its 
          methods (also) allow using a NEW OPERATOR NOTATION, closely 
          resembling mathematical conditions.
          
          Note that '&' and '|' are 'abused' as 'logical and / or' in this
          context (and NOT bitwise!).
          
          examples for said ADDITIONAL capabilities (standard list operations work too):
          
          
          #convert a parameter list to an enhanced list 
          eL = EnhList(1,3,5,7)                                       #eL: [1,3,5,7]
          
          #push single as well as multiple elements into the list
          eL.push(9)                                  ==> None        #eL: [1,3,5,7,9]
          eL.push(11,13,15)                           ==> None        #eL: [1,3,5,7,9,11,13,15]
          
          #pop - note that push/pop implements a FIFO - in contrast to the standard list
          eL.pop()                                    ==> 1           #eL: [3,5,7,9,11,13,15]
          eL.pop( (elem > 3) & (elem < 11), single )  ==> 5           #eL: [3,7,9,11,13,15]
          eL.pop( (elem > 3) & (elem < 11)         )  ==> [7,9]       #eL: [3,11,13,15]      
          
          #get items from list
          eL[ elem >= 10         ]                    ==> [11,13,15]  #eL: unchanged
          eL[ elem >= 10, single ]                    ==> 11          #eL: unchanged
          eL[ elem <  3,  single ]                    ==> None        #eL: unchanged
          
          #check whether list contains items
          ( elem <  3 ) in eL                         ==> False       #eL: unchanged
          ( elem >= 3 ) in eL                         ==> True        #eL: unchanged
          
          #delete items from list
          del eL[ elem < 12, single ]                 ==> ---         #eL: [11,13,15]
          del eL[ elem > 12         ]                 ==> ---         #eL: [11]
          
          eL = EnhList(1,3,5,7)                                       #eL: [1,3,5,7]
          #check whether all element meet a condition
          eL.areAll( elem % 2 == 1 )                  ==> True
          eL.areAll( elem     >= 3 )                  ==> False
          
          #map function on elements / work with items of elements
          eL.mapIf( lambda x: dict(a=x) )                          
                                                      ==> None        #eL: [{'a':1},{'a':3},{'a':5},{'a':7}]
          eL.mapIf( lambda x: x['a'] + 1, elem['a'] > 3)           
                                                      ==> None        #eL: [{'a':1},{'a':3},6,8]
          
          #work with attributes of elements
          class Attr(object):
                def __init__(self, value):
                    self.a = value
                def __repr__(self):
                    return ".a=%s" % self.a
          eL.mapIf( lambda x: Attr(x), lambda x: type(x) ==  int ) 
                                                      ==> None        #eL: [{'a':1},{'a':3},.a=6,.a=8]
                
          More examples can be found in the source code of the selftest function
          of the module and the methods called from there.
          
          Please also take the doc/help-texts of each revised method into account too.
          
          Also note, that 'elem' just is an alias defined as follows:
          
          elem = ConditionFunction(lambda x: x)
          
          So that more informations about 'elem' also can be found in the doc/help-text
          belonging to the class 'ConditionFunction', which, by the way, is inherited from
          functools.partial.
      """
      
      
      #initialisation
      @logExceptions
      def __init__(self, *params):
          """
               If several parameters 'params' are given, they are taken 
               as the initial elements of the (enhanced) list.
               
               Otherwise, 'params' (just) is forwarded to the __init__ method
               of the parent 'list' class as is.
          """

          #handle parameters and call the __init__ of the parent 'list' class accordingly
          if    len(params) <= 1:
                #no or one parameter ==> use it as parameter for __init__ of the parent class
                list.__init__(self, *params)
                
          else:
                #several parameters ==> use it as initial elements of the (enhanced) list
                list.__init__(self,  params)
                
                
      #method testing __init__
      @classmethod
      @muteLogging
      def _initSelftest(cls):
          """ """
          
          print ( "Testing EnhList.__init__..." )
          
          #no parameter
          assert EnhList() == []

          #one -non iterable- parameter  
          try:        
                  assert EnhList(1)
                  assert False
          except:
                  pass
                
          #one -iterable- parameter
          assert EnhList([1,3,5,7]) == [1,3,5,7]
          assert EnhList((1,3,5,7)) == [1,3,5,7]
          
          
          #several parameters
          assert EnhList(1,3,5,7) == [1,3,5,7]
          
          print ( "...EnhList.__init__ tested sucessfully!" )
                
                
      #push element to the end
      @logExceptions
      def push(self, *params):
          """
              The methods 'push' and 'pop' implement a FIFO.
              
              'Push' hereby appends to the end of the (enhanced) list.
              
              It accepts no, one or several parameters (elements) to be appended.
              Returns None.
          """
          
          #accept no, one or several parameters
          if    len(params) == 1:
                #one parameter
                self.append( *params )
                
          else:
                #no or several parameters
                self.extend( params ) 
                
                
      #method testing push
      @classmethod
      def _pushSelftest(cls):
          """ """
          
          print ( "Testing EnhList.push..." )
          
          testL = EnhList(1,3,5,7)
          
          #no parameter
          testL.push()
          assert testL == [1,3,5,7]
          
          #one parameter
          testL.push(9)
          assert testL == [1,3,5,7,9]
          
          #several parameters
          testL.push(11,13,15)
          assert testL == [1,3,5,7,9,11,13,15]
          
          print ( "...EnhList.push tested sucessfully!" )                

                                
      #pop element(s) meeting a condition
      @logExceptions
      def pop(self, selector=0, multitude=several):
          """
              The methods 'push' and 'pop' implement a FIFO.
              
              By default (with no parameter given), 'pop' hereby pops from the 
              beginning of the (enhanced) list.
              
              If the parameter 'selector' is a (condition) function resp. partial, taking
              one parameter, namely an element, (just) the elements, for which said
              function resp. partial returns True, are popped.
              
              If, in this situation, the parameter 'multitude' is 'single', just the first
              element meeting said condition is popped (if there is none, None is returned), 
              whereas if it is 'several', all elements meeting said condition are popped.
              
              If on the other hand the 'selector' parameter neither is of type function 
              nor of type partial, it is (just) forwarded to the list.pop method, leading
              to the behaviour of the standard list type.
          """
             
          if  isinstance(selector, (Types_FunctionType, Functools_partial)):
                #selector is a function, returning True (just) for the elements to be popped
                selectionFunction = selector
          
                if    multitude is single:
                      #just pop the (very) first element meeting the condition
                      for indexI in xrange(len(self)):
                          if selectionFunction( self[indexI] ) == True:
                             return list.pop( self, indexI )
                          
                      #if no element meets the condition, return None
                      return None
          
                elif  multitude is several:
                      #pop all elements meeting the condition
          
                      popL              = EnhList()
                      indexI            = len(self) - 1
                               
                      #process list starting from the end using indices - as the list might be 
                      #modified during processing (by the pops)
                      while indexI >= 0:
                          
                            #just pop elements, for which selectionFunction(element) returns True 
                            if selectionFunction( self[indexI] ) == True:
                               popL.insert(0, list.pop( self, indexI ))
                         
                            #next element
                            indexI -= 1
                          
                          
                      #return the (enhanced) list containing the popped elements
                      #if no element met the condition, said list is empty
                      return popL
                     
                else:
                      raise Exception("The parameter 'multitude' must either be 'single' or 'several'!")
                      
          else:    
                #standard list behaviour 
                #selector should be an index to the element to be popped
                return list.pop(self, selector)  


      #method testing pop
      @classmethod
      def _popSelftest(cls):
          """ """
          
          print ( "Testing EnhList.pop..." )
          
          #no parameter
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop() == 1
          assert testL == [3,5,7,9,11,13,15]
          
          #index parameter
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop(4) == 9
          assert testL == [1,3,5,7,11,13,15]
          
          #(lambda) function parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop( lambda x: (x > 6) and (x < 10) ) == [7,9]
          assert testL == [1,3,5,11,13,15]
          
          #(lambda) function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop( lambda x: (x < 6) or (x > 10) ) == [1,3,5,11,13,15]
          assert testL == [7,9]   
          
          #(lambda) function parameter - just the first
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop( lambda x: (x > 6), single ) == 7
          assert testL == [1,3,5,9,11,13,15]
          
          #(lambda) function parameter - none
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop( lambda x: (x > 15), single ) == None
          assert testL == [1,3,5,7,9,11,13,15]         
                      
          #'partial' parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop( (elem > 6) & (elem < 10) ) == [7,9]
          assert testL == [1,3,5,11,13,15]
          
          #'partial' function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop( (elem < 6) | (elem > 10) ) == [1,3,5,11,13,15]
          assert testL == [7,9]
          
          #'partial' function parameter - just the first
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop( (elem > 6), single ) == 7
          assert testL == [1,3,5,9,11,13,15]
          
          #'partial' function parameter - none
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.pop( (elem > 15), single ) == None
          assert testL == [1,3,5,7,9,11,13,15]          
          
          print ( "...EnhList.pop tested sucessfully!" )                                          
                
                
      #get element(s) meeting a condition
      @logExceptions
      def __getitem__(self, *params):
          """
              If the first positional parameter is a (condition) function resp. partial, 
              taking one parameter, namely an element, (just) the elements, for which said
              function resp. partial returns True, are returned.
              
              If, in this situation, the second parameter is 'single', 
              just the first element meeting said condition is returned 
              (if there is none, None is returned), whereas if it is 'several', 
              all elements meeting said condition are returned. Default is 'several'.
              
              If on the other hand the first positional parameter neither is of type 
              function nor of type partial, the parameters (just) are forwarded to 
              the list.__getitem__ method, leading to the behaviour of the standard 
              list type.
          """

          #getitem just takes exactly one parameter, this is why, if several
          #are given, e.g. self[a,b], this leads to params == ((a,b),),
          #which is not the common way of passing parameters to methods
          #the following changes this back to the common way
          paramsT = tuple()
          if (len(params) > 0):
             if     isinstance( params[0], Types_TupleType ):
                    #if params is a tuple containing a tuple (at the first position)
                    paramsT = params[0]
                
             else:
                    #if params is a tuple containing a non-tuple (at the first position)
                    paramsT = params
          
          #one or two 'real' parameters are accepted
          if    len(paramsT) == 1:
                #exactly one positional parameter ==> use it as the selector
                selector  = paramsT[0]
                multitude = several           #use a default for multitude
                
          elif  (len(paramsT) == 2) and (paramsT[1] in (single, several)):
                #two positional parameters and the second either is 'single' or 'several'
                selector  = paramsT[0]
                multitude = paramsT[1]
                
          else:
                raise Exception( "Either one parameter or two parameters - with the "  \
                                 "second being 'single' or 'several' - is allowed!"    )
          
          #check, whether the selector is a function or a 'partial' or something else
          if  isinstance(selector, (Types_FunctionType, Functools_partial)):
                #selector is a function, returning True (just) for the elements to be returned
                selectionFunction = selector
          
                if    multitude is single:
                      #just return the (very) first element meeting the condition
                      for indexI in xrange(len(self)):
                          if selectionFunction( self[indexI] ) == True:
                             return list.__getitem__( self, indexI )
                          
                      #if no element meets the condition, return None
                      return None
          
                elif  multitude is several:
                      #return all elements meeting the condition                
                      return EnhList([ element for element in self if selectionFunction(element) == True ])
                     
                else:
                      raise Exception("The parameter 'multitude' must either be 'single' or 'several'!")
                      
          else:    
                #forward to standard list behaviour 
                return list.__getitem__( self, selector )
                
                
      #method testing __getitem__
      @classmethod
      def _getitemSelftest(cls):
          """ """
          
          print ( "Testing EnhList.__getitem__..." )
          
          #index parameter
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL[4] == 9
          assert testL == [1,3,5,7,9,11,13,15]
          
          #cross check slicing
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL[4:6] == [9,11]
          assert testL == [1,3,5,7,9,11,13,15]
          
          #cross check slicing with step with 2
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL[2:7:2] == [5,9,13]
          assert testL == [1,3,5,7,9,11,13,15]          
          
          #(lambda) function parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL[ lambda x: (x > 6) and (x < 10) ] == [7,9]
          assert testL == [1,3,5,7,9,11,13,15]
          
          #(lambda) function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL[ lambda x: (x < 6) or (x > 10) ] == [1,3,5,11,13,15]
          assert testL == [1,3,5,7,9,11,13,15]
          
          #(lambda) function parameter - just the first
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL[ lambda x: (x > 6), single ] == 7
          assert testL == [1,3,5,7,9,11,13,15]
          
          #(lambda) function parameter - none
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL[ lambda x: (x > 15), single ] == None
          assert testL == [1,3,5,7,9,11,13,15]        
                      
          #'partial' parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL[ (elem > 6) & (elem < 10) ] == [7,9]
          assert testL == [1,3,5,7,9,11,13,15]
          
          #'partial' function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL[ (elem < 6) | (elem > 10) ] == [1,3,5,11,13,15]
          assert testL == [1,3,5,7,9,11,13,15]
          
          #'partial' function parameter - just the first
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL[ (elem > 6), single ] == 7
          assert testL == [1,3,5,7,9,11,13,15]
          
          #'partial' function parameter - none
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL[ (elem > 15), single ] == None
          assert testL == [1,3,5,7,9,11,13,15]     
          
          print ( "...EnhList.__getitem__ tested sucessfully!" )                 
        
                      
      ##delete element(s) meeting a condition
      @logExceptions
      def __delitem__(self, *params):
          """ 
              If the first positional parameter is a (condition) function resp. partial, 
              taking one parameter, namely an element, (just) the elements, for which said
              function resp. partial returns True, are deleted.
              
              If, in this situation, the second parameter is 'single', 
              just the first element meeting said condition is deleted 
              (if there is none, None is returned), whereas if it is 'several', 
              all elements meeting said condition are deleted. Default is 'several'.
              
              If on the other hand the first positional parameter neither is of type 
              function nor of type partial, the parameter (just) is forwarded to 
              the list.__delitem__ method, leading to the behaviour of the standard 
              list type.
          """

          #delitem just takes exactly one parameter, this is why, if several
          #are given, e.g. self[a,b], this leads to params == ((a,b),),
          #which is not the common way of passing parameters to methods
          #the following changes this back to the common way
          paramsT = tuple()
          if (len(params) > 0):
             if     isinstance( params[0], Types_TupleType ):
                    #if params is a tuple containing a tuple (at the first position)
                    paramsT = params[0]
                
             else:
                    #if params is a tuple containing a non-tuple (at the first position)
                    paramsT = params
          
          #one or two 'real' parameters are accepted
          if    len(paramsT) == 1:
                #exactly one positional parameter ==> use it as the selector
                selector  = paramsT[0]
                multitude = several
                
          elif  (len(paramsT) == 2) and (paramsT[1] in (single, several)):
                #two positional parameters and the second either is 'single' or 'several'
                selector  = paramsT[0]
                multitude = paramsT[1]
                
          else:
                raise Exception( "Either one parameter or two parameters - with the "  \
                                 "second being 'single' or 'several' - is allowed!"    )
          
          #check, whether the selector is a function or a 'partial' or something else
          if  isinstance(selector, (Types_FunctionType, Functools_partial)):
                #selector is a function, returning True (just) for the elements to be returned
                selectionFunction = selector
          
                if    multitude is single:
                      #just delete the (very) first element meeting the condition
                      for indexI in xrange(len(self)):
                          if selectionFunction( self[indexI] ) == True:
                             return list.__delitem__( self, indexI )
                          
                      #if no element meets the condition, do nothing and return None
                      return None
          
                elif  multitude is several:
                      #delete all elements meeting the condition
          
                      indexI            = len(self) - 1
                               
                      #process list starting from the end using indices - as the list might be 
                      #modified during processing (by the deletions)
                      while indexI >= 0:
                          
                            #just delete elements, for which selectionFunction(element) returns True 
                            if selectionFunction( self[indexI] ) == True:
                               list.__delitem__(self, indexI )
                         
                            #next element
                            indexI -= 1
                          
                      #return the None
                      return None
                     
                else:
                      raise Exception("The parameter 'multitude' must either be 'single' or 'several'!")
                      
          else:    
                #forward to standard list behaviour 
                return list.__delitem__( self, selector )
                
                
      #method testing __getitem__
      @classmethod
      def _delitemSelftest(cls):
          """ """
          
          print ( "Testing EnhList.__delitem__..." )
          
          #index parameter
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[4]
          assert testL == [1,3,5,7,11,13,15]
          
          #cross check slicing
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[4:6]
          assert testL == [1,3,5,7,13,15]
          
          #cross check slicing with step with 2
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[2:7:2]
          assert testL == [1,3,7,11,15]          
          
          #(lambda) function parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ lambda x: (x > 6) and (x < 10) ]
          assert testL == [1,3,5,11,13,15]
          
          #(lambda) function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ lambda x: (x < 6) or (x > 10) ]
          assert testL == [7,9]
          
          #(lambda) function parameter - just the first
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ lambda x: (x > 6), single ]
          assert testL == [1,3,5,9,11,13,15]
          
          #(lambda) function parameter - none
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ lambda x: (x > 15), single ]
          assert testL == [1,3,5,7,9,11,13,15]        
                      
          #'partial' parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ (elem > 6) & (elem < 10) ]
          assert testL == [1,3,5,11,13,15]
          
          #'partial' function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ (elem < 6) | (elem > 10) ]
          assert testL == [7,9]
          
          #'partial' function parameter - just the first
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ (elem > 6), single ]
          assert testL == [1,3,5,9,11,13,15]
          
          #'partial' function parameter - none
          testL = EnhList(1,3,5,7,9,11,13,15)
          del testL[ (elem > 15), single ]
          assert testL == [1,3,5,7,9,11,13,15]     
          
          print ( "...EnhList.__delitem__ tested sucessfully!" )               
          
        
      #check whether element(s) meeting a condition is/are in list
      @logExceptions
      def __contains__(self, selector):
          """
              If the (positional) parameter is a (condition) function resp. partial, 
              taking one parameter, namely an element, __contains__ returns True, if
              the list contains an element, for which said condition function returns 
              True - False otherwise.
              
              If on the other hand the (positional) parameter neither is of type 
              function nor of type partial, the parameter (just) is forwarded to 
              the list.__contains__ method, leading to the behaviour of the standard 
              list type.
          """
          
          if  isinstance(selector, (Types_FunctionType, Functools_partial)):
                #selector is a function, returning True (just) for elements checked for
                selectionFunction = selector
          
                #just search until one element meeting the condition has been found
                for indexI in xrange(len(self)):
                    if selectionFunction( self[indexI] ) == True:
                       #one element meeting the condition found
                       return True
                          
                #if no element met the condition, return False
                return False
          
          else:    
                #standard list behaviour 
                #selector should be an index to the element to be deleted
                return list.__contains__(self, selector)  
                
                
      #method testing __contains__
      @classmethod
      def _containsSelftest(cls):
          """ """
          
          print ( "Testing EnhList.__contains__..." )
          
          #object
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert 7 in testL
              
          #(lambda) function parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert (lambda x: (x > 5) and (x < 9)) in testL
          
          #(lambda) function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert (lambda x: (x < 1) or (x > 15)) not in testL
          
          #'partial' parameter - logical 'or' and 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert (((elem == 3) | (elem == 7)) & ((elem > 4) | (elem < 4))) in testL
          
          print ( "...EnhList.__contains__ tested sucessfully!" )                 
        
   
      #check whether all elements of the list meet an condition
      @logExceptions
      def areAll(self, conditionFct):
          """ 
              Checks whether all elements of the list meet the condition
              described by the parameter conditionFct - which either can be a
              function or a 'partial' (inheritors are fine too).
              
              If conditionFct is True for all elements, True is returned - 
              False otherwise.
          """
          
          #ensure, that conditionFct is a function or a 'partial'
          assert isinstance(conditionFct, (Types_FunctionType, Functools_partial)),                           \
                 "The parameter 'conditionFct' must either be of type function or of type 'partial'!"
                 
          #just search until one element does not meet the condition has been found
          for indexI in xrange(len(self)):
              if conditionFct( self[indexI] ) == False:
                 #(at least) one element does not meet the condition
                 return False
                    
          #all elements met the condition
          return True
          
                                        
      #method testing areAll
      @classmethod
      def _areAllSelftest(cls):
          """ """
          
          print ( "Testing EnhList.areAll..." )
          
          #(lambda) function parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.areAll( lambda x: (x >= 1) and (x <= 15) )
          
          #(lambda) function parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.areAll( lambda x: (x >= 9) or (x <= 10) )
          
          #'partial' parameter - logical 'and'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.areAll( (elem >= 1) & (elem <= 15) )
          
          #'partial' parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert testL.areAll( (elem >= 9) | (elem <= 10) )

          #'partial' parameter - logical 'or'
          testL = EnhList(1,3,5,7,9,11,13,15)
          assert not testL.areAll( (elem >= 11) | (elem <= 8) )          
          
          print ( "...EnhList.areAll tested sucessfully!" ) 


      #map function to all elements meeting condition
      @logExceptions
      def mapIf(self, *params):
          """ 
               The first positional parameter 'mapO' is the 
               function / 'partial' / object to be  
               mapped to the list elements (inheritors are fine too). 
               
               The second positional parameter 'conditionFct' is the 
               condition function / 'partial'
               - the mapping just is done for list elements, which meet said 
               condition (means: for which the condition function returns True).
               
               If the (second positional) parameter 'conditionFct' is omitted, 
               it defaults to: 'lambda x: True' (means: True in any case).
          """
             
          #method accepts one or two parameters          
          if    len(params) == 1:
                #map all elements
                mapO = params[0]
                
                #ensure the correct type for mapO
                assert isinstance(mapO, (Types_FunctionType, Functools_partial, object)), \
                       "First positional parameter 'mapO' has the wrong type!"
                
                #map mapO to all elements - in-place
                for indexI in xrange(len(self)):
                    self[indexI] = mapO( self[indexI] )
                 
          elif  len(params) == 2:
                #just map elements, meeting the condition
                mapO         = params[0]
                conditionFct = params[1] 
                
                #ensure the correct type for mapO and conditionFct
                assert isinstance(mapO,         (Types_FunctionType, Functools_partial, object))          and \
                       isinstance(conditionFct, (Types_FunctionType, Functools_partial, Types_NoneType)),     \
                       "Parameter types do not fit!"                
                
                #map mapO to all elements, for which conditionFct returns True - in place
                for indexI in xrange(len(self)):
                    if conditionFct( self[indexI] ) == True:
                       self[indexI] = mapO( self[indexI] )
                       
          else:
                raise Exception("Method expects one or two parameters!")
              
              
      #method testing mapAll
      @classmethod
      def _mapIfSelftest(cls):
          """ """
          
          print ( "Testing EnhList.mapIf..." )
          
          #(lambda) function parameter
          testL = EnhList(1,3,5,7,9)
          testL.mapIf( lambda x: x*2 )
          assert testL == [2,6,10,14,18]
          
          #object parameter
          testL = EnhList(1,3,5,7,9)
          class testO(object):
                def __init__(self, value):
                    self.abc = value
          testL.mapIf( testO )
          assert [element.abc for element in testL] == [1,3,5,7,9]    
          
          ### with condition ###
          #(lambda) function parameter
          testL = EnhList(range(1,10))
          testL.mapIf( lambda x: x*2, lambda x: x % 2 == 0)
          assert testL == [1,4,3,8,5,12,7,16,9]
          
          #object parameter
          testL = EnhList(range(1,10))
          class testO(object):
                def __init__(self, value):
                    self.abc = value
                def __repr__(self):
                    return "abc=%s" % self.abc
                def __eq__(self, ohs):
                    return (True if self.abc == ohs else False)
          testL.mapIf( testO, elem > 5 )
          assert testL == [1,2,3,4,5,testO(6),testO(7),testO(8),testO(9)]

          print ( "...EnhList.mapIf tested sucessfully!" )  


      #method testing self
      @classmethod
      def _selftest(cls):            
          """
              If no exception is raised during the execution of this method 
              the EnhList class behaves as expected.
              
              It e.g. can be used to check the integrity after modifications
              or to check the compatibility with specific python versions.
              
              Have a look into the methods called in this method for examples,
              how EnhList can be used.
          """
          
          cls._initSelftest()
          cls._pushSelftest()
          cls._popSelftest()
          cls._getitemSelftest()
          cls._delitemSelftest()
          cls._containsSelftest()
          cls._areAllSelftest()
          cls._mapIfSelftest()
          

                              
##################
### Test Means ###
##################
class TestO(object):
      """ """
      
      def __init__(self, val):
          """ """
          
          self.a = val   
          self.b = val
          
      def __eq__(self, ohs):
          return (self.a==ohs.a) and (self.b==ohs.b)
 
      def __repr__(self):
          return "(a=%s, b=%s)" % (self.a, self.b)  
          
class TestL(list):
      """ """

      def __init__(self, val):
          """ """
          
          list.__init__(self, (val, val, val))
 
class TestD(dict):
      """ """
      
      def __init__(self, val):
          """ """
          
          dict.__init__(self, a=val, b=val)
          
      def __eq__(self, ohs):
          return (self['a']==ohs['a']) and (self['b']==ohs['b'])
          
      
#############################
# module selfttest function #
#############################
def selftest():
    """
        Calls all test functions contained in this module.
        If there is no exception resp. assertion error, module seems to do what it
        is expected to.
    """
    
    print ( "Testing Module..." )
    
    _testElem()
    EnhList._selftest()
    
    ### test attribute and item access using 'elem' ###
    #list of objects with attributes 
    print ( "Testing attribute and item access..." )
    
    enhList = EnhList( range(1,17) )
    poppedL = enhList.pop( ((elem > 3) & (elem < 9)) | ((elem > 9) & (elem < 15)) )
    assert poppedL  == [4,5,6,7,8,10,11,12,13,14]
    assert enhList  == [1,2,3,9,15,16]
    
    #list of objects with attributes 
    enhList = EnhList( map(TestO, range(1,17)) )
    poppedL = enhList.pop( ((elem.a > 3) & (elem.a < 9)) | ((elem.b > 9) & (elem.b < 15)) )
    assert poppedL  == list(map(TestO, [4,5,6,7,8,10,11,12,13,14]))
    assert enhList  == list(map(TestO, [1,2,3,9,15,16]))

    #list of lists 
    enhList = EnhList( map(TestL, range(1,17)) )
    poppedL = enhList.pop( ((elem[0] > 3) & (elem[2] < 9)) | ((elem[0] > 9) & (elem[2] < 15)) )
    assert poppedL  == list(map(TestL, [4,5,6,7,8,10,11,12,13,14]))
    assert enhList  == list(map(TestL, [1,2,3,9,15,16]))  
   
    #list of dictionaries 
    enhList = EnhList( map(TestD, range(1,17)) )
    poppedL = enhList.pop( ((elem['a'] > 3) & (elem['b'] < 9)) | ((elem['a'] > 9) & (elem['b'] < 15)) )
    assert poppedL  == list(map(TestD, [4,5,6,7,8,10,11,12,13,14]))
    assert enhList  == list(map(TestD, [1,2,3,9,15,16]))
    
    print ( "...attribute and item access tested successfully!" )
    
    print ( "...Module tested successfully!" )        
          

       
       
if __name__ == "__main__":
  
   #parse command line arguments
   argParser = Argparse_ArgumentParser()
   argParser.add_argument("--test", action="store_true", help="run code testing this library for errors using test cases.")
   argParser.add_argument("--intro", action="store_true", help="print introduction to this library.")
   
   args      = argParser.parse_args()
   

   #run tests if '--test' is given in command line
   if    args.test == True:          
         selftest()
         
   if    args.intro == True:
         introS=\
"""
############
# EnhList: #
############
""" + EnhList.__doc__

         print (introS)
      
      
      
#TBD: add multi threading / processing locked version
#TBD: add type locked version
#TBD: check cythonized





