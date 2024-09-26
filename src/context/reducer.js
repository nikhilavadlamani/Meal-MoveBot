export const reducer =(state,action)=>{
    if(action.type){
        return {
            ...state,
            ...action.payload
        }
    }
    return state
}

