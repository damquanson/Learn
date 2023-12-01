import { useState } from 'react'
import './App.css'

function App() {
  const [name,setName]=useState("")
  const [todos,setTodos]=useState([])

  function handleSubmit(e) {
    e.preventDefault()
    console.log('aa')
    setTodos ([
    ...todos,
    { id: crypto.randomUUID(), title: name, completed:
    false },
    ])
    setName('')
  }
 return (
  <div className='div1'>
  <form className='form-name' onSubmit={handleSubmit}>
  <label htmlFor='item' > Label </label>
  <input  type='text' id='items' value={name} onChange={e=> setName(e.target.value)}/>
  <button > Add</button>
  </form>
  <div className='listItem'>
    <ul>
      {todos.map((todo) => {return (<li key={todo.id}> {todo.title} </li>)})}
   

    </ul>
  </div>
  </div>
 )
}

export default App
