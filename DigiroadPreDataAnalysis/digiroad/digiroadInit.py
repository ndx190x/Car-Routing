import getopt
import sys

from digiroad.carRoutingExceptions import ImpedanceAttributeNotDefinedException, NotParameterGivenException
from digiroad.connection import WFSServiceProvider
from digiroad.logic.MetropAccessDigiroad import MetropAccessDigiroadApplication
from digiroad.util import CostAttributes, getConfigurationProperties


def printHelp():
    print (
        "DigiroadPreDataAnalysis tool\n"
        "\n\t[--help]: Print information about the parameters necessary to run the tool."
        "\n\t[-s, --start_point]: Geojson file containing all the pair of points to calculate the shortest path between them."
        "\n\t[-e, --end_point]: Geojson file containing all the pair of points to calculate the shortest path between them."
        "\n\t[-o, --outputFolder]: The final destination where the output geojson and summary files will be located."
        "\n\t[-c, --cost]: The impedance/cost attribute to calculate the shortest path."
        "\n\t[--all]: Calculate the shortest path to all the impedance/cost attributes."
        "\n\nImpedance/cost values allowed:"
        "\n\tDISTANCE"
        "\n\tSPEED_LIMIT_TIME"
        "\n\tDAY_AVG_DELAY_TIME"
        "\n\tMIDDAY_DELAY_TIME"
        "\n\tRUSH_HOUR_DELAY"
    )


def main():
    """
    Read the arguments written in the command line to read the input coordinates from a
    Geojson file (a set of pair points) and the location (URL) to store the Shortest Path geojson features for each
    pair of points.

    Call the ``calculateTotalTimeTravel`` from the WFSServiceProvider configured
    with the parameters in './resources/configuration.properties' and calculate the shortest path for each
    pair of points and store a Geojson file per each of them.

    After that, call the function ``createSummary`` to summarize the total time expend to go from one point to another
    for each of the different impedance attribute (cost).

    :return: None. All the information is stored in the ``shortestPathOutput`` URL.
    """
    argv = sys.argv[1:]
    opts, args = getopt.getopt(argv, "s:e:o:c:", ["start_point=", "end_point=", "outputFolder=", "cost", "all", "help"])

    startPointsGeojsonFilename = None
    outputFolder = None
    # impedance = CostAttributes.DISTANCE
    impedance = None
    impedances = {
        "DISTANCE": CostAttributes.DISTANCE,
        "SPEED_LIMIT_TIME": CostAttributes.SPEED_LIMIT_TIME,
        "DAY_AVG_DELAY_TIME": CostAttributes.DAY_AVG_DELAY_TIME,
        "MIDDAY_DELAY_TIME": CostAttributes.MIDDAY_DELAY_TIME,
        "RUSH_HOUR_DELAY": CostAttributes.RUSH_HOUR_DELAY
    }

    allImpedanceAttribute = False

    impedanceErrorMessage = "Use the paramenter -c or --cost.\nValues allowed: DISTANCE, SPEED_LIMIT_TIME, DAY_AVG_DELAY_TIME, MIDDAY_DELAY_TIME, RUSH_HOUR_DELAY.\nThe parameter --all enable the analysis for all the impedance attributes."

    for opt, arg in opts:
        if opt in "--help":
            printHelp()
            return

        print("options: %s, arg: %s" % (opt, arg))

        if opt in ("-s", "--start_point"):
            startPointsGeojsonFilename = arg

        if opt in ("-e", "--end_point"):
            endPointsGeojsonFilename = arg

        if opt in ("-o", "--outputFolder"):
            outputFolder = arg

        if opt in "--all":
            allImpedanceAttribute = True
        else:
            if opt in ("-c", "--cost"):
                if arg not in impedances:
                    raise ImpedanceAttributeNotDefinedException(
                        impedanceErrorMessage)

                impedance = impedances[arg]

    if not startPointsGeojsonFilename or not endPointsGeojsonFilename or not outputFolder:
        raise NotParameterGivenException("Type --help for more information.")

    if not allImpedanceAttribute and not impedance:
        raise ImpedanceAttributeNotDefinedException(
            impedanceErrorMessage)

    config = getConfigurationProperties()

    starter = MetropAccessDigiroadApplication()
    wfsServiceProvider = WFSServiceProvider(wfs_url=config["wfs_url"],
                                            nearestVertexTypeName=config["nearestVertexTypeName"],
                                            nearestCarRoutingVertexTypeName=config["nearestCarRoutingVertexTypeName"],
                                            shortestPathTypeName=config["shortestPathTypeName"],
                                            outputFormat=config["outputFormat"])

    if impedances and not allImpedanceAttribute:
        starter.calculateTotalTimeTravel(wfsServiceProvider=wfsServiceProvider,
                                         startCoordinatesGeojsonFilename=startPointsGeojsonFilename,
                                         endCoordinatesGeojsonFilename=endPointsGeojsonFilename,
                                         outputFolderPath=outputFolder,
                                         costAttribute=impedance)
        starter.createSummary(outputFolder, impedance, "metroAccessDigiroadSummary.geojson")

    if allImpedanceAttribute:
        for key in impedances:
            starter.calculateTotalTimeTravel(wfsServiceProvider=wfsServiceProvider,
                                             startCoordinatesGeojsonFilename=startPointsGeojsonFilename,
                                             endCoordinatesGeojsonFilename=endPointsGeojsonFilename,
                                             outputFolderPath=outputFolder,
                                             costAttribute=impedances[key])
