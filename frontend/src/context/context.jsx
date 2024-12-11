import {createContext, useReducer} from "react"
import { reducer } from "./reducer"
import initialState from "./state"
export const Context = createContext()

const ContextProvider =(props)=>{
    const [state,dispatch] = useReducer(initialState,reducer)
    return(
        <Context.Provider value={[state,dispatch]}>
            {props.children}
        </Context.Provider>
    )
}

export default ContextProvider