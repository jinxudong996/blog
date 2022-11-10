

const INCREMENT = 'increment';
const DECREMENT = 'decrement';
// const INCREMENT_ASYNC = 'increment_async';

const initialState = {
  count: 2
}

const reducer = (state = initialState, action) => {
  switch(action.type) {
    
    case INCREMENT:
      return {
        count: state.count + 1
      }
    case DECREMENT:
      return {
        count: state.count - 1
      }
    default: 
      return state;
  }
}

export default reducer