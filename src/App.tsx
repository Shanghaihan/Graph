import axios from 'axios';
import React, {useEffect, useMemo, useReducer, useState } from 'react';
import './App.css';
import  { NetWork, Scatter} from './component/Graph';

function reducer(state:any,action:any) {
    switch (action.type) {
        case 'changeState':
            return action.currentGraph
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
            </context.Provider>     
        </div>
    );
}

export default App;
