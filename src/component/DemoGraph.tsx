import React, { useContext } from 'react'
import G6 from '@antv/g6';
import ReactDOM from 'react-dom';
import { useEffect } from 'react';
import { context } from '../App';
const DemoGraph:React.FC = ()=>{
    const ref = React.useRef<HTMLDivElement>(null);
    //@ts-ignore
    const {currentGraph} = useContext(context);
    console.log(currentGraph)
    const data = {
        // 点集
        nodes: currentGraph.currentGraph==null?[]:currentGraph.currentGraph.nodes,
        // 边集
        edges: currentGraph.currentGraph==null?[]:currentGraph.currentGraph.edgess,
    };
    //@ts-ignore 
    var graph:any = null;
    useEffect(() => {
        if(!graph){
           ref.current?.firstChild?.remove();
            graph = new G6.Graph({
                //@ts-ignore    
                container: ReactDOM.findDOMNode(ref.current), // String | HTMLElement，必须，在 Step 1 中创建的容器 id 或容器本身
                width: 600, // Number，必须，图的宽度
                height: 600, // Number，必须，图的高度
                layout: {
                    type: 'concentric',
                    center: [ 300, 300 ],     // 可选，默认为图的中心
                    linkDistance: 50,         // 可选，边长
                    preventOverlap: true,     // 可选，必须配合 nodeSize
                    nodeSize: 10,             // 可选
                    minNodeSpacing:15
                }
            }); 
            graph.data(data); // 读取 Step 2 中的数据源到图上
            graph.render()// 渲染图
        }  
    },[data])
    return(
        <div ref={ref}></div>    
    )
};
export default DemoGraph;