/** Commonly-used functions */

function hypot(...val) {
  return Math.sqrt(val.reduce((previousValue, currentValue) => (previousValue + Math.pow(currentValue, 2)), 0));
}

function distance(p1, p2) {
  return hypot(p2.x - p1.x, p2.y - p1.y);
}

function ensureLoadedFaceApi(uri, callback=null) {
  if (!!callback) {
    Promise.all([
      faceapi.nets.tinyFaceDetector.loadFromUri(uri),
      faceapi.nets.faceLandmark68Net.loadFromUri(uri),
      faceapi.nets.faceRecognitionNet.loadFromUri(uri),
      faceapi.nets.faceExpressionNet.loadFromUri(uri)
    ]).then(callback)
  } else {
    faceapi.nets.tinyFaceDetector.loadFromUri(uri)
    faceapi.nets.faceLandmark68Net.loadFromUri(uri)
    faceapi.nets.faceRecognitionNet.loadFromUri(uri)
    faceapi.nets.faceExpressionNet.loadFromUri(uri)
  }
}

function getEyeLengthByCoordinates(eyeCoordinates) {
  let left_point, right_point, top_point, bot_point
  left_point = [eyeCoordinates[0].x, eyeCoordinates[0].y]
  right_point = [eyeCoordinates[3].x, eyeCoordinates[3].y]
  top_point = [(eyeCoordinates[1].x + eyeCoordinates[2].x) / 2, (eyeCoordinates[1].y + eyeCoordinates[2].y) / 2]
  bot_point = [(eyeCoordinates[4].x + eyeCoordinates[5].x) / 2, (eyeCoordinates[4].y + eyeCoordinates[5].y) / 2]
  let vert_length, hor_length
  hor_length = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
  vert_length = hypot((top_point[0] - bot_point[0]), (top_point[1] - bot_point[1]))
  return [hor_length, vert_length]

}

function getMaxMinCoordinates(eyeCoordinates) {

  let x = [], y = [];
  eyeCoordinates.forEach(p => { x.push(p.x); y.push(p.y)} )
  let min_x = Math.min(...x), min_y = Math.min(...y), max_x = Math.max(...x), max_y = Math.max(...y);
  return [min_x, min_y, max_x, max_y]

}

function getEyeMask(width, height, eyeCoordinates) {

  let cvs;
  let maskRGBA;

  try {
    cvs = document.createElement('CANVAS');
    cvs.style.display = 'none';
    cvs.width = width;
    cvs.height = height;

    let ctx = cvs.getContext('2d');
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, width, height);

    let [f, ...r] = eyeCoordinates;
    ctx.beginPath();
    ctx.moveTo(f.x, f.y);
    r.forEach(p => ctx.lineTo(p.x, p.y));
    ctx.closePath();
    ctx.fillStyle = 'white';  // ctx.strokeStyle
    ctx.fill();  // ctx.fill

    maskRGBA = cv.imread(cvs);
    let mask = new cv.Mat();
    cv.cvtColor(maskRGBA, mask, cv.COLOR_RGBA2GRAY, 0);

    return mask;

  } finally {
    if (cvs) cvs.remove();
    if (maskRGBA) maskRGBA.delete();
  }

}

function getGrayEyeFromCanvas(canvas, eyeCoordinates) {

  let gray, mask;

  try {

    gray = cv.imread(canvas);
    cv.cvtColor(gray, gray, cv.COLOR_RGBA2GRAY, 0);

    mask = getEyeMask(canvas.width, canvas.height, eyeCoordinates);
    cv.bitwise_and(gray, gray, gray, mask);

    let [min_x, min_y, max_x, max_y] = getMaxMinCoordinates(eyeCoordinates).map(Math.round);
    let rect = new cv.Rect(min_x, min_y, max_x - min_x, max_y - min_y);
    return gray.roi(rect);

  } finally {
    if (gray) gray.delete();
    if (mask) mask.delete();
  }

}
