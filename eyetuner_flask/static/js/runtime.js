const EYE_TUNER_RUNTIME = {};

class Queue {
  constructor(max_length=undefined) {
    this._arr = [];
    this.max_length = max_length;
  }
  enqueue(item) {
    this._arr.push(item);
    while (this._arr.length > this.max_length) {
      this.dequeue();
    }
  }
  dequeue() {
    return this._arr.shift();
  }

  items() {
    return [...this._arr]
  }

  clear() {
    this._arr = [];
  }

  length() {
    return this._arr.length
  }

}

EYE_TUNER_RUNTIME.speed_queue = new Queue(100);
EYE_TUNER_RUNTIME.last_coord = null;
EYE_TUNER_RUNTIME.last_speed = 0;
EYE_TUNER_RUNTIME.time_elapsed = 0;
EYE_TUNER_RUNTIME.listener = function(data, clock) {

  console.log(clock);

  let last_time = EYE_TUNER_RUNTIME.time_elapsed;
  let time_delta = clock - last_time;
  EYE_TUNER_RUNTIME.time_elapsed = clock / 1000;  // ms

  let last_coord = EYE_TUNER_RUNTIME.last_coord;
  EYE_TUNER_RUNTIME.last_coord = data;

  if (last_coord === null) {
    return
  }

  let speed_x = (data.x - last_coord.x) / time_delta;
  let speed_y = (data.y - last_coord.y) / time_delta;

  let speed = hypot(speed_x, speed_y);

  EYE_TUNER_RUNTIME.speed_queue.enqueue(speed);
  EYE_TUNER_RUNTIME.last_speed = speed;

  console.log(EYE_TUNER_RUNTIME.speed_queue.items());

}
