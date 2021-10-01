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

  slice(...input) {
    return this._arr.slice(...input);
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
EYE_TUNER_RUNTIME.time_queue = new Queue(100);
EYE_TUNER_RUNTIME.last_coord = null;
EYE_TUNER_RUNTIME.last_speed = 0;
EYE_TUNER_RUNTIME.time_elapsed = 0;
EYE_TUNER_RUNTIME.make_listener = function(set_speed_callback) {
  return function(data, clock) {

  let last_time = EYE_TUNER_RUNTIME.time_elapsed;
  let time_elapsed = clock / 1000;  // ms
  let time_delta = (time_elapsed - last_time);
  EYE_TUNER_RUNTIME.time_elapsed = time_elapsed
  EYE_TUNER_RUNTIME.time_queue.enqueue(time_elapsed);

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

  if (EYE_TUNER_RUNTIME.speed_queue.length() >= 90) {
    let speeds = [];
    for (let it = 0; it < 5; it++) {
      let sliced = EYE_TUNER_RUNTIME.speed_queue.slice(it * 20, (it + 1) * 20)
      speeds.push(sliced.reduce((sum, value) => (sum + value), 0) / sliced.length);
    }
    console.log(speeds)

    let sliced = EYE_TUNER_RUNTIME.speed_queue.slice(80, 100);
    let cur_speed = sliced.reduce((sum, value) => (sum + value), 0) / sliced.length;
    if (cur_speed >= 800) {
      set_speed_callback(10);
    } else if (cur_speed >= 600) {
      set_speed_callback(40);
    } else if (cur_speed >= 400) {
      set_speed_callback(60);
    } else if (cur_speed >= 200) {
      set_speed_callback(80);
    } else {
      set_speed_callback(100);
    }
  }

  // console.log(EYE_TUNER_RUNTIME.time_queue._arr[0], time_delta)
  // console.log(EYE_TUNER_RUNTIME.speed_queue._arr[0]);

}
}
