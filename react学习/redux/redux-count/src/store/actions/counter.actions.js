import { INCREMENT, DECREMENT } from "../const/counter.const";

export const increment = payload => ({type: INCREMENT,payload});
export const decrement = payload => ({type: DECREMENT,payload});
