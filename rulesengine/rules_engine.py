#
# rulesengine/rules_engine.py
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
"""
Rules Engine
  Execute a path of functionality based on the Boolean value of each node.
  A binary tree algorithm is used in traversing the node tree.

by: Carl J. Nobile

email: carl.nobile@gmail.com
"""
__docformat__ = "restructuredtext en"


class RulesEngineException(Exception): pass
class InvalidNodeSizeException(RulesEngineException): pass


class Node(object):
    """
    A Node object that encapsulates an execution entity.
    """
    def __init__(self, method=None, left=None, right=None):
        """
        :Keywords:
          method : ``FunctionType``, ``LambdaType``, ``MethodType``, \
                   ``BuiltinFunctionType``, or ``BuiltinMethodType``
            A callable type that shall return a Boolean object. Default is
            `None`.
          left : `list`, `tuple`, or ``NoneType``
            A left branch can be a `list` or `tuple`. If a leaf the type
            shall be a ``NoneType``. Default is `None`.
          right : `list`, `tuple`, or ``NoneType``
            A right branch can be a `list` or `tuple`. If a leaf the type
            shall be a ``NoneType``. Default is `None`.
        """
        self.method = method
        self.left = left
        self.right = right


class RulesEngine(object):
    """
    An engine to execute a path of functionality. Each `Node` shall have one
    or two branches or leaves. The execution will follow all nodes where one
    or two branches are found and shall continue when all branches are
    exhausted and shall end when no further branches to traverse are found.
    """
    NO_INST = 999999999

    def __init__(self, this=None, storeSeq=False):
        """
        :Keywords:
          this : ``InstanceType``
            The object that the methods are called from. If `this` is None the
            `self` from the RulesEngine will be used. If `this` is an instance,
            that instance will be used. If `this` is the special value
            referred to by `RulesEngine.NO_INST` the node method is attached
            to an instance and there is no need to define one.
          storeSeq : `bool`
            The default `False` will not store the call method sequence. Set
            to `True` if you want the call sequence stored. Then get it with
            the `getCallSequence` method.
        """
        if this != RulesEngine.NO_INST:
            self._self = this is None and self or this
        else:
            self._self = None

        self._root = None
        self._reset()
        self._storeSeq = storeSeq

    def _reset(self):
        """
        Reset the iteration count and the call sequence.
        """
        self._iterCount = 0
        self._callSequence = []

    def load(self, seq):
        """
        Loads the execution tree. The node list object can be any combination
        of lists or tuples.

        example: ``[<function>, (<function>, None, None), None]``

        :Parameters:
          seq : `list` or `tuple`
            A sequence of nodes comprising an execution path.
        """
        self._root = Node()
        self.__insert(self._root, seq)
        return self._root

    def __insert(self, node, blist):
        """
        A recursive call that loads the sequence object into `Node` objects.

        :Parameters:
          node : `Node`
            The current node being loaded with sequence data.
          blist : `list` or `tuple`
            The current sequence object used to load the Node.

        :Exceptions:
          * `InvalidNodeSizeException`
            Indicates an invalid sequence size. Sequences shall always have a
            size of three.
        """
        size = len(blist)

        if size != 3:
            msg = "Invalid sequence size, expected: 3, " + \
                  "got: {}, on: {}".format(size, blist)
            raise InvalidNodeSizeException(msg)

        for i in range(size):
            item = blist[i]
            if 0 == i: node.method = item

            if isinstance(item, (list, tuple)):
                nnode = Node()
                self.__insert(nnode, item)
                if 1 == i: node.left = nnode
                if 2 == i: node.right = nnode

    def dump(self, **kwargs):
        """
        Dumps the result of the execution tree.

        :Parameters:
          kwargs : `dict`
            The possible keyword arguments that shall be passed to the
            callable objects in the `Node` objects.

        :Returns:
          The Boolean from first callable object.
        """
        self._reset()
        return self.__extract(self._root, **kwargs)

    def __extract(self, node, **kwargs):
        """
        A recursive call that dumps the result of each `Node` objects.

        :Parameters:
          node : `Node`
            The current node being executed.
          kwargs : `dict`
            The keyword arguments that are passed to the callable objects in
            the Node objects.

        :Returns:
          A Boolean from a callable object.
        """
        self._iterCount += 1

        if self._self is None:
            result = node.method(**kwargs)
        else:
            result = node.method(self._self, **kwargs)

        self._storeSeq and self._callSequence.append(node.method)

        if result:  # True take the left branch
            if isinstance(node.left, Node):
                result = self.__extract(node.left, **kwargs)
        else:  # False take the right branch
            if isinstance(node.right, Node):
                result = self.__extract(node.right, **kwargs)

        return result

    def getIterationCount(self):
        """
        Gets the resulting iteration count.

        :Returns:
          The ending iteration count.
        """
        return self._iterCount

    def getCallSequence(self):
        """
        Gets the call sequence. This is primarily used for testing.

        :Returns:
          A `list` of the method objects in the order they were called.
        """
        return self._callSequence
