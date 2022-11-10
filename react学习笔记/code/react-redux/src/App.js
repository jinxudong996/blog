import Count from './components/Count'
import { Provider } from 'react-redux';
import { store } from './store'; 

function App() {
  return (
    <div className="App">
      <Provider store={store}>
        <Count></Count>
      </Provider>
      
    </div>
  );
}

export default App;
