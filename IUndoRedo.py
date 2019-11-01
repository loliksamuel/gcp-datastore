from abc import ABCMeta


class IUndoRedo(metaclass=ABCMeta):
    """The Undo Redo interface"""
    @abstractstaticmethod
    def history():
        """the history of the states"""

    @abstractstaticmethod
    def undo():
        """for undoing the hsitory of the states"""

    @abstractstaticmethod
    def redo():
        """for redoing the hsitory of the states"""