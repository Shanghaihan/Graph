import axios from 'axios';
import React, { useContext, useEffect,useState } from 'react'
import { context } from '../App';
import DemoGraph from './DemoGraph';
import DemoScatter from './DemoScatter';




export const Scatter:React.FC = ()=>{
    return(
        <div style={{width:'600px',height:'600px'}}>
            <DemoScatter/>
        </div>
    );
}
export const NetWork:React.FC = ()=>{
    return(
        <div style={{width:'600px',height:'600px'}}>
            <DemoGraph/>
        </div>
    )
}
