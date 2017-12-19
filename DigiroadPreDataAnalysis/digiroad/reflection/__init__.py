import importlib
import inspect
import os

from digiroad.additionalOperations import AbstractAdditionalLayerOperation, EuclideanDistanceOperation, \
    WalkingTimeOperation, ParkingTimeOperation
from digiroad.util import LinkedList


class Reflection:
    def getLinkedAbstractAdditionalLayerOperation(self):

        euclideanDistanceAdditionalLayerOperation = EuclideanDistanceOperation()
        walkingAdditionalLayerOperation = WalkingTimeOperation()
        parkingAdditionalLayerOperation = ParkingTimeOperation()

        additionalLayersLinkedList = LinkedList()
        additionalLayersLinkedList.add(euclideanDistanceAdditionalLayerOperation)
        additionalLayersLinkedList.add(walkingAdditionalLayerOperation)
        additionalLayersLinkedList.add(parkingAdditionalLayerOperation)

        return additionalLayersLinkedList

    def getAbstractAdditionalLayerOperationObjects(self):
        """
        Retrieve all the specifications objects from the AbstractAdditionalLayerOperation class.

        :return: List of instances that are subclass of AbstractAdditionalLayerOperation.
        """
        mainPythonModulePath = "digiroad.additionalOperations"
        additionalOperationsList = self.getClasses(
            os.getcwd(),
            mainPythonModulePath,
            AbstractAdditionalLayerOperation
        )
        additionalOperationsList = sorted(additionalOperationsList, key=lambda _class: _class.getExecutionOrder())
        return additionalOperationsList

    def getClasses(self, root_directory, package_name, *classes):
        """
        Retrive all the instances from a module that are subclasses of the given *classes.

        :param root_directory: Project PYTHONPATH.
        :param package_name: Name of the module to inspect.
        :param classes: Generic class, e.g. AbstractAdditionalLayerOperation.
        :return: List of instances that are subclass of the given *classes.
        """
        additionalOperationsList = []
        moduleComponents = package_name.split(".")
        mainModulePath = ""
        for component in moduleComponents:
            mainModulePath = mainModulePath + os.sep + component

        moduleDirectory = root_directory + mainModulePath
        for file in os.listdir(moduleDirectory):
            if file.endswith(".py"):
                if file.endswith("__init__.py"):
                    modulePath = package_name
                else:
                    filename = file.replace(".py", "")
                    modulePath = package_name + "." + filename

                module = importlib.import_module(modulePath)
                self.__exploreModule(module,
                                     modulePath,
                                     additionalOperationsList,
                                     *classes)

        return additionalOperationsList

    def __exploreModule(self, module, modulePath, classesFound, *classes):
        """
        Recursive function to retrive the subclasses of the given *classes.

        :param module: Module instance.
        :param modulePath: Name of the module to inspect.
        :param classesFound: List of the instances created.
        :param classes: Generic classes.
        :return:
        """
        for element_name in dir(module):
            element = getattr(module, element_name)
            if inspect.isclass(element):
                if issubclass(element, classes) and not self.isContained(element.__name__, *classes):
                    the_object = element()
                    classesFound.append(the_object)
            elif inspect.ismodule(element):
                if modulePath.replace(".", os.sep) in element.__file__:
                    self.__exploreModule(element, modulePath)

    def isContained(self, __name__, *param):
        """
        Verify if the __name__ is contained in any tuple of *param.

        :param __name__: String name.
        :param param: Any string tuple.
        :return: True if __name__ is contained in *param, Otherwise, return False.
        """
        for _class in list(param):
            if __name__ == _class.__name__:
                return True

        return False