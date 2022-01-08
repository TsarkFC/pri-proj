import axios from 'axios';
import { useState } from 'react';

function App() {
  const [queryResult, setQueryResult] = useState<any>(null)

  const runQuery = () => {
    axios.get("http://localhost:3001/test")
      .then(result => {
        console.log(result)
        setQueryResult(result)
      })
  }


  return <div>
    <h1>Greatest Search Engine Ever</h1>
    <input type="button" onClick={ runQuery } value="click here to run test query" />
    {queryResult === null ? null : 
      <>
        <p>Found {queryResult.data.response.numFound} results.</p>
        {queryResult.data.response.docs.map((doc: any, idx: number) => <div key={idx}>
          <h2><a href={doc["url"]}>{doc["article.title"]}</a></h2>
          <p>
            {doc["article.entities.title"].map((entity: string, idx: number, arr: Array<String>) => <span key={idx}>
              {entity + (arr.length - 1 !== idx ? ", " : "")}
            </span>)}
          </p>
        </div>)}
      </>    
    }
  </div>
}

export default App;
