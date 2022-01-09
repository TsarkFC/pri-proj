import { useState } from 'react';
import { getAll, getFullTextSearch, Query, QueryResult } from './query/Query';
import { SearchResults } from './SearchResults';

function App() {
  const [queryResult, setQueryResult] = useState<QueryResult | null>(null)
  const [queryInput, setQueryInput] = useState("")

  const runQuery = (query: Query) => {
    query(queryInput)
      .then(result => {
        console.log(result.data)
        setQueryResult(result.data)
      })
  }

  return <div id="layout">
    <h1>Greatest Search Engine Ever</h1>
    <form onSubmit={ (event) => { event.preventDefault(); runQuery(getFullTextSearch) } }>
      <input type="text" value={queryInput} onChange={ (event) => setQueryInput(event.target.value) } />
      <input type="submit" value="Search" />
    </form>
    {queryResult === null ? null : <SearchResults result={queryResult} /> }
  </div>
}

export default App;
