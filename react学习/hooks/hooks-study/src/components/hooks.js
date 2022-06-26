import {useState,useEffect} from 'react'
import axios from 'axios'

function usePost(){
  const [post,setPost] = useState({})
  useEffect(() => {
    axios.get('https://jsonplaceholder.typicode.com/posts/1')
      .then(res => setPost(res.data))
  },[])
  return [post,setPost]
}

function CustomHooks(){
  const [post] = usePost({});
  
  return (
    <div>
      <div>{post.title}</div>
      <div>{post.body}</div>
    </div>
  )
}

export default CustomHooks