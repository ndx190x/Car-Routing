import json

from owslib.util import openURL

from digiroad.logic.Operations import Operations
from digiroad.util import FileActions


class WFSServiceProvider:
    def __init__(self, wfs_url="http://localhost:8080/geoserver/wfs?",
                 nearestVertexTypeName="", nearestCarRoutingVertexTypeName="",
                 shortestPathTypeName="", outputFormat="", epsgCode="EPSG:3857"):
        self.shortestPathTypeName = shortestPathTypeName
        self.__geoJson = None
        self.wfs_url = wfs_url
        self.nearestVertexTypeName = nearestVertexTypeName
        self.nearestCarRoutingVertexTypeName = nearestCarRoutingVertexTypeName
        self.outputFormat = outputFormat
        self.epsgCode = epsgCode
        self.operations = Operations(FileActions())

    # def getGeoJson(self):
    #     return self.__geoJson
    #
    # def setGeoJson(self, geojson):
    #     self.__geoJson = geojson

    def getNearestVertexFromAPoint(self, coordinates):
        """
        From the WFS Service retrieve the nearest vertex from a given point coordinates.

        :param coordinates: Point coordinates. e.g [889213124.3123, 231234.2341]
        :return: Geojson (Geometry type: Point) with the nearest point coordinates.
        """
        coordinates = self.operations.transformPoint(coordinates, self.epsgCode)

        url = self.wfs_url + "service=WFS&version=1.0.0&request=GetFeature&typeName=%s&outputformat=%s&viewparams=x:%s;y:%s" % (
            self.nearestVertexTypeName, self.outputFormat, str(
                coordinates.getLongitude()), str(coordinates.getLatitude()))

        return self.requestFeatures(url)

    def requestFeatures(self, url):
        """
        Request a JSON from an URL.

        :param url: URL.
        :return: Downloaded Json.
        """
        u = openURL(url)
        # return json.loads(u.read())
        return json.loads(u.read().decode('utf-8'))

    def getNearestCarRoutableVertexFromAPoint(self, coordinates):
        """
        From the WFS Service retrieve the nearest car routing vertex from a given point coordinates.

        :param coordinates: Point coordinates. e.g [889213124.3123, 231234.2341]
        :return: Geojson (Geometry type: Point) with the nearest point coordinates.
        """
        url = self.wfs_url + "service=WFS&version=1.0.0&request=GetFeature&typeName=%s&outputformat=%s&viewparams=x:%s;y:%s" % (
            self.nearestCarRoutingVertexTypeName, self.outputFormat, str(
                coordinates.getLongitude()), str(coordinates.getLatitude()))

        return self.requestFeatures(url)

    def getShortestPath(self, startVertexId, endVertexId, cost):
        """
        From a pair of vertices (startVertexId, endVertexId) and based on the "cost" attribute,
        retrieve the shortest path by calling the WFS Service.

        :param startVertexId: Start vertex from the requested path.
        :param endVertexId: End vertex from the requested path.
        :param cost: Attribute to calculate the cost of the shortest path
        :return: Geojson (Geometry type: LineString) containing the segment features of the shortest path.
        """
        url = self.wfs_url + "service=WFS&version=1.0.0&request=GetFeature&typeName=%s&outputformat=%s&viewparams=source:%s;target:%s;cost:%s" % (
            self.shortestPathTypeName, self.outputFormat,
            startVertexId, endVertexId, cost)

        return self.requestFeatures(url)

    def getEPSGCode(self):
        return self.epsgCode
