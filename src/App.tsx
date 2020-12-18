import axios from 'axios';
import React, {useEffect, useMemo, useReducer, useState } from 'react';
import './App.css';
import  { NetWork, Parallel, Scatter} from './component/Graph';

function reducer(state:any,action:any) {
    switch (action.type) {
        case 'changeState':
            return  {currentGraph:action.currentGraph,...state}
        case 'changeColor':
            return {color:action.color,...state}
        default:
            return state;
    }
}
const useData =(action:any)=>{
    const [data,setData] = useState([]);
    const [pending,setPending] = useState(true);
    useEffect(() => {
        const getData = async()=>{
            setPending(true);
            const res = await (await axios.get('../struc.json')).data;
            setPending(false);
            res.forEach((ele:any)=>{
                ele.cluster = "type"+ele.cluster  ;
            });
            setData(res); 
            action({
                type:'changeState',
                currentGraph:res[10]
            }) 
        }
        getData();
        return () => {
        }
    },[]) 
    return {data,pending};
}
export const context = React.createContext({});

function App() {
    const [currentGraph,dispatch] = useReducer<any>(reducer,{})
    const {data,pending} = useData(dispatch);
    return (
        <div className="App">
            <context.Provider value={{ 
                data,
                currentGraph,dispatch,
            }}>
                <Scatter/>
                <NetWork/>
                <Parallel/>
            </context.Provider>     
        </div>
    );
}

export default App;
