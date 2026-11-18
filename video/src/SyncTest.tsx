import React from "react";
import {AbsoluteFill,Audio,staticFile,useCurrentFrame,useVideoConfig} from "remotion";
import phrases from "./phrases.json";
export const SyncTest=()=>{const f=useCurrentFrame();const {fps}=useVideoConfig();const t=f/fps;const c=(phrases as any[]).find(p=>t>=p.start&&t<=p.end);return(<AbsoluteFill style={{backgroundColor:"#0b0f19",color:"#fff",justifyContent:"center",alignItems:"center",padding:60,textAlign:"center",fontFamily:"Noto Sans Devanagari,sans-serif"}}><Audio src={staticFile("song.mp3")}/><div style={{fontSize:64,fontWeight:800}}>{c?c.text:"SYNC TEST"}</div><div style={{position:"absolute",bottom:120,fontSize:32,opacity:0.7}}>{t.toFixed(2)}s</div></AbsoluteFill>);};
