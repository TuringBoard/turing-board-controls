# Copyright (c) 2019 Cvsae
# Distributed under the MIT/X11 software license, see the accompanying
# file license http://www.opensource.org/licenses/mit-license.php.



class Iterable(object):
  class Iterator(object):
    def __init__(self, data, pos=0):
      self.data = data
      self.pos = pos


    def __getitem__(self, pos=0):
      return self.data[self.pos + pos]

    def __setitem__(self, pos, value):
      self.data[self.pos + pos] = value

    def __iadd__(self, increment):
      self.pos += increment
      return self

    def __isub__(self, decrement):
      self.pos -= decrement
      return self

    def __ne__(self, other):
      return self.data != other.data or self.pos != other.pos

    def __eq__(self, other):
      return not (self != other)

  #######################################################################################################
  # Modifiers
  #

  def push_back(self, data):
    # Add data to the end of the vector
    # @data : paramm to be added
    self.append(data)

  def pop_back(self):
    # Removes last element
    del self[-1]

  def clear(self):
    # Clear vector elements 
    del self[:]

  #########################################################################################################
  #  Element access
  #

  def front(self):
    # Return the first element in vector
    return self[0]
  
  def back(self):
    # Return the last element in vector
    return self[-1]

  #########################################################################################################
  # Capacity
  #

  def empty(self):
    # Returns true if the vector is empty
    # Thus begin() would equal end()
    return self.begin() == self.end()

  def capacity(self):
    # Returns the total number of elements that the vector can*  hold before needing to allocate more memory.
    pass 

  def resize(self):
    # Change size
    pass
 
  def reserver(self):
    # Request a change in capacity
    pass
  
  def size(self):
    return len(self)

  
  #########################################################################################################
  # Iterators
  #

  def begin(self):
    # Returns a iterator that points to the* first element in the %vector.
    return self.Iterator(self)

  def end(self):
    # Returns a iterator that points one past*  the last element in the %vector
    return self.Iterator(self, len(self))