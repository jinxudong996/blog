interface ClockConstructor {
    new (hour: number, minute: number)
  }
  
  // error
  class Clock implements ClockConstructor {
    currentTime: Date
    constructor(h: number, m: number) { }
  }