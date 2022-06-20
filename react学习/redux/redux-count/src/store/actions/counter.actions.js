import { INCREMENT, DECREMENT } from "../const/counter.const";

export const increment = payload => ({type: INCREMENT});
export const decrement = payload => ({type: DECREMENT});
