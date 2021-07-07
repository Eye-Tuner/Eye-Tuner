
let DEBUG = true

let leftBlink, rightBlink;

let video, canvas2, canvas3, text;
let temp = document.createElement('canvas');

// let cap = new cv.VideoCapture(video); // todo

function Setup(callback=null) {
  /** Init debugging text field, video and canvases */

  document.body.innerText = "";

  video = document.createElement("VIDEO");
  video.style.position = "absolute";
  video.style.top = 0 + "px";
  video.style.left = 0 + "px";
  video.width = 749
  video.height = 560
  video.autoplay = true;
  video.defaultMuted = true;
  video.id = "video";
  if(!DEBUG){
    video.style.left = -window.innerWidth + "px";
  }
  video.load();
  document.body.appendChild(video);

  canvas2 = document.createElement("CANVAS");
  canvas2.style.position = "absolute";
  canvas2.style.top = 570 + "px";
  canvas2.style.left = 10 + "px";
  canvas2.width = 300
  canvas2.height = 150
  canvas2.id = "canvas2"
  document.body.appendChild(canvas2);

  canvas3 = document.createElement("CANVAS");
  canvas3.style.position = "absolute";
  canvas3.style.top = 730 + "px";
  canvas3.style.left = 10 + "px";
  canvas3.width = canvas2.width
  canvas3.height = canvas2.height
  canvas3.id = "canvas3"
  document.body.appendChild(canvas3);

  text = document.createElement("P");
  text.style.fontSize = "200%";
  text.style.position = "absolute";
  text.style.top = 600 + "px";
  text.style.left = 400 + "px";
  text.id = "txt";
  document.body.appendChild(text);

  if (!!callback) callback();

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

function startVideo(videoElement=video) {

  text.innerText = "Loading video... Please enable your video on browser"

  let errorCallback = err => {
    console.error(err);
    text.innerText = "";
    let a = document.createElement("A");
    a.href = "javascript:location.reload()";
    a.innerText = "Please reload page, video loading failed.";
    text.appendChild(a);
  };

  // userAgent: string type
  // if firefox use navigator.mediaDevices.getUserMedia instead of deprecated navigator.getUserMedia
  if (navigator.userAgent.indexOf("Firefox") > -1) {

    navigator.mediaDevices.getUserMedia({ audio: false, video: true })
    .then(function(stream) {
      videoElement.srcObject = stream;
      videoElement.onloadedmetadata = function(__) {
        videoElement.play();
      };
      text.innerText = "";
    })
    .catch(errorCallback);

  } else {

    navigator.getUserMedia(
      { video: {} },
      function (stream) {
        videoElement.srcObject = stream;
        text.innerText = "";
      },
      errorCallback
    )

  }
  return video;
}

function clearCanvas(c) {
  c.getContext("2d").clearRect(0, 0, c.width, c.height);
}


function detectFace(videoElement=video) {

}

function getVideoEventListener(
    videoElement=video,
    canvas2Element=canvas2,
    canvas3Element=canvas3,
) {
  return () => {

    let leftEye, rightEye, resizedLeftEye, resizedRightEye

    // Create the overlayed canvas and append it to body
    const canvas = faceapi.createCanvasFromMedia(videoElement);
    canvas.style.position = "absolute";
    canvas.style.top = 0 + "px";
    canvas.style.left = 0 + "px";
    const displaySize = { width: videoElement.width, height: videoElement.height };
    faceapi.matchDimensions(canvas, displaySize);
    document.body.append(canvas);

    // Get context of canvas2, canvas3
    let ctx = canvas2Element.getContext("2d");
    ctx.fillStyle = "#FF0000";
    let ctx2 = canvas3Element.getContext("2d");
    ctx2.fillStyle = "#FF0000";

    setInterval(async () => {  // face-api requires async function

      // Detect faces with face-api
      const detections = await faceapi.detectAllFaces(videoElement, new faceapi.TinyFaceDetectorOptions())
          .withFaceLandmarks()
          .withFaceExpressions();

      // Resize the detections to match the canvas size
      const resizedDetections = faceapi.resizeResults(detections, displaySize);

      [canvas, canvas2Element, canvas3Element].forEach(clearCanvas);

      if(DEBUG) {
        faceapi.draw.drawDetections(canvas, resizedDetections);
        faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
        faceapi.draw.drawFaceExpressions(canvas, resizedDetections);
      }

      // Check if there's only 1 face on the feed and change the BG color of winkScroll class element
      let backgroundColor;
      if(detections.length === 1){
        leftEye = detections[0].landmarks.getLeftEye();
        rightEye = detections[0].landmarks.getRightEye();
        resizedLeftEye = resizedDetections[0].landmarks.getLeftEye();
        resizedRightEye = resizedDetections[0].landmarks.getRightEye();
        backgroundColor = "#e6faff";
      } else {
        backgroundColor = "white";
      }
      for(let i=0; i<document.getElementsByClassName("winkScroll").length||0; i++) {
        document.getElementsByClassName("winkScroll")[i].style.backgroundColor = backgroundColor;
      }

      temp.width = videoElement.width;
      temp.height = videoElement.height;
      let tempCtx = temp.getContext('2d');
      tempCtx.drawImage(videoElement, 0, 0)

      // distance?
      // cannot read
      let disX = distance(resizedLeftEye[0], resizedLeftEye[3]) /2;
      let disY = distance(resizedLeftEye[1], resizedLeftEye[4]) -5;

      // Draw cropped image on canvas2
      // https://stackoverflow.com/questions/26015497/how-to-resize-then-crop-an-image-with-canvas
      ctx.drawImage( video,
        leftEye[0].x +10,        // start X
        leftEye[0].y - 3,        // start Y
        disX, disY,                                           // area to crop
        0, 0,                                                 // Place the result at 0, 0 in the canvas,
        canvas2.width, canvas2.height
      );

      let blink_ratio_r = getBlinkingRatio(rightEye);
      let blink_ratio_l = getBlinkingRatio(leftEye);

      let blink_threshold = 3.45;  // todo: not precise as Dlib
      if (DEBUG) console.log('blink ratio:', blink_ratio_r, blink_ratio_l);  // todo

      if(blink_ratio_r >= blink_threshold && blink_ratio_l >= blink_threshold) {
        text.innerHTML = "Both blinking";
        text.style.backgroundColor = "red";
        leftBlink++; rightBlink++;
      } else if(blink_ratio_r >= blink_threshold) {
        text.innerHTML = "Right blinking";
        text.style.backgroundColor = "blue";
        rightBlink++;
      } else if(blink_ratio_l >= blink_threshold) {
        text.innerHTML = "Left blinking";
        text.style.backgroundColor = "blue";
        leftBlink++;
      } else {
        text.innerHTML = "No blinking";
        text.style.backgroundColor = "white";
      }

      let gaze_ratio_r = getGazeRatio(temp, rightEye, canvas3);
      let gaze_ratio_l = getGazeRatio(temp, leftEye);
      let gaze_ratio = (gaze_ratio_r + gaze_ratio_l) / 2;

      if(gaze_ratio > 0) {
        if (gaze_ratio <= 1) {
          text.innerHTML += "& RIGHT";
        } else if (gaze_ratio < 3) {
          text.innerHTML += "& CENCER";
        } else {
          text.innerHTML += "& LEFT";
        }
      }

    }, /* todo: time interval */ 100)

  }
}

function getBlinkingRatio(eyeCoordinates) {
  let [hor_length, vert_length] = getEyeLengthByCoordinates(eyeCoordinates);
  return (hor_length / vert_length) || NaN;
}

function getGazeRatio(canvas, eyeCoordinates, threshShowDst=null) {

  let eye = getGrayEyeFromCanvas(canvas, eyeCoordinates);

  cv.threshold(eye, eye, 70, 255, cv.THRESH_BINARY);

  let [height, width] = eye.matSize
  let half_width = Math.round(width / 2)
  let threshold_left = eye.roi(new cv.Rect(0, 0, half_width, height))
  let threshold_right = eye.roi(new cv.Rect(half_width, 0, width - half_width, height))
  let white_left = cv.countNonZero(threshold_left)
  let white_right = cv.countNonZero(threshold_right)

  // todo
  if (DEBUG && !!threshShowDst) cv.imshow(threshShowDst, eye);
  //

  threshold_left.delete(); threshold_right.delete(); eye.delete();

  if (white_left === 0) {
    return 1
  } else if (white_right === 0) {
    return 5
  } else {
    return white_left / white_right
  }
}

Setup();
