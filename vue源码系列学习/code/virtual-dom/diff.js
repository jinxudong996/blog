function diff(oldTree,newTree){
    let index = 0;
    let patches = {};
    dfWalk(oldTree,newTree,index,patches)
}

