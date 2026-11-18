import React from "react";
import {Composition} from "remotion";
import {SyncTest} from "./SyncTest";
import {MainVideo} from "./MainVideo";
import phrases from "./phrases.json";
const dur=Math.max(300,Math.ceil(((phrases[phrases.length-1]?.end||30)+2)*30));
export const RemotionRoot=()=>(<><Composition id="SyncTest" component={SyncTest} durationInFrames={Math.min(450,dur)} fps={30} width={1080} height={1920}/><Composition id="MainVideo" component={MainVideo} durationInFrames={dur} fps={30} width={1080} height={1920}/></>);
