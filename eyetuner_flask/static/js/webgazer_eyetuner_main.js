// import '../lib/wg_eyetuner.js';

/* js/main.js */

window.onload = async function() {

    wg_eyetuner.params.showVideoPreview = true;
    //start the webgazer tracker
    await wg_eyetuner.setRegression('ridge') /* currently must set regression and tracker */
        //.setTracker('clmtrackr')
        .setListener(function(data, clock) {
          //   console.log(data); /* data is an object containing an x and y key which are the x and y prediction coordinates (no bounds limiting) */
          //   console.log(clock); /* elapsed time in milliseconds since webgazer.begin() was called */
        })
        .saveDataAcrossSessions(true)
        .begin();
        wg_eyetuner.showVideoPreview(true) /* shows all video previews */
            .showPredictionPoints(true) /* shows a square every 100 milliseconds where current prediction is */
            .applyKalmanFilter(true); /* Kalman Filter defaults to on. Can be toggled by user. */

    //Set up the webgazer video feedback.
    let setup = function() {

        //Set up the main canvas. The main canvas is used to calibrate the webgazer.
        let canvas = document.getElementById("plotting_canvas");
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        canvas.style.position = 'fixed';
    };
    setup();

};

// Set to true if you want to save the data even if you reload the page.
window.saveDataAcrossSessions = true;

window.onbeforeunload = function() {
    wg_eyetuner.end();
}

/**
 * Restart the calibration process by clearing the local storage and reseting the calibration point
 */
function Restart(){
    document.getElementById("Accuracy").innerHTML = "<a>Not yet Calibrated</a>";
    wg_eyetuner.clearData();
    ClearCalibration();
    PopUpInstruction();
}



/* js/calibration.js */

let PointCalibrate = 0;
let CalibrationPoints={};

/**
 * Clear the canvas and the calibration button.
 */
function ClearCanvas(){
  $(".Calibration").hide();
  let canvas = document.getElementById("plotting_canvas");
  canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
}

/**
 * Show the instruction of using calibration at the start up screen.
 */
function PopUpInstruction(){
  ClearCanvas();
  swal({
    title:"Calibration",
    text: "Please click on each of the 9 points on the screen. You must click on each point 5 times till it goes yellow. This will calibrate your eye movements.",
    buttons:{
      cancel: false,
      confirm: true
    }
  }).then(isConfirm => {
    ShowCalibrationPoint();
  });

}
/**
  * Show the help instructions right at the start.
  */
function helpModalShow() {
    $('#helpModal').modal('show');
}

/**
 * Load this function when the index page starts.
* This function listens for button clicks on the html page
* checks that all buttons have been clicked 5 times each, and then goes on to measuring the precision
*/
$(document).ready(function(){
  ClearCanvas();
  helpModalShow();
 $(".Calibration").click(function(){ // click event on the calibration buttons

  let id = $(this).attr('id');

  if (!CalibrationPoints[id]){ // initialises if not done
    CalibrationPoints[id]=0;
  }
  CalibrationPoints[id]++; // increments values

  if (CalibrationPoints[id]===5){ //only turn to yellow after 5 clicks
    $(this).css('background-color','yellow');
    $(this).prop('disabled', true); //disables the button
    PointCalibrate++;
  }else if (CalibrationPoints[id]<5){
    //Gradually increase the opacity of calibration points when click to give some indication to user.
    let opacity = 0.2*CalibrationPoints[id]+0.2;
    $(this).css('opacity',opacity);
  }

  //Show the middle calibration point after all other points have been clicked.
  if (PointCalibrate === 8){
    $("#Pt5").show();
  }

  if (PointCalibrate >= 9){ // last point is calibrated
        //using jquery to grab every element in Calibration class and hide them except the middle point.
        $(".Calibration").hide();
        $("#Pt5").show();

        // clears the canvas
        let canvas = document.getElementById("plotting_canvas");
        canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);

        // notification for the measurement process
        swal({
          title: "Calculating measurement",
          text: "Please don't move your mouse & stare at the middle dot for the next 5 seconds. This will allow us to calculate the accuracy of our predictions.",
          closeOnEsc: false,
          allowOutsideClick: false,
          closeModal: true
        }).then( isConfirm => {

            // makes the variables true for 5 seconds & plots the points
            $(document).ready(function(){

              store_points_variable(); // start storing the prediction points

              sleep(5000).then(() => {
                  stop_storing_points_variable(); // stop storing the prediction points
                  let past50 = wg_eyetuner.getStoredPoints(); // retrieve the stored points
                  let precision_measurement = calculatePrecision(past50);
                  document.getElementById("Accuracy").innerHTML = "<a>Accuracy | " + precision_measurement + "%</a>"; // Show the accuracy in the nav bar.
                  swal({
                    title: "Your accuracy measure is " + precision_measurement + "%",
                    allowOutsideClick: false,
                    buttons: {
                      cancel: "Recalibrate",
                      confirm: true,
                    }
                  }).then(isConfirm => {
                      if (isConfirm){
                        //clear the calibration & hide the last middle button
                        ClearCanvas();
                      } else {
                        //use restart function to restart the calibration
                        document.getElementById("Accuracy").innerHTML = "<a>Not yet Calibrated</a>";
                        wg_eyetuner.clearData();
                        ClearCalibration();
                        ClearCanvas();
                        ShowCalibrationPoint();
                      }
                  });
              });
            });
        });
      }

    });
});

/**
 * Show the Calibration Points
 */
function ShowCalibrationPoint() {
  $(".Calibration").show();
  $("#Pt5").hide(); // initially hides the middle button
}

/**
* This function clears the calibration buttons memory
*/
function ClearCalibration(){
  // Clear data from WebGazer

  let calibration = $(".Calibration")
  calibration.css('background-color','red');
  calibration.css('opacity',0.2);
  calibration.prop('disabled',false);

  CalibrationPoints = {};
  PointCalibrate = 0;
}

// sleep function because java doesn't have one, sourced from http://stackoverflow.com/questions/951021/what-is-the-javascript-version-of-sleep
function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
}

/* js/precision_calculation.js */


/**
 * This function calculates a measurement for how precise
 * the eye tracker currently is which is displayed to the user
 */
function calculatePrecision(past50Array) {
  let windowHeight = $(window).height();
  let windowWidth = $(window).width();

  // Retrieve the last 50 gaze prediction points
  let x50 = past50Array[0];
  let y50 = past50Array[1];

  // Calculate the position of the point the user is staring at
  let staringPointX = windowWidth / 2;
  let staringPointY = windowHeight / 2;

  let precisionPercentages = new Array(50);
  calculatePrecisionPercentages(precisionPercentages, windowHeight, x50, y50, staringPointX, staringPointY);
  let precision = calculateAverage(precisionPercentages);

  // Return the precision measurement as a rounded percentage
  return Math.round(precision);
}

/*
 * Calculate percentage accuracy for each prediction based on distance of
 * the prediction point from the centre point (uses the window height as
 * lower threshold 0%)
 */
function calculatePrecisionPercentages(precisionPercentages, windowHeight, x50, y50, staringPointX, staringPointY) {
  for (let x = 0; x < 50; x++) {
    // Calculate distance between each prediction and staring point
    let xDiff = staringPointX - x50[x];
    let yDiff = staringPointY - y50[x];
    let distance = Math.sqrt((xDiff * xDiff) + (yDiff * yDiff));

    // Calculate precision percentage
    let halfWindowHeight = windowHeight / 2;
    let precision = 0;
    if (distance <= halfWindowHeight && distance > -1) {
      precision = 100 - (distance / halfWindowHeight * 100);
    } else if (distance > halfWindowHeight) {
      precision = 0;
    } else if (distance > -1) {
      precision = 100;
    }

    // Store the precision
    precisionPercentages[x] = precision;
  }
}

/*
 * Calculates the average of all precision percentages calculated
 */
function calculateAverage(precisionPercentages) {
  let precision = 0;
  for (let x = 0; x < 50; x++) {
    precision += precisionPercentages[x];
  }
  precision = precision / 50;
  return precision;
}




/* js/precision_store_points.js */

/**
 * Sets store_points to true, so all the occuring prediction
 * points are stored
 */
function store_points_variable(){
  wg_eyetuner.params.storingPoints = true;
}

/**
 * Sets store_points to false, so prediction points aren't
 * stored any more
 */
function stop_storing_points_variable(){
  wg_eyetuner.params.storingPoints = false;
}




/* js/resize_canvas.js */

function resize() {
    let canvas = document.getElementById('plotting_canvas');
    let context = canvas.getContext('2d');
    context.clearRect(0, 0, canvas.width, canvas.height);
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize, false);
