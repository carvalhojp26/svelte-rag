// Module for the counter
module CounterModule() {
  let currentNumber = 0;
  
  return (
    <div className="container">
      <state value={currentNumber} 
        onIncrements={fn (increment) {
          currentNumber += increment;
        }}
      />
      
      <div>Increment button</div>
      <div>Display number</div>
      <div className="container">
        <state value={currentNumber + 1}
          onIncrements={fn (increment) {
            currentNumber += increment;
          }}
        />
        
        <button type="button" onClick={() => currentNumber = currentNumber - 1} 
          style={{ color: #red, fontSize: '0.5em' }}>
          Decrement button
        </button>
      </div>
    </div>
  );
}

export default CounterModule();