
import './App.css'
import { MathJax, MathJaxContext } from "better-react-mathjax";

import MarkDownEditor from './components/MarkdownEditor/MarkdownEditor'

const mathJaxConfig = {
  tex: {
    inlineMath: [["$", "$"]],
    displayMath: [["$$", "$$"]],
  },
};


function App() {

  return (

    <MathJaxContext config={mathJaxConfig}>
      <h1 className='text-blue-500 text-3xl'>MarkdownEditor</h1>
      <MarkDownEditor />
    </MathJaxContext>

  )
}

export default App
