# Notes:
# self refers to the reference of the current instance of the class.
# self._subscribers accesses the list that belongs to the specific instance.
# without self the method/fields is not associated with the instance and Python wont know what data to use.
# Python automatically passes self when you call methods to the object that is why self must be the first parameter of the function.



class Event:

    # Constructor of this class, basically it initializes the list called subscribers.
    # It is a list that will store functions that we want to call if there is an event
    # happening like a button click.
    def __init__(self):
        self._subscribers = []

    # This method adds a function to the list.
    # func is a function reference not a function call.
    def subscribe(self, func):
        self._subscribers.append(func)

    # This method removes a function to the list.
    def unsubscribe(self, func):
        self._subscribers.remove(func)

    # This method fires the methods inside of the list.
    # It loops then calls the functions so since we are not passing any arguments
    # it assumes the function has no parameters.
    def notify(self):
        for func in self._subscribers:
            func()


