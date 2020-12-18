//@ts-ignore
import React, { useContext, useEffect, useRef } from 'react';
import { Scatter} from '@ant-design/charts';
import { context } from '../App';

const DemoScatter: React.FC = () => { 
    const ref = useRef();
    //@ts-ignore
    const {currentGraph,dispatch,data} = useContext(context)
    useEffect(() => {
        if(ref.current){   
            dispatch({
                type:'changeColor',
                //@ts-ignore
                color:ref.current.chart.geometries[0].dataArray.flat()
            })
        }
    }, [])

    useEffect(() => {
        if (ref.current) {
            // 点击 point
            //@ts-ignore
            ref.current.on('element:click', (e) => {
                dispatch({
                    type:'changeState',
                    currentGraph:e.data.data
                }) 
            });
        }
    },[dispatch]);
    var config = {
        appendPadding: 30,
        data: data,
        xField: 'x',
        yField: 'y',
        colorField: 'cluster',
        legend: { position: 'top' },
        size: 2,
        shape: 'circle',
        pointStyle: {
          fillOpacity: 1.0,
          stroke: '#bbb',
        },
        xAxis: {
            min:-100,
            max:100,
            grid: { line: { style: { stroke: 'grey' } } },
        },
        yAxis: {
            line: { style: { stroke: 'grey' } } 
        
        },
        // quadrant: {
        //   xBaseline: 0,
        //   yBaseline: 0,
        // },
      };
    //@ts-ignore
    return <Scatter {...config} chartRef={ref} />;
};
export default DemoScatter;