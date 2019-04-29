/**
 * geoJSON2JTS
 *
 * Convert GeoJSON polygons to JTS Coordinate objects as required by JTS.
 *
 * @param {array} boundaries in geoJSON format.
 * @return {array} boundaries in JTS friendly format.
 */
var geoJSON2JTS = function(boundaries) {
  var coordinates = [];
  for (var i = 0; i < boundaries.length; i++) {
    coordinates.push(new jsts.geom.Coordinate(
        boundaries[i][1], boundaries[i][0]));
  }
  return coordinates;
};

/**
 * findSelfIntersects
 *
 * Detect self-intersections in a polygon.
 *
 * @param {object} GeoJSON polygon co-ordinates.
 * @return {array} array of points of intersections.
 */
var findSelfIntersects = function(geoJsonPolygon) {
  var coordinates = geoJSON2JTS(geoJsonPolygon);
  var geometryFactory = new jsts.geom.GeometryFactory();
  var shell = geometryFactory.createLinearRing(coordinates);
  var jstsPolygon = geometryFactory.createPolygon(shell);

  // if the geometry is aleady a simple linear ring, do not
  // try to find self intersection points.
  var validator = new jsts.operation.IsSimpleOp(jstsPolygon);
  if (validator.isSimpleLinearGeometry(jstsPolygon)) {
    return;
  }

  var res = [];
  var graph = new jsts.geomgraph.GeometryGraph(0, jstsPolygon);
  var cat = new jsts.operation.valid.ConsistentAreaTester(graph);
  var r = cat.isNodeConsistentArea();
  if (!r) {
    var pt = cat.getInvalidPoint();
    res.push([pt.x, pt.y]);
  }
  return res;
};
