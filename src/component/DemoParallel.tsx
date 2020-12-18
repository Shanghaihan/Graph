import React, { useContext, useEffect ,useRef} from 'react';
import { context } from '../App';

const DemoParallel:React.FC = ()=>{
    const ref = useRef<HTMLDivElement>(null);
    //@ts-ignore
    const { data,currentGraph} = useContext(context);
    const datas = data.map((ele:any)=>{
        return [ele.count,ele.cite,ele.position,ele.connect,ele.totalCount,ele.totalCite,ele.totalPosition,ele.totalConnect];
    })
    useEffect(() => {
        //@ts-ignore
        var echarts = require('echarts');
        let myChart = echarts.init(document.getElementById('parallel')); 
        let option = {
            parallelAxis: [
                {dim: 0, name: 'count'},
                {dim: 1, name: 'cite'},
                {dim: 2, name: 'position'},
                {dim: 3, name: 'connect'},
                {dim: 4, name: 'totalCount'},
                {dim: 5, name: 'totalCite'},
                {dim: 6, name: 'totalPosition'},
                {dim: 7, name: 'totalConnect'},
            ],
            parallel: {                         // 这是『坐标系』的定义
                left: '5%',                     // 平行坐标系的位置设置
                right: '5%',
                bottom: '5%',
                top: '10%',
            },
            series: {
                type: 'parallel',
                lineStyle: {
                    width: 1,
                color:function(d:any){
                        return data[d.dataIndex] === currentGraph ? 'red':'rgba(116, 203, 237,1)';
                    },
                },
                data: datas
            },
        };
        //@ts-ignore
        myChart.setOption(option);
        return () => {
        }
    }, [datas])
    return(
        <div ref={ref} id="parallel" style={{width:'100%',height:'100%'}}></div>
    )
}
export default DemoParallel;